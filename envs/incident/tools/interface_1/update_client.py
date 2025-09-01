import json
from typing import Any, Dict
from datetime import datetime
from tau_bench.envs.tool import Tool

class UpdateClient(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        client_id: str,
        client_name: str = None,
        registration_number: str = None,
        contact_email: str = None,
        client_type: str = None,
        industry: str = None,
        country: str = None,
        status: str = None,
    ) -> str:
        clients = data.get("clients", {})
        if client_id not in clients:
            return json.dumps({"success": False, "error": f"Client {client_id} not found"})

        # Validate enums if provided
        valid_types = {"enterprise", "mid_market", "small_business", "startup"}
        valid_status = {"active", "inactive", "suspended"}
        if client_type and client_type not in valid_types:
            return json.dumps({"success": False, "error": f"Invalid client_type. Must be one of {sorted(valid_types)}"})
        if status and status not in valid_status:
            return json.dumps({"success": False, "error": f"Invalid status. Must be one of {sorted(valid_status)}"})

        c = clients[client_id]
        if client_name is not None: c["client_name"] = client_name
        if registration_number is not None: c["registration_number"] = registration_number
        if contact_email is not None: c["contact_email"] = contact_email
        if client_type is not None: c["client_type"] = client_type
        if industry is not None: c["industry"] = industry
        if country is not None: c["country"] = country
        if status is not None: c["status"] = status

        c["updated_at"] = "2025-09-02T23:59:59"
        return json.dumps({"success": True, "data": c})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_client",
                "description": "Update an existing client record and set updated_at.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "client_id": {"type": "string"},
                        "client_name": {"type": "string"},
                        "registration_number": {"type": "string"},
                        "contact_email": {"type": "string"},
                        "client_type": {"type": "string", "description": "enterprise|mid_market|small_business|startup"},
                        "industry": {"type": "string"},
                        "country": {"type": "string"},
                        "status": {"type": "string", "description": "active|inactive|suspended"}
                    },
                    "required": ["data", "client_id"]
                }
            }
        }
