# update_benefits_plan.py
import json
from typing import Any, Dict, Optional
from datetime import datetime, date

from tau_bench.envs.tool import Tool


class UpdateBenefitsPlan(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        plan_id: str,
        hr_director_approval: Optional[bool] = None,
        finance_officer_approval: Optional[bool] = None,
        plan_name: Optional[str] = None,
        provider: Optional[str] = None,
        employee_cost: Optional[float] = None,
        employer_cost: Optional[float] = None,
        status: Optional[str] = None,
        effective_date: Optional[str] = None,
        expiration_date: Optional[str] = None,
    ) -> str:
        """
        Update an existing benefits plan.
        Returns JSON: {"success": True, "message": "Benefits plan updated"} or {"error": "...", "halt": True}
        """

        # ---------- helpers ----------
        def parse_date(d: str) -> date:
            try:
                return datetime.fromisoformat(d).date()
            except ValueError:
                try:
                    return datetime.strptime(d, "%Y-%m-%d").date()
                except Exception:
                    raise ValueError("Dates must be ISO format YYYY-MM-DD")

        def to_decimal_str(val: float, places: int = 2) -> str:
            return f"{round(float(val), places):.{places}f}"

        # ---------- load table ----------
        plans = data.get("benefits_plans", {})

        # ---------- validations: required ----------
        if not plan_id:
            raise ValueError("plan_id is required")
        if str(plan_id) not in plans:
            return json.dumps({"error": f"Benefits plan {plan_id} not found", "halt": True})

        # Approvals: require BOTH to update (policy + financial implications)
        if hr_director_approval is None or finance_officer_approval is None:
            return json.dumps({
                "error": "HR Director and Finance Officer approvals are required to update a benefits plan",
                "halt": True
            })
        if not hr_director_approval or not finance_officer_approval:
            return json.dumps({
                "error": "Approval denied: both HR Director and Finance Officer must approve",
                "halt": True
            })

        row = plans[str(plan_id)]

        # If nothing to update
        if all(v is None for v in [plan_name, provider, employee_cost, employer_cost, status, effective_date, expiration_date]):
            return json.dumps({"success": True, "message": "No changes provided"})

        # ---------- field validations ----------
        # plan_name
        if plan_name is not None and not str(plan_name).strip():
            return json.dumps({"error": "plan_name cannot be empty", "halt": True})

        # provider length
        if provider is not None and len(provider) > 255:
            return json.dumps({"error": "provider exceeds 255 characters", "halt": True})

        # status enum
        if status is not None:
            valid_statuses = ["active", "inactive"]
            if status not in valid_statuses:
                return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}", "halt": True})

        # costs
        if employee_cost is not None:
            try:
                ec = float(employee_cost)
            except Exception:
                return json.dumps({"error": "employee_cost must be a number", "halt": True})
            if ec < 0:
                return json.dumps({"error": "employee_cost cannot be negative", "halt": True})
            if ec > 99999999.99:
                return json.dumps({"error": "employee_cost exceeds allowed limit", "halt": True})
        else:
            ec = None

        if employer_cost is not None:
            try:
                erc = float(employer_cost)
            except Exception:
                return json.dumps({"error": "employer_cost must be a number", "halt": True})
            if erc < 0:
                return json.dumps({"error": "employer_cost cannot be negative", "halt": True})
            if erc > 99999999.99:
                return json.dumps({"error": "employer_cost exceeds allowed limit", "halt": True})
        else:
            erc = None

        # dates (consider current values for cross-field checks)
        current_eff = row.get("effective_date")
        current_exp = row.get("expiration_date")

        try:
            eff_final = parse_date(effective_date) if effective_date else (parse_date(current_eff) if current_eff else None)
        except ValueError as ve:
            return json.dumps({"error": str(ve), "halt": True})

        exp_final_iso = None
        if expiration_date is not None:
            if expiration_date == "" or expiration_date is None:
                exp_final_iso = None
            else:
                try:
                    exp_final = parse_date(expiration_date)
                except ValueError as ve:
                    return json.dumps({"error": str(ve), "halt": True})
                exp_final_iso = exp_final.isoformat()
        else:
            exp_final_iso = current_exp  # unchanged

        # If we have both effective (possibly updated) and expiration (possibly updated), enforce order
        if eff_final and exp_final_iso:
            try:
                exp_dt = parse_date(exp_final_iso)
            except ValueError:
                # Should not happen, stored value should be valid
                return json.dumps({"error": "Stored expiration_date is invalid", "halt": True})
            if exp_dt < eff_final:
                return json.dumps({"error": "expiration_date must be on/after effective_date", "halt": True})

        # ---------- persist updates ----------
        timestamp = "2025-10-01T00:00:00"

        if plan_name is not None:
            row["plan_name"] = plan_name.strip()
        if provider is not None:
            row["provider"] = provider
        if employee_cost is not None:
            row["employee_cost"] = to_decimal_str(ec, 2)
        if employer_cost is not None:
            row["employer_cost"] = to_decimal_str(erc, 2)
        if status is not None:
            row["status"] = status
        if effective_date is not None:
            row["effective_date"] = eff_final.isoformat() if eff_final else None
        if expiration_date is not None:
            row["expiration_date"] = exp_final_iso  # may be None (cleared)

        row["updated_at"] = timestamp

        plans[str(plan_id)] = row
        data["benefits_plans"] = plans

        return json.dumps({"success": True, "message": "Benefits plan updated"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_benefits_plan",
                "description": "Update fields of an existing benefits plan (requires HR Director and Finance approvals).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "plan_id": {"type": "string", "description": "Plan ID (required)"},
                        "plan_name": {"type": "string", "description": "Updated plan name (optional)"},
                        "provider": {"type": "string", "description": "Updated provider name (optional)"},
                        "employee_cost": {"type": "number", "description": "Updated employee cost DECIMAL(10,2) (optional)"},
                        "employer_cost": {"type": "number", "description": "Updated employer cost DECIMAL(10,2) (optional)"},
                        "status": {"type": "string", "description": "Updated status: active, inactive (optional)"},
                        "effective_date": {"type": "string", "description": "Updated effective date YYYY-MM-DD (optional)"},
                        "expiration_date": {"type": "string", "description": "Updated expiration date YYYY-MM-DD (optional)"},
                        "hr_director_approval": {"type": "boolean", "description": "HR Director approval (required)"},
                        "finance_officer_approval": {"type": "boolean", "description": "Finance Officer approval (required)"}
                    },
                    "required": ["plan_id", "hr_director_approval", "finance_officer_approval"]
                }
            }
        }
