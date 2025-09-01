import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class FetchProducts(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        product_id: str = None,
        product_name: str = None,
        product_name_contains: str = None,
        product_type: str = None,
        vendor_support_id: str = None,
        status: str = None
    ) -> str:
        products = data.get("products", {})
        results = []

        for prod in products.values():
            if product_id and prod.get("product_id") != product_id:
                continue
            if product_name and prod.get("product_name") != product_name:
                continue
            if product_name_contains and product_name_contains.lower() not in (prod.get("product_name", "").lower()):
                continue
            if product_type and prod.get("product_type") != product_type:
                continue
            if vendor_support_id and prod.get("vendor_support_id") != vendor_support_id:
                continue
            if status and prod.get("status") != status:
                continue
            results.append(prod)

        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "fetch_products",
                "description": "Unified get/list for products with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "product_id": {"type": "string"},
                        "product_name": {"type": "string", "description": "Exact name match"},
                        "product_name_contains": {"type": "string", "description": "Case-insensitive contains"},
                        "product_type": {
                            "type": "string",
                            "description": "payment_processing|banking_system|api_gateway|data_integration|reporting_platform|security_service|backup_service|monitoring_tool"
                        },
                        "vendor_support_id": {"type": "string"},
                        "status": {"type": "string", "description": "active|deprecated|maintenance"}
                    },
                    "required": []
                }
            }
        }
