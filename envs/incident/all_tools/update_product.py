import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdateProduct(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        product_id: str,
        product_name: str = None,
        product_type: str = None,   # payment_processing|banking_system|api_gateway|data_integration|reporting_platform|security_service|backup_service|monitoring_tool
        version: str = None,
        vendor_support_id: str = None,
        internal_team_lead_id: str = None,
        status: str = None          # active|deprecated|maintenance
    ) -> str:
        try:
            products = data.get("products", {})
            if product_id not in products:
                return json.dumps({"success": False, "error": f"Product {product_id} not found"})

            valid_types = {
                "payment_processing","banking_system","api_gateway","data_integration","reporting_platform",
                "security_service","backup_service","monitoring_tool"
            }
            valid_status = {"active","deprecated","maintenance"}

            if product_type and product_type not in valid_types:
                return json.dumps({"success": False, "error": f"Invalid product_type. Must be one of {sorted(valid_types)}"})
            if status and status not in valid_status:
                return json.dumps({"success": False, "error": f"Invalid status. Must be one of {sorted(valid_status)}"})

            p = products[product_id]
            if product_name is not None: p["product_name"] = product_name
            if product_type is not None: p["product_type"] = product_type
            if version is not None: p["version"] = version
            if vendor_support_id is not None: p["vendor_support_id"] = vendor_support_id
            if internal_team_lead_id is not None: p["internal_team_lead_id"] = internal_team_lead_id
            if status is not None: p["status"] = status

            p["updated_at"] = "2025-10-01T00:00:00"
            return json.dumps(p)
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

    @staticmethod
    def get_info()->Dict[str,Any]:
        return{
            "type":"function",
            "function":{
                "name":"update_product",
                "description":"Update a product; sets updated_at",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "product_id":{"type":"string"},
                        "product_name":{"type":"string"},
                        "product_type":{"type":"string","description":"payment_processing|banking_system|api_gateway|data_integration|reporting_platform|security_service|backup_service|monitoring_tool"},
                        "version":{"type":"string"},
                        "vendor_support_id":{"type":"string"},
                        "internal_team_lead_id":{"type":"string"},
                        "status":{"type":"string","description":"active|deprecated|maintenance"}
                    },
                    "required":["product_id"]
                }
            }
        }
