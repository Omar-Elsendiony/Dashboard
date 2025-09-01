import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateVendor(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        vendor_id: str,
        vendor_name: str = None,
        vendor_type: str = None,   # cloud_provider|payment_processor|software_vendor|infrastructure_provider|security_vendor
        contact_email: str = None,
        contact_phone: str = None,
        status: str = None         # active|inactive|suspended
    ) -> str:
        try:
            vendors = data.get("vendors", {})
            if vendor_id not in vendors:
                return json.dumps({"success": False, "error": f"Vendor {vendor_id} not found"})

            valid_vendor_types = {
                "cloud_provider","payment_processor","software_vendor","infrastructure_provider","security_vendor"
            }
            valid_status = {"active","inactive","suspended"}

            if vendor_type and vendor_type not in valid_vendor_types:
                return json.dumps({"success": False, "error": f"Invalid vendor_type. Must be one of {sorted(valid_vendor_types)}"})

            if status and status not in valid_status:
                return json.dumps({"success": False, "error": f"Invalid status. Must be one of {sorted(valid_status)}"})

            v = vendors[vendor_id]
            if vendor_name is not None: v["vendor_name"] = vendor_name
            if vendor_type is not None: v["vendor_type"] = vendor_type
            if contact_email is not None: v["contact_email"] = contact_email
            if contact_phone is not None: v["contact_phone"] = contact_phone
            if status is not None: v["status"] = status

            # Table has no updated_at; do not set it.
            return json.dumps(v)
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return{
            "type":"function",
            "function":{
                "name":"update_vendor",
                "description":"Update a vendor record with partial fields",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "vendor_id":{"type":"string"},
                        "vendor_name":{"type":"string"},
                        "vendor_type":{"type":"string","description":"cloud_provider|payment_processor|software_vendor|infrastructure_provider|security_vendor"},
                        "contact_email":{"type":"string"},
                        "contact_phone":{"type":"string"},
                        "status":{"type":"string","description":"active|inactive|suspended"}
                    },
                    "required":["vendor_id"]
                }
            }
        }
