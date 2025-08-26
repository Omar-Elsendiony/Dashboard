# create_benefits_plan.py
import json
from typing import Any, Dict, Optional
from datetime import datetime, date

from tau_bench.envs.tool import Tool


class CreateBenefitsPlan(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        plan_name: str,
        plan_type: str,
        effective_date: str,
        provider: Optional[str] = None,
        employee_cost: Optional[float] = None,
        employer_cost: Optional[float] = None,
        expiration_date: Optional[str] = None,
        hr_director_approval: Optional[bool] = None,
        finance_officer_approval: Optional[bool] = None,
    ) -> str:
        """
        Create a benefits plan record in data["benefits_plans"].
        Returns JSON: {"plan_id": str, "success": True} or {"error": "...", "halt": True}
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
                try:
                    return datetime.strptime(d, "%Y-%m-%d").date()
                except Exception:
                    raise ValueError("Dates must be ISO format YYYY-MM-DD")

        def to_decimal_str(val: float, places: int = 2) -> str:
            return f"{round(float(val), places):.{places}f}"

        # ---------- load table ----------
        plans = data.get("benefits_plans", {})

        # ---------- validations: required ----------
        if not plan_name or not str(plan_name).strip():
            raise ValueError("plan_name is required")
        if not plan_type:
            raise ValueError("plan_type is required")
        if not effective_date:
            raise ValueError("effective_date is required")

        # Approvals: require both for plan creation (financial & policy control)
        if hr_director_approval is None or finance_officer_approval is None:
            return json.dumps({
                "error": "HR Director and Finance Officer approvals are required to create a benefits plan",
                "halt": True
            })
        if not hr_director_approval or not finance_officer_approval:
            return json.dumps({
                "error": "Approval denied: both HR Director and Finance Officer must approve",
                "halt": True
            })

        # ---------- validate enums and fields ----------
        valid_types = [
            "health_insurance", "dental", "vision", "life_insurance",
            "disability", "retirement_401k", "pto", "flexible_spending"
        ]
        if plan_type not in valid_types:
            return json.dumps({"error": f"Invalid plan_type. Must be one of {valid_types}", "halt": True})

        # Costs (optional, but if provided must be >= 0 and fit DECIMAL(10,2))
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

        # Dates
        try:
            eff = parse_date(effective_date)
        except ValueError as ve:
            return json.dumps({"error": str(ve), "halt": True})

        exp_iso = None
        if expiration_date:
            try:
                exp = parse_date(expiration_date)
            except ValueError as ve:
                return json.dumps({"error": str(ve), "halt": True})
            if exp < eff:
                return json.dumps({"error": "expiration_date must be on/after effective_date", "halt": True})
            exp_iso = exp.isoformat()

        # Provider length (optional)
        if provider is not None and len(provider) > 255:
            return json.dumps({"error": "provider exceeds 255 characters", "halt": True})

        # ---------- create row ----------
        plan_id = generate_id(plans)
        timestamp = "2025-10-01T00:00:00"

        new_row = {
            "plan_id": plan_id,
            "plan_name": plan_name.strip(),
            "plan_type": plan_type,
            "provider": provider,
            "employee_cost": to_decimal_str(ec, 2) if ec is not None else None,
            "employer_cost": to_decimal_str(erc, 2) if erc is not None else None,
            "status": "active",
            "effective_date": eff.isoformat(),
            "expiration_date": exp_iso,
            "created_at": timestamp,
            "updated_at": timestamp,
        }

        plans[plan_id] = new_row
        data["benefits_plans"] = plans

        return json.dumps({"plan_id": plan_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_benefits_plan",
                "description": "Create a new benefits plan (requires HR Director and Finance approvals).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "plan_name": {"type": "string", "description": "Plan name (required)"},
                        "plan_type": {"type": "string", "description": "One of: health_insurance, dental, vision, life_insurance, disability, retirement_401k, pto, flexible_spending"},
                        "provider": {"type": "string", "description": "Provider name (optional)"},
                        "employee_cost": {"type": "number", "description": "Employee cost DECIMAL(10,2) (optional)"},
                        "employer_cost": {"type": "number", "description": "Employer cost DECIMAL(10,2) (optional)"},
                        "effective_date": {"type": "string", "description": "Effective date YYYY-MM-DD (required)"},
                        "expiration_date": {"type": "string", "description": "Expiration date YYYY-MM-DD (optional)"},
                        "hr_director_approval": {"type": "boolean", "description": "HR Director approval (required)"},
                        "finance_officer_approval": {"type": "boolean", "description": "Finance Officer approval (required)"}
                    },
                    "required": ["plan_name", "plan_type", "effective_date", "hr_director_approval", "finance_officer_approval"]
                }
            }
        }
