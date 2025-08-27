# enroll_employee_benefits.py
import json
from typing import Any, Dict, Optional
from datetime import datetime, date

from tau_bench.envs.tool import Tool


class EnrollEmployeeBenefits(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        employee_id: str,
        plan_id: str,
        enrollment_date: str,
        coverage_level: str,
        employee_contribution: Optional[float] = None,
        beneficiary_name: Optional[str] = None,
        beneficiary_relationship: Optional[str] = None,
        status: str = "active",
    ) -> str:
        """
        Enroll an employee into a benefits plan.
        Returns JSON: {"enrollment_id": str, "success": True} or {"error": "...", "halt": True}
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

        # ---------- load tables ----------
        enrollments = data.get("employee_benefits", {})
        plans = data.get("benefits_plans", {})
        employees_tbl = data.get("employees") or data.get("users") or {}

        # ---------- required validations ----------
        if not employee_id:
            raise ValueError("employee_id is required")
        if not plan_id:
            raise ValueError("plan_id is required")
        if not enrollment_date:
            raise ValueError("enrollment_date is required")
        if not coverage_level:
            raise ValueError("coverage_level is required")

        # Employee existence (by key or by employee_id/user_id field)
        emp_exists = (str(employee_id) in employees_tbl) or any(
            isinstance(v, dict) and str(v.get("employee_id") or v.get("user_id")) == str(employee_id)
            for v in employees_tbl.values()
        )
        if employees_tbl and not emp_exists:
            return json.dumps({"error": f"Employee {employee_id} not found", "halt": True})

        # Plan existence
        if str(plan_id) not in plans:
            return json.dumps({"error": f"Benefits plan {plan_id} not found", "halt": True})
        plan_row = plans[str(plan_id)]

        # ---------- enums & field validations ----------
        valid_statuses = ["active", "terminated", "pending"]
        if status not in valid_statuses:
            return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}", "halt": True})

        valid_coverage = ["employee_only", "employee_spouse", "employee_children", "family"]
        if coverage_level not in valid_coverage:
            return json.dumps({"error": f"Invalid coverage_level. Must be one of {valid_coverage}", "halt": True})

        # employee_contribution (optional DECIMAL(10,2))
        if employee_contribution is not None:
            try:
                ec = float(employee_contribution)
            except Exception:
                return json.dumps({"error": "employee_contribution must be a number", "halt": True})
            if ec < 0:
                return json.dumps({"error": "employee_contribution cannot be negative", "halt": True})
            if ec > 99999999.99:
                return json.dumps({"error": "employee_contribution exceeds allowed limit", "halt": True})
        else:
            ec = None

        # Dates: enrollment within plan effective window
        try:
            enroll_dt = parse_date(enrollment_date)
        except ValueError as ve:
            return json.dumps({"error": str(ve), "halt": True})

        # Validate plan status/effective window
        plan_status = (plan_row.get("status") or "active").lower()
        if plan_status != "active":
            return json.dumps({"error": f"Plan {plan_id} is not active", "halt": True})

        # plan effective/expiration
        eff_str = plan_row.get("effective_date")
        exp_str = plan_row.get("expiration_date")  # may be None
        try:
            eff_dt = parse_date(eff_str) if eff_str else None
        except ValueError:
            return json.dumps({"error": "Stored plan effective_date is invalid", "halt": True})
        if exp_str:
            try:
                exp_dt = parse_date(exp_str)
            except ValueError:
                return json.dumps({"error": "Stored plan expiration_date is invalid", "halt": True})
        else:
            exp_dt = None

        if eff_dt and enroll_dt < eff_dt:
            return json.dumps({"error": "enrollment_date is before plan effective_date", "halt": True})
        if exp_dt and enroll_dt > exp_dt:
            return json.dumps({"error": "enrollment_date is after plan expiration_date", "halt": True})

        # Optional: prevent duplicate active enrollment for same employee/plan
        for erow in enrollments.values():
            if (
                isinstance(erow, dict)
                and str(erow.get("employee_id")) == str(employee_id)
                and str(erow.get("plan_id")) == str(plan_id)
                and (erow.get("status") or "active") == "active"
            ):
                return json.dumps({
                    "error": f"Employee {employee_id} is already actively enrolled in plan {plan_id}",
                    "halt": True
                })

        # ---------- create row ----------
        enrollment_id = generate_id(enrollments)
        timestamp = "2025-10-01T00:00:00"

        new_row = {
            "enrollment_id": enrollment_id,
            "employee_id": str(employee_id),
            "plan_id": str(plan_id),
            "enrollment_date": enroll_dt.isoformat(),
            "status": status,
            "employee_contribution": to_decimal_str(ec, 2) if ec is not None else None,
            "coverage_level": coverage_level,
            "beneficiary_name": beneficiary_name,
            "beneficiary_relationship": beneficiary_relationship,
            "created_at": timestamp,
            "updated_at": timestamp,
        }

        enrollments[enrollment_id] = new_row
        data["employee_benefits"] = enrollments

        return json.dumps({"enrollment_id": enrollment_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "enroll_employee_benefits",
                "description": "Enroll an employee into a benefits plan.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "employee_id": {"type": "string", "description": "Employee ID (required)"},
                        "plan_id": {"type": "string", "description": "Benefits plan ID (required)"},
                        "enrollment_date": {"type": "string", "description": "YYYY-MM-DD (required)"},
                        "employee_contribution": {"type": "number", "description": "Employee contribution DECIMAL(10,2) (optional)"},
                        "coverage_level": {"type": "string", "description": "employee_only, employee_spouse, employee_children, family (required)"},
                        "beneficiary_name": {"type": "string", "description": "Beneficiary name (optional)"},
                        "beneficiary_relationship": {"type": "string", "description": "Beneficiary relationship (optional)"},
                        "status": {"type": "string", "description": "active, terminated, pending (default active)"}
                    },
                    "required": ["employee_id", "plan_id", "enrollment_date", "coverage_level"]
                }
            }
        }
