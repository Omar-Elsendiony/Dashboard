# submit_timesheet.py
import json
from typing import Any, Dict, Optional
from datetime import datetime, date, timezone, timedelta
from tau_bench.envs.tool import Tool


class SubmitTimesheet(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        employee_id: str,
        work_date: str,
        clock_in_time: str,
        clock_out_time: str,
        break_duration_minutes: int = 0,
        project_code: Optional[str] = None,
        status: str = "submitted",
    ) -> str:
        """
        Create a new timesheet row in data["employee_timesheets"] and return JSON:
        {"timesheet_id": str, "success": True} or {"error": "...", "halt": True}
        """

        # ---------- helpers ----------
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        def parse_date(d: str) -> date:
            try:
                return datetime.fromisoformat(d).date()
            except ValueError:
                # Fallback for plain YYYY-MM-DD
                try:
                    return datetime.strptime(d, "%Y-%m-%d").date()
                except Exception:
                    raise ValueError("work_date must be ISO format YYYY-MM-DD")

        def parse_ts(ts: str) -> datetime:
            """
            Accepts ISO 8601 timestamps. If no timezone is present,
            interpret as naive local and treat consistently (no TZ math needed here).
            """
            try:
                return datetime.fromisoformat(ts)
            except ValueError:
                # Try common format without microseconds
                try:
                    return datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
                except Exception:
                    raise ValueError(
                        "clock_in_time/clock_out_time must be ISO 8601 (e.g., 2025-10-01T09:00:00)"
                    )

        # ---------- tables ----------
        timesheets = data.get("employee_timesheets", {})
        # Optional existence check against either 'employees' or 'users'
        employees_tbl = data.get("employees") or data.get("users")

        # ---------- validations ----------
        if not employee_id:
            raise ValueError("employee_id is required")
        if not work_date:
            raise ValueError("work_date is required")
        if not clock_in_time or not clock_out_time:
            raise ValueError("clock_in_time and clock_out_time are required")

        if employees_tbl and isinstance(employees_tbl, dict):
            # Accept key presence OR any record with matching id field
            if (employee_id not in employees_tbl) and not any(
                (isinstance(v, dict) and str(v.get("user_id") or v.get("employee_id")) == str(employee_id))
                for v in employees_tbl.values()
            ):
                return json.dumps({"error": f"Employee {employee_id} not found", "halt": True})

        # Status validation: this tool should only create 'draft' or 'submitted' rows
        valid_statuses = ["draft", "submitted", "approved", "rejected"]
        if status not in valid_statuses:
            return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}", "halt": True})
        if status in ("approved", "rejected"):
            return json.dumps({
                "error": "Timesheets cannot be created directly as 'approved' or 'rejected'. Use an approval tool.",
                "halt": True
            })

        if break_duration_minutes is None:
            break_duration_minutes = 0
        if not isinstance(break_duration_minutes, int) or break_duration_minutes < 0:
            return json.dumps({"error": "break_duration_minutes must be a non-negative integer", "halt": True})

        # Parse dates/times
        try:
            _work_date = parse_date(work_date)
            cin = parse_ts(clock_in_time)
            cout = parse_ts(clock_out_time)
        except ValueError as ve:
            return json.dumps({"error": str(ve), "halt": True})

        if cout <= cin:
            return json.dumps({"error": "clock_out_time must be after clock_in_time", "halt": True})

        # Compute total hours with break deduction
        raw_hours = (cout - cin).total_seconds() / 3600.0
        total_hours = raw_hours - (break_duration_minutes / 60.0)
        if total_hours < 0:
            return json.dumps({"error": "Break time exceeds worked time", "halt": True})

        # Round to 2 decimals to match DECIMAL(4,2)
        total_hours = round(total_hours, 2)
        if total_hours > 99.99:
            return json.dumps({"error": "total_hours exceeds allowed limit", "halt": True})

        # ---------- create row ----------
        timesheet_id = generate_id(timesheets)
        timestamp = "2025-10-01T00:00:00"

        new_row = {
            "timesheet_id": timesheet_id,
            "employee_id": str(employee_id),
            "work_date": _work_date.isoformat(),
            "clock_in_time": cin.isoformat(),
            "clock_out_time": cout.isoformat(),
            "break_duration_minutes": int(break_duration_minutes),
            "total_hours": f"{total_hours:.2f}",
            "project_code": project_code,
            "approved_by": None,  # set by approval tool
            "status": status,     # 'draft' or 'submitted'
            "created_at": timestamp,
            "updated_at": timestamp,
        }

        # Save
        timesheets[timesheet_id] = new_row
        data["employee_timesheets"] = timesheets

        return json.dumps({"timesheet_id": timesheet_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "submit_timesheet",
                "description": "Create a new employee timesheet entry ('draft' or 'submitted').",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "employee_id": {"type": "string", "description": "Employee ID (must exist)"},
                        "work_date": {"type": "string", "description": "Work date (YYYY-MM-DD, ISO 8601)"},
                        "clock_in_time": {"type": "string", "description": "Clock-in timestamp (ISO 8601)"},
                        "clock_out_time": {"type": "string", "description": "Clock-out timestamp (ISO 8601)"},
                        "break_duration_minutes": {"type": "integer", "description": "Break duration in minutes (>= 0, default 0)"},
                        "project_code": {"type": "string", "description": "Optional project code (<= 50 chars)"},
                        "status": {"type": "string", "description": "Timesheet status: draft or submitted (default submitted)"}
                    },
                    "required": ["employee_id", "work_date", "clock_in_time", "clock_out_time"]
                }
            }
        }
