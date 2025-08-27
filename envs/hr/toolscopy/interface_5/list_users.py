import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetUsers(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: Optional[str] = None,
               email: Optional[str] = None, role: Optional[str] = None,
               status: Optional[str] = None) -> str:
        
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
            results.append(user)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_users",
                "description": "Get users with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "Filter by user ID"},
                        "email": {"type": "string", "description": "Filter by email"},
                        "role": {"type": "string", "description": "Filter by role"},
                        "status": {"type": "string", "description": "Filter by status"}
                    },
                    "required": []
                }
            }
        }
