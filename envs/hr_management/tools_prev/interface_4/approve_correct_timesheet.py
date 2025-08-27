# approve_correct_timesheet.py
import json
from typing import Any, Dict, Optional
from datetime import datetime


from tau_bench.envs.tool import Tool


class ApproveCorrectTimesheet(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        timesheet_id: str,
        approved_by: str,
        status: str,
        clock_in_time: Optional[str] = None,
        clock_out_time: Optional[str] = None,
        break_duration_minutes: Optional[int] = None,
        total_hours: Optional[float] = None,
        correction_notes: Optional[str] = None,
    ) -> str:
        """
        Approve or reject a timesheet, with optional corrections to time fields.
        Returns JSON: {"success": True, "message": "Timesheet processed"} or {"error": "...", "halt": True}
        """

        # -------- helpers --------
        def parse_ts(ts: str) -> datetime:
            # Accept ISO 8601 with or without 'T' separator
            try:
                return datetime.fromisoformat(ts)
            except ValueError:
                try:
                    return datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
                except Exception:
                    raise ValueError("Timestamps must be ISO 8601 (e.g., 2025-10-01T09:00:00)")

        def round_hours(h: float) -> float:
            # Match DECIMAL(4,2)
            return round(h, 2)

        # -------- load tables --------
        timesheets = data.get("employee_timesheets", {})
        employees_tbl = data.get("employees") or data.get("users")  # optional approver existence check

        # -------- basic validations --------
        if not timesheet_id:
            raise ValueError("timesheet_id is required")
        if not approved_by:
            raise ValueError("approved_by is required")

        if str(timesheet_id) not in timesheets:
            return json.dumps({"error": f"Timesheet {timesheet_id} not found", "halt": True})

        # Check approver existence if employee/user table is present
        if employees_tbl and isinstance(employees_tbl, dict):
            approver_exists = (approved_by in employees_tbl) or any(
                (isinstance(v, dict) and str(v.get("user_id") or v.get("employee_id")) == str(approved_by))
                for v in employees_tbl.values()
            )
            if not approver_exists:
                return json.dumps({"error": f"Approver {approved_by} not found", "halt": True})

        valid_statuses = ["approved", "rejected"]
        if status not in valid_statuses:
            return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}", "halt": True})

        row = timesheets[str(timesheet_id)]

        # Disallow re-approving an already terminal record unless explicitly correcting+re-finalizing
        if row.get("status") in ("approved", "rejected") and not any(
            x is not None for x in [clock_in_time, clock_out_time, break_duration_minutes, total_hours, correction_notes]
        ):
            return json.dumps({
                "error": f"Timesheet {timesheet_id} is already {row.get('status')}. Provide corrections if you intend to re-finalize.",
                "halt": True
            })

        # -------- apply corrections (if any) --------
        # Start with current values
        cin_str = row.get("clock_in_time")
        cout_str = row.get("clock_out_time")
        brk = row.get("break_duration_minutes") if row.get("break_duration_minutes") is not None else 0

        # Update from inputs
        if clock_in_time is not None:
            cin_str = clock_in_time
        if clock_out_time is not None:
            cout_str = clock_out_time
        if break_duration_minutes is not None:
            if not isinstance(break_duration_minutes, int) or break_duration_minutes < 0:
                return json.dumps({"error": "break_duration_minutes must be a non-negative integer", "halt": True})
            brk = break_duration_minutes

        # Parse times if present for recompute or validation
        cin_dt = None
        cout_dt = None
        if cin_str:
            try:
                cin_dt = parse_ts(cin_str)
            except ValueError as ve:
                return json.dumps({"error": str(ve), "halt": True})
        if cout_str:
            try:
                cout_dt = parse_ts(cout_str)
            except ValueError as ve:
                return json.dumps({"error": str(ve), "halt": True})

        # If either in/out is present, require both for consistency
        if (clock_in_time is not None) ^ (clock_out_time is not None):
            return json.dumps({"error": "Provide both clock_in_time and clock_out_time when correcting times.", "halt": True})

        # Compute total_hours if not explicitly provided and times are available
        computed_total = None
        if total_hours is None and (cin_dt is not None and cout_dt is not None):
            if cout_dt <= cin_dt:
                return json.dumps({"error": "clock_out_time must be after clock_in_time", "halt": True})
            raw_hours = (cout_dt - cin_dt).total_seconds() / 3600.0
            computed_total = raw_hours - (brk or 0) / 60.0
            if computed_total < 0:
                return json.dumps({"error": "Break time exceeds worked time", "halt": True})
            computed_total = round_hours(computed_total)

        # Use provided total_hours if given; otherwise the computed one (if available); otherwise keep existing
        final_total_hours = total_hours if total_hours is not None else (computed_total if computed_total is not None else row.get("total_hours"))

        # Validate final_total_hours
        if final_total_hours is None:
            # If we still have no total, but times exist, we should have computed it. If neither times nor total provided, keep existing if present.
            return json.dumps({"error": "total_hours is missing and cannot be computed; provide times or total_hours.", "halt": True})

        try:
            final_total_val = float(final_total_hours)
        except Exception:
            return json.dumps({"error": "total_hours must be a number", "halt": True})

        if final_total_val < 0:
            return json.dumps({"error": "total_hours cannot be negative", "halt": True})
        if final_total_val > 99.99:
            return json.dumps({"error": "total_hours exceeds allowed limit", "halt": True})

        # -------- persist updates --------
        timestamp = "2025-10-01T00:00:00"

        if cin_str is not None:
            row["clock_in_time"] = cin_str
        if cout_str is not None:
            row["clock_out_time"] = cout_str
        if brk is not None:
            row["break_duration_minutes"] = int(brk)

        # Store as string with 2 decimals to mirror DECIMAL(4,2)
        row["total_hours"] = f"{round_hours(final_total_val):.2f}"

        row["approved_by"] = str(approved_by)
        row["status"] = status  # approved or rejected
        if correction_notes:
            row["correction_notes"] = correction_notes  # not in table, but harmless in in-memory dict
        row["updated_at"] = timestamp

        # Save back
        timesheets[str(timesheet_id)] = row
        data["employee_timesheets"] = timesheets

        return json.dumps({"success": True, "message": "Timesheet processed"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "approve_correct_timesheet",
                "description": "Approve or reject a timesheet with optional corrections to time fields and totals.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "timesheet_id": {"type": "string", "description": "Timesheet ID to process"},
                        "approved_by": {"type": "string", "description": "Approver's user/employee ID"},
                        "status": {"type": "string", "description": "New status: approved or rejected"},
                        "clock_in_time": {"type": "string", "description": "Corrected clock-in timestamp (ISO 8601)"},
                        "clock_out_time": {"type": "string", "description": "Corrected clock-out timestamp (ISO 8601)"},
                        "break_duration_minutes": {"type": "integer", "description": "Corrected break duration in minutes (>= 0)"},
                        "total_hours": {"type": "number", "description": "Corrected total hours (overrides computed if provided)"},
                        "correction_notes": {"type": "string", "description": "Notes about corrections (optional)"},
                    },
                    "required": ["timesheet_id", "approved_by", "status"]
                }
            }
        }
