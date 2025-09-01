import json
import re
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class FetchUsers(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        user_id: str = None,
        email: str = None,
        role: str = None,
        department: str = None,
        client_id: str = None,
        vendor_id: str = None,
        status: str = None,
        first_name: str = None,
        last_name: str = None,
        phone: str = None,  # phone filter (digits-only, suffix match)
    ) -> str:
        users = data.get("users", {})
        results = []

        valid_roles = {
            "incident_manager","technical_support","account_manager",
            "executive","vendor_contact","system_administrator","client_contact"
        }
        valid_status = {"active","inactive","on_leave"}
        if role and role not in valid_roles:
            return json.dumps({"error": f"Invalid role. Must be one of {sorted(valid_roles)}"})
        if status and status not in valid_status:
            return json.dumps({"error": f"Invalid status. Must be one of {sorted(valid_status)}"})

        def normalize_phone(p) -> str:
            if p is None:
                return ""
            return re.sub(r"\D", "", str(p))

        target_phone = normalize_phone(phone)
        target_email = email.lower() if email is not None else None

        for u in users.values():
            if user_id and u.get("user_id") != user_id:
                continue
            if target_email:
                user_email = (u.get("email") or "").lower()
                if user_email != target_email:
                    continue
            if role and u.get("role") != role:
                continue
            if department and u.get("department") != department:
                continue
            if client_id and u.get("client_id") != client_id:
                continue
            if vendor_id and u.get("vendor_id") != vendor_id:
                continue
            if status and u.get("status") != status:
                continue
            if first_name and u.get("first_name") != first_name:
                continue
            if last_name and u.get("last_name") != last_name:
                continue
            if target_phone:
                # Support both "phone" and "phone_number" in stored data
                user_phone = normalize_phone(u.get("phone") or u.get("phone_number"))
                if not user_phone.endswith(target_phone):
                    continue

            results.append(u)

        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "fetch_users",
                "description": "Unified get/list for users with optional filters. Email is case-insensitive; phone uses digits-only suffix match.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string"},
                        "email": {
                            "type": "string",
                            "description": "Filter by email address (case-insensitive)"
                        },
                        "role": {
                            "type": "string",
                            "description": "incident_manager|technical_support|account_manager|executive|vendor_contact|system_administrator|client_contact"
                        },
                        "department": {"type": "string"},
                        "client_id": {"type": "string"},
                        "vendor_id": {"type": "string"},
                        "status": {"type": "string", "description": "active|inactive|on_leave"},
                        "first_name": {"type": "string"},
                        "last_name": {"type": "string"},
                        "phone": {
                            "type": "string",
                            "description": "Filter by phone; formatting ignored; digits-only suffix match supported"
                        }
                    },
                    "required": []
                }
            }
        }
