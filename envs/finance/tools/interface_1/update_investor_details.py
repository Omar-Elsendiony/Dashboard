import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class update_investor_details(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        investor_id: str,
        name: str = None,
        contact_email: str = None,
        accreditation_status: str = None,
        employee_id: str = None
    ) -> str:
        users = data.get("users", {})
        investors = data.get("investors", {})

        # Validate investor exists
        if str(investor_id) not in investors:
            raise ValueError(f"Investor {investor_id} not found")

        # Retrieve current investor state
        investor = investors[str(investor_id)]

        # Update fields if provided
        if name is not None:
            investor["name"] = name
        if contact_email is not None:
            investor["contact_email"] = contact_email
        if accreditation_status is not None:
            valid_statuses = ["accredited", "non_accredited"]
            if accreditation_status not in valid_statuses:
                raise ValueError(f"Invalid accreditation status. Must be one of {valid_statuses}")
            investor["accreditation_status"] = accreditation_status
        if employee_id is not None:
            # Validate employee exists and is active
            if str(employee_id) not in users:
                raise ValueError(f"Employee {employee_id} not found")
            user = users[str(employee_id)]
            if user.get("status") != "active":
                raise ValueError(f"User {employee_id} is not active")
            investor["employee_id"] = employee_id

        # Return updated state
        return json.dumps(investor)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_investor_details",
                "description": "Update investor details; only provided fields will be changed.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {"type": "string", "description": "ID of the investor"},
                        "name": {"type": "string", "description": "New name of the investor"},
                        "contact_email": {"type": "string", "description": "New contact email of the investor"},
                        "accreditation_status": {"type": "string", "description": "New accreditation status (accredited, non_accredited)"},
                        "employee_id": {"type": "string", "description": "New employee ID representing the investor (must be an active employee)"}
                    },
                    "required": ["investor_id"]
                }
            }
        }
