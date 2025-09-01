import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class RetrieveClients(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        client_id: str = None,
        registration_number: str = None,
        contact_email: str = None,
        client_name_contains: str = None,
        client_type: str = None,
        status: str = None,
    ) -> str:
        clients = data.get("clients", {})
        results = []

        # Validate enums if provided
        valid_types = {"enterprise", "mid_market", "small_business", "startup"}
        valid_status = {"active", "inactive", "suspended"}
        if client_type and client_type not in valid_types:
            return json.dumps({"error": f"Invalid client_type. Must be one of {sorted(valid_types)}"})
        if status and status not in valid_status:
            return json.dumps({"error": f"Invalid status. Must be one of {sorted(valid_status)}"})

        for c in clients.values():
            if client_id and c.get("client_id") != client_id:
                continue
            if registration_number and c.get("registration_number") != registration_number:
                continue
            if contact_email and c.get("contact_email") != contact_email:
                continue
            if client_type and c.get("client_type") != client_type:
                continue
            if status and c.get("status") != status:
                continue
            if client_name_contains:
                if not isinstance(c.get("client_name", ""), str):
                    continue
                if client_name_contains.lower() not in c.get("client_name", "").lower():
                    continue
            results.append(c)

        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "retrieve_clients",
                "description": "Unified get/list for clients with optional filters.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "client_id": {"type": "string", "description": "Exact client ID filter"},
                        "registration_number": {"type": "string", "description": "Exact registration number"},
                        "contact_email": {"type": "string", "description": "Exact contact email"},
                        "client_name_contains": {"type": "string", "description": "Case-insensitive substring on client_name"},
                        "client_type": {"type": "string", "description": "enterprise|mid_market|small_business|startup"},
                        "status": {"type": "string", "description": "active|inactive|suspended"}
                    },
                    "required": []
                }
            }
        }
