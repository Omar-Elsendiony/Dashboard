import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ListVendors(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        vendor_id: str = None,
        vendor_name: str = None,
        vendor_name_contains: str = None,
        vendor_type: str = None,
        status: str = None,
    ) -> str:
        vendors = data.get("vendors", {})
        results = []

        valid_types = {"cloud_provider","payment_processor","software_vendor","infrastructure_provider","security_vendor"}
        valid_status = {"active","inactive","suspended"}
        if vendor_type and vendor_type not in valid_types:
            return json.dumps({"success": False, "error": f"Invalid vendor_type. Must be one of {sorted(valid_types)}"})
        if status and status not in valid_status:
            return json.dumps({"success": False, "error": f"Invalid status. Must be one of {sorted(valid_status)}"})

        for v in vendors.values():
            if vendor_id and v.get("vendor_id") != vendor_id:
                continue
            if vendor_name and v.get("vendor_name") != vendor_name:
                continue
            if vendor_type and v.get("vendor_type") != vendor_type:
                continue
            if status and v.get("status") != status:
                continue
            if vendor_name_contains:
                if not isinstance(v.get("vendor_name", ""), str):
                    continue
                if vendor_name_contains.lower() not in v.get("vendor_name", "").lower():
                    continue
            results.append(v)

        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_vendors",
                "description": "Unified get/list for vendors with optional filters.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "vendor_id": {"type": "string"},
                        "vendor_name": {"type": "string", "description": "Exact name"},
                        "vendor_name_contains": {"type": "string", "description": "Case-insensitive substring match"},
                        "vendor_type": {"type": "string", "description": "cloud_provider|payment_processor|software_vendor|infrastructure_provider|security_vendor"},
                        "status": {"type": "string", "description": "active|inactive|suspended"}
                    },
                    "required": ["data"]
                }
            }
        }
