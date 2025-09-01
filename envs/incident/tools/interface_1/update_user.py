import json
from typing import Any, Dict
from datetime import datetime
from tau_bench.envs.tool import Tool

class UpdateUser(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        user_id: str,
        role: str = None,
        status: str = None,
        first_name: str = None,
        last_name: str = None,
        phone: str = None,
        department: str = None,
        client_id: str = None,
        vendor_id: str = None,
        timezone: str = None,
    ) -> str:
        users = data.get("users", {})
        if user_id not in users:
            return json.dumps({"success": False, "error": f"User {user_id} not found"})

        valid_roles = {"incident_manager","technical_support","account_manager","executive","vendor_contact","system_administrator","client_contact"}
        valid_status = {"active","inactive","on_leave"}
        if role and role not in valid_roles:
            return json.dumps({"success": False, "error": f"Invalid role. Must be one of {sorted(valid_roles)}"})
        if status and status not in valid_status:
            return json.dumps({"success": False, "error": f"Invalid status. Must be one of {sorted(valid_status)}"})

        u = users[user_id]
        if role is not None: u["role"] = role
        if status is not None: u["status"] = status
        if first_name is not None: u["first_name"] = first_name
        if last_name is not None: u["last_name"] = last_name
        if phone is not None: u["phone"] = phone
        if department is not None: u["department"] = department
        if client_id is not None: u["client_id"] = client_id
        if vendor_id is not None: u["vendor_id"] = vendor_id
        if timezone is not None: u["timezone"] = timezone

        u["updated_at"] = "2025-09-02T23:59:59"
        return json.dumps(u)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_user",
                "description": "Update user fields; if role provided, ensure it’s a valid enum. Sets updated_at.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string"},
                        "role": {"type": "string", "description": "Valid role enum"},
                        "status": {"type": "string", "description": "active|inactive|on_leave"},
                        "first_name": {"type": "string"},
                        "last_name": {"type": "string"},
                        "phone": {"type": "string"},
                        "department": {"type": "string"},
                        "client_id": {"type": "string"},
                        "vendor_id": {"type": "string"},
                        "timezone": {"type": "string"}
                    },
                    "required": ["data", "user_id"]
                }
            }
        }
