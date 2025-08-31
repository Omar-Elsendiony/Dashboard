import json
import re
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
        contact_email: str = None,   # new: case-insensitive exact match
        contact_phone: str = None,   # new: digits-only, suffix match
    ) -> str:
        vendors = data.get("vendors", {})
        results = []

        valid_types = {"cloud_provider","payment_processor","software_vendor","infrastructure_provider","security_vendor"}
        valid_status = {"active","inactive","suspended"}
        if vendor_type and vendor_type not in valid_types:
            return json.dumps({"success": False, "error": f"Invalid vendor_type. Must be one of {sorted(valid_types)}"})
        if status and status not in valid_status:
            return json.dumps({"success": False, "error": f"Invalid status. Must be one of {sorted(valid_status)}"})

        def normalize_phone(p) -> str:
            if p is None:
                return ""
            return re.sub(r"\D", "", str(p))

        target_phone = normalize_phone(contact_phone)
        target_email = contact_email.lower() if contact_email is not None else None

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
                vn = v.get("vendor_name", "")
                if not isinstance(vn, str) or vendor_name_contains.lower() not in vn.lower():
                    continue
            if target_email:
                v_email = (v.get("contact_email") or "").lower()
                if v_email != target_email:
                    continue
            if target_phone:
                # Support both "contact_phone" and generic "phone" fields
                v_phone = normalize_phone(v.get("contact_phone") or v.get("phone"))
                if not v_phone.endswith(target_phone):
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
                        "vendor_type": {
                            "type": "string",
                            "description": "cloud_provider|payment_processor|software_vendor|infrastructure_provider|security_vendor"
                        },
                        "status": {"type": "string", "description": "active|inactive|suspended"},
                        "contact_email": {
                            "type": "string",
                            "description": "Filter by contact email (case-insensitive exact match)"
                        },
                        "contact_phone": {
                            "type": "string",
                            "description": "Filter by phone; formatting ignored; digits-only suffix match supported"
                        }
                    },
                    "required": []
                }
            }
        }
