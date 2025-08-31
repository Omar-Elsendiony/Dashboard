import json
from typing import Any, Dict
from datetime import datetime
from tau_bench.envs.tool import Tool

class CreateVendor(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        vendor_name: str,
        vendor_type: str,
        contact_email: str,
        contact_phone: str,
        status: str = "active",
    ) -> str:
        vendors = data.setdefault("vendors", {})

        valid_types = {"cloud_provider","payment_processor","software_vendor","infrastructure_provider","security_vendor"}
        valid_status = {"active","inactive","suspended"}
        if vendor_type not in valid_types:
            return json.dumps({"success": False, "error": f"Invalid vendor_type. Must be one of {sorted(valid_types)}"})
        if status not in valid_status:
            return json.dumps({"success": False, "error": f"Invalid status. Must be one of {sorted(valid_status)}"})

        def generate_id(table: Dict[str, Any]) -> str:
            return str(max([int(k) for k in table.keys()] + [0]) + 1)

        vendor_id = generate_id(vendors)
        ts = "2025-10-01T00:00:00"

        new_vendor = {
            "vendor_id": vendor_id,
            "vendor_name": vendor_name,
            "vendor_type": vendor_type,
            "contact_email": contact_email,
            "contact_phone": contact_phone,
            "status": status,
            "created_at": ts
        }

        vendors[vendor_id] = new_vendor
        return json.dumps({"vendor_id": vendor_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_vendor",
                "description": "Create a new vendor (defaults status=active) and return vendor_id.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "vendor_name": {"type": "string"},
                        "vendor_type": {"type": "string", "description": "cloud_provider|payment_processor|software_vendor|infrastructure_provider|security_vendor"},
                        "contact_email": {"type": "string"},
                        "contact_phone": {"type": "string"},
                        "status": {"type": "string", "description": "active|inactive|suspended (default active)"}
                    },
                    "required": ["data", "vendor_name", "vendor_type", "contact_email", "contact_phone"]
                }
            }
        }
