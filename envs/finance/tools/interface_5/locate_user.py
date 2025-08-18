import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class LocateUser(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: Optional[str] = None, email: Optional[str] = None,
               role: Optional[str] = None, status: Optional[str] = None,
               first_name: Optional[str] = None, last_name: Optional[str] = None) -> str:
        users = data.get("users", {})
        results = []
        
        for user in users.values():
            if user_id and user.get("user_id") != user_id:
                continue
            if email and user.get("email", "").lower() != email.lower():
                continue
            if role and user.get("role") != role:
                continue
            if status and user.get("status") != status:
                continue
            if first_name and first_name.lower() not in user.get("first_name", "").lower():
                continue
            if last_name and last_name.lower() not in user.get("last_name", "").lower():
                continue
            results.append(user)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "locate_user",
                "description": "Locate users for lookup and support",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "email": {"type": "string", "description": "Filter by email address"},
                        "role": {"type": "string", "description": "Filter by role (system_administrator, fund_manager, compliance_officer, finance_officer, trader)"},
                        "status": {"type": "string", "description": "Filter by status (active, inactive, suspended)"},
                        "first_name": {"type": "string", "description": "Filter by first name (partial match)"},
                        "last_name": {"type": "string", "description": "Filter by last name (partial match)"}
                    },
                    "required": []
                }
            }
        }
