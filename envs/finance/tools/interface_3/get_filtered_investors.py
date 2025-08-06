import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class get_filtered_investors(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        investor_id: Optional[str] = None,
        employee_id: Optional[str] = None,
        name: Optional[str] = None,
        investor_type: Optional[str] = None,
        contact_email: Optional[str] = None,
        accreditation_status: Optional[str] = None
    ) -> str:
        investors = data.get("investors", {})
        results = []

        for inv in investors.values():
            if investor_id is not None and str(inv.get("investor_id")) != str(investor_id):
                continue
            if employee_id is not None and str(inv.get("employee_id")) != str(employee_id):
                continue
            if name is not None and name.lower() not in inv.get("name", "").lower():
                continue
            if investor_type is not None and inv.get("investor_type") != investor_type:
                continue
            if contact_email is not None and inv.get("contact_email", "").lower() != contact_email.lower():
                continue
            if accreditation_status is not None and inv.get("accreditation_status") != accreditation_status:
                continue

            results.append(inv)

        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_filtered_investors",
                "description": "Fetch investors with optional filters: investor_id, employee_id, name, investor_type, contact_email, accreditation_status.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {
                            "type": "string",
                            "description": "Filter by investor ID"
                        },
                        "employee_id": {
                            "type": "string",
                            "description": "Filter by employee (user) ID"
                        },
                        "name": {
                            "type": "string",
                            "description": "Partial match on investor name"
                        },
                        "investor_type": {
                            "type": "string",
                            "description": "Filter by investor type (organization, retail, high_net_worth)"
                        },
                        "contact_email": {
                            "type": "string",
                            "description": "Filter by contact email"
                        },
                        "accreditation_status": {
                            "type": "string",
                            "description": "Filter by accreditation status (accredited, non_accredited)"
                        }
                    },
                    "required": []
                }
            }
        }
