import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class CreateUsers(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        # approval: bool,
        # For Create
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        email: Optional[str] = None,
        role: Optional[str] = None,
        timezone: Optional[str] = None,
        phone: Optional[str] = None,
        department: Optional[str] = None,
        client_id: Optional[str] = None,
        vendor_id: Optional[str] = None,
        status: Optional[str] = "active",
        # For Update
        user_id: Optional[str] = None
    ) -> str:

        users = data.get("users", {})
        clients = data.get("clients", {})
        vendors = data.get("vendors", {})

        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1

        valid_roles = [
            "incident_manager", "technical_support", "account_manager",
            "executive", "vendor_contact", "system_administrator",
            "client_contact"
        ]
        valid_status = ["active", "inactive", "on_leave"]

        # ----- Check Approval -----
        # if not approval:
        #     return json.dumps({
        #         "success": False,
        #         "error": "Approval missing for user management action"
        #     })

        # ----- CREATE -----
        if not user_id:
            # Required fields
            if not first_name or not last_name or not email or not role or not timezone:
                return json.dumps({
                    "success": False,
                    "error": "Missing or invalid inputs"
                })

            if role not in valid_roles:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid role. Must be one of {valid_roles}"
                })

            if status and status not in valid_status:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid status. Must be one of {valid_status}"
                })

            # Check email uniqueness
            for user in users.values():
                if user.get("email") == email:
                    return json.dumps({
                        "success": False,
                        "error": "Email already exists"
                    })

            # Validate client
            if client_id:
                client = clients.get(client_id)
                if not client or client.get("status") != "active":
                    return json.dumps({
                        "success": False,
                        "error": "Client not found or inactive"
                    })

            # Validate vendor
            if vendor_id:
                vendor = vendors.get(vendor_id)
                if not vendor or vendor.get("status") != "active":
                    return json.dumps({
                        "success": False,
                        "error": "Vendor not found or inactive"
                    })

            # Create new user
            new_id = str(generate_id(users))
            timestamp = "2025-10-01T00:00:00"

            new_user = {
                "user_id": new_id,
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "role": role,
                "timezone": timezone,
                "phone": phone,
                "department": department,
                "client_id": client_id,
                "vendor_id": vendor_id,
                "status": status,
                "created_at": timestamp
            }
            users[new_id] = new_user

            # Simulate audit record logging
            if not data.get("audit_log"):
                data["audit_log"] = []
            data["audit_log"].append({
                "action": "create_user",
                "user_id": new_id,
                "timestamp": timestamp
            })

            return json.dumps(new_user)

        # ----- UPDATE -----
        else:
            if user_id not in users:
                return json.dumps({
                    "success": False,
                    "error": "User not found"
                })

            user = users[user_id]

            if email:
                # Check uniqueness
                for uid, existing in users.items():
                    if uid != user_id and existing.get("email") == email:
                        return json.dumps({
                            "success": False,
                            "error": "New email already exists"
                        })
                user["email"] = email

            if role and role not in valid_roles:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid role. Must be one of {valid_roles}"
                })

            if status and status not in valid_status:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid status. Must be one of {valid_status}"
                })

            # Validate client
            if client_id:
                client = clients.get(client_id)
                if not client or client.get("status") != "active":
                    return json.dumps({
                        "success": False,
                        "error": "Client not found or inactive"
                    })
                user["client_id"] = client_id

            # Validate vendor
            if vendor_id:
                vendor = vendors.get(vendor_id)
                if not vendor or vendor.get("status") != "active":
                    return json.dumps({
                        "success": False,
                        "error": "Vendor not found or inactive"
                    })
                user["vendor_id"] = vendor_id

            # Update allowed fields
            for field, val in [
                ("first_name", first_name), ("last_name", last_name),
                ("phone", phone), ("role", role),
                ("department", department), ("timezone", timezone),
                ("status", status)
            ]:
                if val is not None:
                    user[field] = val

            # Simulate audit logging
            timestamp = "2025-10-01T00:00:00"
            if not data.get("audit_log"):
                data["audit_log"] = []
            data["audit_log"].append({
                "action": "update_user",
                "user_id": user_id,
                "timestamp": timestamp
            })

            return json.dumps(user)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_users",
                "description": (
                    "Create or update user accounts in the incident management system. "
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "Existing user ID for updates. "
                                           "If omitted, a new user will be created."
                        },
                        "first_name": {"type": "string"},
                        "last_name": {"type": "string"},
                        "email": {"type": "string"},
                        "phone": {"type": "string"},
                        "role": {
                            "type": "string",
                            "description": "Must be one of: incident_manager, technical_support, "
                                           "account_manager, executive, vendor_contact, "
                                           "system_administrator, client_contact"
                        },
                        "department": {"type": "string"},
                        "client_id": {"type": "string"},
                        "vendor_id": {"type": "string"},
                        "timezone": {"type": "string"},
                        "status": {
                            "type": "string",
                            "description": "User status. Must be one of: active, inactive, on_leave"
                        }
                    }
                }
            }
        }

