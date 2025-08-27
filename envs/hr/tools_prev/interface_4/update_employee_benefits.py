# update_employee_benefits.py
import json
from typing import Any, Dict, Optional

from tau_bench.envs.tool import Tool


class UpdateEmployeeBenefits(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        enrollment_id: str,
        employee_contribution: Optional[float] = None,
        coverage_level: Optional[str] = None,
        beneficiary_name: Optional[str] = None,
        beneficiary_relationship: Optional[str] = None,
        status: Optional[str] = None,
    ) -> str:
        """
        Update an existing employee benefits enrollment.
        Returns JSON: {"success": True, "message": "Employee benefits updated"}
        or {"error": "...", "halt": True}
        """

        # ---------- helpers ----------
        def to_decimal_str(val: float, places: int = 2) -> str:
            return f"{round(float(val), places):.{places}f}"

        # ---------- load ----------
        enrollments = data.get("employee_benefits", {})

        # ---------- validations ----------
        if not enrollment_id:
            raise ValueError("enrollment_id is required")
        if str(enrollment_id) not in enrollments:
            return json.dumps({"error": f"Enrollment {enrollment_id} not found", "halt": True})

        # If nothing to update
        if all(
            v is None
            for v in [
                employee_contribution,
                coverage_level,
                beneficiary_name,
                beneficiary_relationship,
                status,
            ]
        ):
            return json.dumps({"success": True, "message": "No changes provided"})

        # Validate enums
        if status is not None:
            valid_statuses = ["active", "terminated", "pending"]
            if status not in valid_statuses:
                return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}", "halt": True})

        if coverage_level is not None:
            valid_coverage = ["employee_only", "employee_spouse", "employee_children", "family"]
            if coverage_level not in valid_coverage:
                return json.dumps({"error": f"Invalid coverage_level. Must be one of {valid_coverage}", "halt": True})

        # Validate lengths
        if beneficiary_name is not None and len(beneficiary_name) > 255:
            return json.dumps({"error": "beneficiary_name exceeds 255 characters", "halt": True})
        if beneficiary_relationship is not None and len(beneficiary_relationship) > 100:
            return json.dumps({"error": "beneficiary_relationship exceeds 100 characters", "halt": True})

        # Validate contribution
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

        # ---------- persist ----------
        row = enrollments[str(enrollment_id)]
        timestamp = "2025-10-01T00:00:00"

        if employee_contribution is not None:
            row["employee_contribution"] = to_decimal_str(ec, 2)
        if coverage_level is not None:
            row["coverage_level"] = coverage_level
        if beneficiary_name is not None:
            row["beneficiary_name"] = beneficiary_name
        if beneficiary_relationship is not None:
            row["beneficiary_relationship"] = beneficiary_relationship
        if status is not None:
            row["status"] = status

        row["updated_at"] = timestamp

        enrollments[str(enrollment_id)] = row
        data["employee_benefits"] = enrollments

        return json.dumps({"success": True, "message": "Employee benefits updated"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_employee_benefits",
                "description": "Update an existing employee benefits enrollment.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "enrollment_id": {"type": "string", "description": "Enrollment ID (required)"},
                        "employee_contribution": {"type": "number", "description": "Updated employee contribution DECIMAL(10,2) (optional)"},
                        "coverage_level": {"type": "string", "description": "Updated coverage level: employee_only, employee_spouse, employee_children, family (optional)"},
                        "beneficiary_name": {"type": "string", "description": "Updated beneficiary name (optional, max 255 chars)"},
                        "beneficiary_relationship": {"type": "string", "description": "Updated beneficiary relationship (optional, max 100 chars)"},
                        "status": {"type": "string", "description": "Updated status: active, terminated, pending (optional)"}
                    },
                    "required": ["enrollment_id"]
                }
            }
        }
