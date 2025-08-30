import json
from typing import Any, Dict
from datetime import datetime
from tau_bench.envs.tool import Tool

class CreateUser(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        first_name: str,
        last_name: str,
        email: str,
        role: str,
        timezone: str,
        phone: str = None,
        department: str = None,
        client_id: str = None,
        vendor_id: str = None,
        status: str = "active",
    ) -> str:
        users = data.setdefault("users", {})

        valid_roles = {"incident_manager","technical_support","account_manager","executive","vendor_contact","system_administrator","client_contact"}
        valid_status = {"active","inactive","on_leave"}
        if role not in valid_roles:
            return json.dumps({"success": False, "error": f"Invalid role. Must be one of {sorted(valid_roles)}"})
        if status not in valid_status:
            return json.dumps({"success": False, "error": f"Invalid status. Must be one of {sorted(valid_status)}"})

        def generate_id(table: Dict[str, Any]) -> str:
            return str(max([int(k) for k in table.keys()] + [0]) + 1)

        user_id = generate_id(users)
        ts = "2025-10-01T00:00:00"

        new_user = {
            "user_id": user_id,
            "client_id": client_id,
            "vendor_id": vendor_id,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone": phone,
            "role": role,
            "department": department,
            "timezone": timezone,
            "status": status,
            "created_at": ts,
            "updated_at": ts
        }

        users[user_id] = new_user
        return json.dumps({"user_id": user_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_user",
                "description": "Create a new user (defaults status=active) and return user_id.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "first_name": {"type": "string"},
                        "last_name": {"type": "string"},
                        "email": {"type": "string"},
                        "role": {"type": "string", "description": "incident_manager|technical_support|account_manager|executive|vendor_contact|system_administrator|client_contact"},
                        "timezone": {"type": "string"},
                        "phone": {"type": "string"},
                        "department": {"type": "string"},
                        "client_id": {"type": "string"},
                        "vendor_id": {"type": "string"},
                        "status": {"type": "string", "description": "active|inactive|on_leave (default active)"}
                    },
                    "required": ["data", "first_name", "last_name", "email", "role", "timezone"]
                }
            }
        }
