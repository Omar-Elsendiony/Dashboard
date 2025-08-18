import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class FindInvestorUser(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_user_id: Optional[str] = None, investor_email: Optional[str] = None,
               investor_role: Optional[str] = None, investor_status: Optional[str] = None,
               investor_first_name: Optional[str] = None, investor_last_name: Optional[str] = None) -> str:
        users = data.get("users", {})
        results = []
        
        for user in users.values():
            if investor_user_id and user.get("investor_user_id") != investor_user_id:
                continue
            if investor_email and user.get("investor_email", "").lower() != investor_email.lower():
                continue
            if investor_role and user.get("investor_role") != investor_role:
                continue
            if investor_status and user.get("investor_status") != investor_status:
                continue
            if investor_first_name and investor_first_name.lower() not in user.get("investor_first_name", "").lower():
                continue
            if investor_last_name and investor_last_name.lower() not in user.get("investor_last_name", "").lower():
                continue
            results.append(user)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "investor_name": "find_user",
                "description": "Find users for lookup and support",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_email": {"type": "string", "description": "Filter by investor_email investor_address"},
                        "investor_role": {"type": "string", "description": "Filter by investor_role (system_administrator, fund_manager, compliance_officer, finance_officer, trader)"},
                        "investor_status": {"type": "string", "description": "Filter by investor_status (active, inactive, suspended)"},
                        "investor_first_name": {"type": "string", "description": "Filter by first investor_name (partial match)"},
                        "investor_last_name": {"type": "string", "description": "Filter by last investor_name (partial match)"}
                    },
                    "required": []
                }
            }
        }
