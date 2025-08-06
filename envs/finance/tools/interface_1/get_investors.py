import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

import json
from typing import Any, Dict, Optional, List

class get_investors(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        investor_id: Optional[str] = None,
        employee_id: Optional[str] = None,
        investor_type: Optional[str] = None,
        accreditation_status: Optional[str] = None,
        name: Optional[str] = None,
        contact_email: Optional[str] = None
    ) -> str:
        """
        Retrieve a list of investors, optionally filtering by investor_id, employee_id,
        investor_type, accreditation_status, name (partial match), and contact_email.
        """
        investors = data.get("investors", {})
        results: List[Dict[str, Any]] = []

        for investor in investors.values():
            if investor_id and str(investor.get("investor_id")) != investor_id:
                continue
            if employee_id and str(investor.get("employee_id")) != employee_id:
                continue
            if investor_type and investor.get("investor_type") != investor_type:
                continue
            if accreditation_status and investor.get("accreditation_status") != accreditation_status:
                continue
            if name and name.lower() not in investor.get("name", "").lower():
                continue
            if contact_email and investor.get("contact_email") != contact_email:
                continue

            results.append(investor)

        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_investors",
                "description": "Get a list of investors with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {"type": "string", "description": "Filter by investor ID"},
                        "employee_id": {"type": "string", "description": "Filter by employee ID"},
                        "investor_type": {"type": "string", "description": "Filter by investor type (organization, retail, high_net_worth)"},
                        "accreditation_status": {"type": "string", "description": "Filter by accreditation status (accredited, non_accredited)"},
                        "name": {"type": "string", "description": "Filter by investor name (partial match)"},
                        "contact_email": {"type": "string", "description": "Filter by investor contact email"}
                    },
                    "required": []
                }
            }
        }
