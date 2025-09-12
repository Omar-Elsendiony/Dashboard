import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetUsers(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: Optional[str] = None, username: Optional[str] = None,
               role: Optional[str] = None, email: Optional[str] = None, status: Optional[str] = None) -> str:
        
        users = data.get("users", {})
        result = []
        
        for uid, user in users.items():
            # Apply filters
            if user_id and str(user_id) != uid:
                continue
            if username and user.get("username", "").lower() != username.lower():
                continue
            if role and user.get("role") != role:
                continue
            if email and user.get("email", "").lower() != email.lower():
                continue
            if status and user.get("status") != status:
                continue
            
            result.append({
                "user_id": uid,
                "username": user.get("username"),
                "role": user.get("role"),
                "email": user.get("email"),
                "first_name": user.get("first_name"),
                "last_name": user.get("last_name"),
                "display_name": user.get("display_name"),
                "timezone": user.get("timezone"),
                "status": user.get("status"),
                "created_at": user.get("created_at"),
                "updated_at": user.get("updated_at")
            })
        
        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_users",
                "description": "Get users matching filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "ID of the user"},
                        "username": {"type": "string", "description": "Username of the user"},
                        "role": {"type": "string", "description": "Role of the user (PlatformOwner, WikiProgramManager, User)"},
                        "email": {"type": "string", "description": "Email of the user"},
                        "status": {"type": "string", "description": "Status of the user (active, inactive, suspended)"}
                    },
                    "required": []
                }
            }
        }
