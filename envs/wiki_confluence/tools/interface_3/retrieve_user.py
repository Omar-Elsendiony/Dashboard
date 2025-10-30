import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class RetrieveUser(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], identifier: str, identifier_type: Optional[str] = "user_id") -> str:
        """
        Retrieve user details by ID or email.
        """
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format"
            })
        
        users = data.get("users", {})
        
        if identifier_type == "user_id":
            if str(identifier) in users:
                user_data = users[str(identifier)].copy()
                return json.dumps({
                    "success": True,
                    "user_data": user_data
                })
            else:
                return json.dumps({
                    "success": False,
                    "error": f"User {identifier} not found"
                })
        elif identifier_type == "email":
            for user_id, user in users.items():
                if user.get("email") == identifier:
                    user_data = user.copy()
                    return json.dumps({
                        "success": True,
                        "user_data": user_data
                    })
            return json.dumps({
                "success": False,
                "error": f"User with email '{identifier}' not found"
            })
        else:
            return json.dumps({
                "success": False,
                "error": f"Invalid identifier_type '{identifier_type}'. Must be 'user_id' or 'email'"
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "retrieve_user",
                "description": "Retrieve user details by ID or email in the Confluence system. This tool fetches comprehensive user account information including user ID, email, account ID, full name, global role, and creation timestamp. Supports lookup by user ID or email address. Essential for user verification, authentication checks, profile display, and validating user existence before performing operations.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "identifier": {
                            "type": "string",
                            "description": "User identifier - either user_id or email (required)"
                        },
                        "identifier_type": {
                            "type": "string",
                            "description": "'user_id'* or 'email' (optional, * = default)",
                            "enum": ["user_id", "email"]
                        }
                    },
                    "required": ["identifier"]
                }
            }
        }
