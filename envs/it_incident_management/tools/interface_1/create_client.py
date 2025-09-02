import json
from typing import Any, Dict
from datetime import datetime
from tau_bench.envs.tool import Tool

class CreateClient(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        client_name: str,
        registration_number: str,
        contact_email: str,
        client_type: str,
        industry: str = None,
        country: str = None,
        status: str = "active",
    ) -> str:
        clients = data.setdefault("clients", {})

        # Basic validations
        valid_types = {"enterprise", "mid_market", "small_business", "startup"}
        valid_status = {"active", "inactive", "suspended"}
        if client_type not in valid_types:
            return json.dumps({"success": False, "error": f"Invalid client_type. Must be one of {sorted(valid_types)}"})
        if status not in valid_status:
            return json.dumps({"success": False, "error": f"Invalid status. Must be one of {sorted(valid_status)}"})

        # ID generator
        def generate_id(table: Dict[str, Any]) -> str:
            return str(max([int(k) for k in table.keys()] + [0]) + 1)

        client_id = generate_id(clients)
        ts = "2025-09-02T23:59:59"

        new_client = {
            "client_id": client_id,
            "client_name": client_name,
            "registration_number": registration_number,
            "contact_email": contact_email,
            "client_type": client_type,
            "industry": industry,
            "country": country,
            "status": status,
            "created_at": ts,
            "updated_at": ts,
        }

        clients[client_id] = new_client
        return json.dumps({"success": True, "client_id": client_id})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_client",
                "description": "Create a new client record (defaults status=active).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "client_name": {"type": "string"},
                        "registration_number": {"type": "string"},
                        "contact_email": {"type": "string"},
                        "client_type": {"type": "string", "description": "enterprise|mid_market|small_business|startup"},
                        "industry": {"type": "string"},
                        "country": {"type": "string"},
                        "status": {"type": "string", "description": "active|inactive|suspended (default active)"}
                    },
                    "required": ["client_name", "registration_number", "contact_email", "client_type"]
                }
            }
        }
