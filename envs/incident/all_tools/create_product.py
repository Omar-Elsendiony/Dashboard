import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateProduct(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        product_name: str,
        product_type: str = None,
        version: str = None,
        vendor_support_id: str = None,
        internal_team_lead_id: str = None,
        status: str = "active"
    ) -> str:
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        try:
            products = data.setdefault("products", {})

            # Basic validations (enum-style where applicable)
            valid_types = [
                "payment_processing","banking_system","api_gateway","data_integration",
                "reporting_platform","security_service","backup_service","monitoring_tool"
            ]
            if product_type is not None and product_type not in valid_types:
                return json.dumps({"success": False, "error": f"Invalid product_type. Must be one of {valid_types}"})

            valid_status = ["active","deprecated","maintenance"]
            if status not in valid_status:
                return json.dumps({"success": False, "error": f"Invalid status. Must be one of {valid_status}"})

            product_id = generate_id(products)
            timestamp = "2025-10-01T00:00:00"

            new_product = {
                "product_id": product_id,
                "product_name": product_name,
                "product_type": product_type,
                "version":  version,
                "vendor_support_id": vendor_support_id,
                "internal_team_lead_id": internal_team_lead_id,
                "status": status,
                "created_at": timestamp,
                "updated_at": timestamp
            }

            products[product_id] = new_product
            return json.dumps({"product_id": product_id, "success": True})
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_product",
                "description": "Create a new product",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "product_name": {"type": "string", "description": "Name of the product"},
                        "product_type": {"type": "string", "description": "payment_processing|banking_system|api_gateway|data_integration|reporting_platform|security_service|backup_service|monitoring_tool"},
                        "version": {"type": "string"},
                        "vendor_support_id": {"type": "string"},
                        "internal_team_lead_id": {"type": "string"},
                        "status": {"type": "string", "description": "active|deprecated|maintenance (default active)"}
                    },
                    "required": ["product_name"]
                }
            }
        }
