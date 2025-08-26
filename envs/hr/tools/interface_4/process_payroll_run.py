# process_payroll_run.py
import json
from typing import Any, Dict, List, Optional
from datetime import datetime, date


from tau_bench.envs.tool import Tool


class ProcessPayrollRun(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        pay_period_start: str,
        pay_period_end: str,
        employee_ids: Optional[List[str]] = None,
        finance_officer_approval: bool = False,
    ) -> str:
        """
        Process payroll for a date range. Creates one payroll_records row per employee with
        approved hours in the period. Returns:
        {"success": True, "message": "Payroll run processed", "payroll_records_created": int}
        or {"error": "...", "halt": True}
        """

        # ---------- helpers ----------
        def parse_date(d: str) -> date:
            try:
                # Accepts 'YYYY-MM-DD' or ISO 8601 date
                return datetime.fromisoformat(d).date()
            except ValueError:
                try:
                    return datetime.strptime(d, "%Y-%m-%d").date()
                except Exception:
                    raise ValueError("Dates must be ISO format YYYY-MM-DD")

        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        def to_decimal_str(val: float, places: int = 2) -> str:
            return f"{round(val, places):.{places}f}"

        # ---------- load tables ----------
        payroll_table = data.get("payroll_records", {})
        timesheets = data.get("employee_timesheets", {})
        employees_tbl = data.get("employees") or data.get("users") or {}

        # ---------- validations ----------
        if not finance_officer_approval:
            return json.dumps({"error": "Finance Officer approval required", "halt": True})

        if not pay_period_start or not pay_period_end:
            raise ValueError("pay_period_start and pay_period_end are required")

        try:
            start_d = parse_date(pay_period_start)
            end_d = parse_date(pay_period_end)
        except ValueError as ve:
            return json.dumps({"error": str(ve), "halt": True})

        if end_d < start_d:
            return json.dumps({"error": "pay_period_end must be on/after pay_period_start", "halt": True})

        # Determine target employees
        target_employee_ids: List[str] = []

        if employee_ids:
            target_employee_ids = [str(eid) for eid in employee_ids]
        else:
            # Prefer all active employees from employees/users table
            if isinstance(employees_tbl, dict) and employees_tbl:
                for k, rec in employees_tbl.items():
                    if isinstance(rec, dict):
                        status = (rec.get("status") or "").lower()
                        # Default to active if status is missing but record exists
                        if status in ("", "active"):
                            # Prefer employee_id/user_id field if present, fallback to table key
                            eid = str(rec.get("employee_id") or rec.get("user_id") or k)
                            target_employee_ids.append(eid)
            else:
                # Fallback: gather employee_ids that have timesheets in the window
                seen = set()
                for ts in timesheets.values():
                    eid = str(ts.get("employee_id"))
                    if eid:
                        seen.add(eid)
                target_employee_ids = sorted(seen)

        # No employees to process?
        if not target_employee_ids:
            return json.dumps({"success": True, "message": "No employees to process for this period", "payroll_records_created": 0})

        # Ensure hourly_rate exists for all targets
        missing_rate: List[str] = []
        hourly_rate_by_emp: Dict[str, float] = {}
        for eid in target_employee_ids:
            rec = None
            # Try to find by key
            if eid in employees_tbl:
                rec = employees_tbl[eid]
            else:
                # Or by matching employee_id/user_id inside values
                for v in employees_tbl.values():
                    if isinstance(v, dict) and str(v.get("employee_id") or v.get("user_id")) == eid:
                        rec = v
                        break

            # Expect an hourly_rate on the employee/user record
            rate_val = None
            if isinstance(rec, dict):
                # Common field names; prefer 'hourly_rate'
                for key in ("hourly_rate", "pay_rate", "hourlyPay", "hourly"):
                    if key in rec and rec[key] is not None:
                        rate_val = rec[key]
                        break

            if rate_val is None:
                missing_rate.append(eid)
            else:
                try:
                    hourly_rate_by_emp[eid] = float(rate_val)
                except Exception:
                    missing_rate.append(eid)

        if missing_rate:
            return json.dumps({
                "error": f"Missing or invalid hourly_rate for employees: {', '.join(sorted(set(missing_rate)))}",
                "halt": True
            })

        # Aggregate APPROVED hours within the period per employee
        hours_by_emp: Dict[str, float] = {eid: 0.0 for eid in target_employee_ids}
        for ts in timesheets.values():
            try:
                eid = str(ts.get("employee_id"))
                if eid not in hours_by_emp:
                    continue

                status = (ts.get("status") or "").lower()
                if status != "approved":
                    continue  # only pay approved timesheets

                ts_date_str = ts.get("work_date")
                if not ts_date_str:
                    continue
                try:
                    ts_date = parse_date(ts_date_str)
                except Exception:
                    continue

                if not (start_d <= ts_date <= end_d):
                    continue

                th = ts.get("total_hours")
                if th is None:
                    continue
                hours = float(th) if isinstance(th, (int, float)) else float(str(th))
                if hours < 0:
                    continue
                hours_by_emp[eid] += hours
            except Exception:
                # Skip malformed entries defensively
                continue

        # Create payroll records for employees with > 0 hours
        created = 0
        timestamp = "2025-10-01T00:00:00"
        for eid in target_employee_ids:
            hours_worked = round(hours_by_emp.get(eid, 0.0), 2)
            if hours_worked <= 0:
                continue

            rate = hourly_rate_by_emp[eid]
            net_pay = round(hours_worked * rate, 2)

            payroll_id = generate_id(payroll_table)

            new_row = {
                "payroll_id": payroll_id,
                "employee_id": str(eid),
                "pay_period_start": start_d.isoformat(),
                "pay_period_end": end_d.isoformat(),
                "hours_worked": to_decimal_str(hours_worked, 2),
                "hourly_rate": to_decimal_str(rate, 2),
                "net_pay": to_decimal_str(net_pay, 2),
                "payment_date": end_d.isoformat(),  # set as period end by default
                "status": "approved",               # this run is finance-approved
                "approved_by": "finance_officer",
                "created_at": timestamp,
                "updated_at": timestamp,
            }

            payroll_table[payroll_id] = new_row
            created += 1

        data["payroll_records"] = payroll_table

        return json.dumps({
            "success": True,
            "message": "Payroll run processed",
            "payroll_records_created": created
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "process_payroll_run",
                "description": "Aggregate approved timesheets for a period and create payroll records per employee.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "pay_period_start": {"type": "string", "description": "Start date (YYYY-MM-DD) inclusive"},
                        "pay_period_end": {"type": "string", "description": "End date (YYYY-MM-DD) inclusive"},
                        "employee_ids": {"type": "array", "items": {"type": "string"}, "description": "Optional explicit employee IDs; defaults to all active"},
                        "finance_officer_approval": {"type": "boolean", "description": "Finance Officer approval (required)"}
                    },
                    "required": ["pay_period_start", "pay_period_end", "finance_officer_approval"]
                }
            }
        }
