# correct_payroll.py
import json
from typing import Any, Dict, Optional

from tau_bench.envs.tool import Tool


class CorrectPayroll(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        payroll_id: str,
        correction_reason: str,
        finance_officer_approval: bool,
        hours_worked: Optional[float] = None,
        hourly_rate: Optional[float] = None,
        net_pay: Optional[float] = None,
    ) -> str:
        """
        Correct an existing payroll record.
        Returns: {"success": True, "message": "Payroll corrected"} or {"error": "...", "halt": True}
        """

        # ---------- helpers ----------
        def to_decimal_str(val: float, places: int = 2) -> str:
            return f"{round(float(val), places):.{places}f}"

        # ---------- load ----------
        payroll_table = data.get("payroll_records", {})

        # ---------- validations ----------
        if not finance_officer_approval:
            return json.dumps({"error": "Finance Officer approval required", "halt": True})
        if not payroll_id:
            raise ValueError("payroll_id is required")
        if str(payroll_id) not in payroll_table:
            return json.dumps({"error": f"Payroll record {payroll_id} not found", "halt": True})
        if not correction_reason or not str(correction_reason).strip():
            return json.dumps({"error": "correction_reason is required", "halt": True})

        row = payroll_table[str(payroll_id)]

        # Require at least one correction field
        if hours_worked is None and hourly_rate is None and net_pay is None:
            return json.dumps({"error": "Provide at least one of hours_worked, hourly_rate, or net_pay", "halt": True})

        # ---------- apply corrections (in-memory) ----------
        # Pull existing numeric values as floats for recalculation
        existing_hours = float(row.get("hours_worked") or 0)
        existing_rate = float(row.get("hourly_rate") or 0)
        existing_net = float(row.get("net_pay") or 0)

        new_hours = existing_hours if hours_worked is None else float(hours_worked)
        new_rate = existing_rate if hourly_rate is None else float(hourly_rate)

        # Basic non-negative validations
        if new_hours < 0:
            return json.dumps({"error": "hours_worked cannot be negative", "halt": True})
        if new_rate < 0:
            return json.dumps({"error": "hourly_rate cannot be negative", "halt": True})

        # net_pay logic:
        # - If explicitly provided, use it (validate non-negative).
        # - Else, recompute as hours * rate.
        if net_pay is not None:
            try:
                new_net = float(net_pay)
            except Exception:
                return json.dumps({"error": "net_pay must be a number", "halt": True})
            if new_net < 0:
                return json.dumps({"error": "net_pay cannot be negative", "halt": True})
        else:
            new_net = round(new_hours * new_rate, 2)

        # DECIMAL capacity checks (defensive; can be adjusted to your real limits)
        if new_hours > 9999.99:
            return json.dumps({"error": "hours_worked exceeds allowed limit", "halt": True})
        if new_rate > 9999999999.99:
            return json.dumps({"error": "hourly_rate exceeds allowed limit", "halt": True})
        if new_net > 9999999999.99:
            return json.dumps({"error": "net_pay exceeds allowed limit", "halt": True})

        # ---------- persist ----------
        timestamp = "2025-10-01T00:00:00"

        row["hours_worked"] = to_decimal_str(new_hours, 2)
        row["hourly_rate"] = to_decimal_str(new_rate, 2)
        row["net_pay"] = to_decimal_str(new_net, 2)
        row["updated_at"] = timestamp
        # annotate who approved & reason (not in schema, harmless in-memory fields)
        row["approved_by"] = "finance_officer"
        row["correction_reason"] = str(correction_reason)

        payroll_table[str(payroll_id)] = row
        data["payroll_records"] = payroll_table

        return json.dumps({"success": True, "message": "Payroll corrected"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "correct_payroll",
                "description": "Correct an existing payroll record (hours, rate, and/or net pay).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "payroll_id": {"type": "string", "description": "Payroll record ID (required)"},
                        "hours_worked": {"type": "number", "description": "Corrected hours worked (>= 0, optional)"},
                        "hourly_rate": {"type": "number", "description": "Corrected hourly rate (>= 0, optional)"},
                        "net_pay": {"type": "number", "description": "Corrected net pay (>= 0, optional). If omitted, recalculated as hours*rate."},
                        "correction_reason": {"type": "string", "description": "Reason for correction (required)"},
                        "finance_officer_approval": {"type": "boolean", "description": "Finance Officer approval (required)"},
                    },
                    "required": ["payroll_id", "correction_reason", "finance_officer_approval"]
                }
            }
        }
