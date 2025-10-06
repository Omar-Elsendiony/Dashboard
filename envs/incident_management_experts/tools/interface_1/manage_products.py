import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class ManageProducts(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        # approval: bool,
        # For Create
        product_name: Optional[str] = None,
        product_type: Optional[str] = None,
        version: Optional[str] = None,
        vendor_support_id: Optional[str] = None,
        status: Optional[str] = "active",
        # For Update
        product_id: Optional[str] = None
    ) -> str:

        products = data.get("products", {})
        vendors = data.get("vendors", {})

        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1

        valid_types = [
            "payment_processing", "banking_system", "api_gateway",
            "data_integration", "reporting_platform", "security_service",
            "backup_service", "monitoring_tool"
        ]
        valid_status = ["active", "deprecated", "maintenance"]

        # ----- Check Approval -----
        # if not approval:
        #     return json.dumps({
        #         "success": False,
        #         "error": "Approval missing for product management action"
        #     })

        # ----- CREATE -----
        if not product_id:
            # Required fields
            if not product_name or not product_type:
                return json.dumps({
                    "success": False,
                    "error": "Missing or invalid inputs"
                })

            if product_type not in valid_types:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid product_type. Must be one of {valid_types}"
                })

            if status and status not in valid_status:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid status. Must be one of {valid_status}"
                })

            # Check product_name uniqueness
            for product in products.values():
                if product.get("product_name") == product_name:
                    return json.dumps({
                        "success": False,
                        "error": "Product name already exists"
                    })

            # Validate vendor
            if vendor_support_id:
                vendor = vendors.get(vendor_support_id)
                if not vendor or vendor.get("status") != "active":
                    return json.dumps({
                        "success": False,
                        "error": "Vendor not found or inactive"
                    })

            # Create new product
            new_id = str(generate_id(products))
            timestamp = "2025-10-01T00:00:00"

            new_product = {
                "product_id": new_id,
                "product_name": product_name,
                "product_type": product_type,
                "version": version,
                "vendor_support_id": vendor_support_id,
                "status": status,
                "created_at": timestamp
            }
            products[new_id] = new_product

            # Simulate audit record logging
            if not data.get("audit_log"):
                data["audit_log"] = []
            data["audit_log"].append({
                "action": "create_product",
                "product_id": new_id,
                "timestamp": timestamp
            })

            return json.dumps(new_product)

        # ----- UPDATE -----
        else:
            if product_id not in products:
                return json.dumps({
                    "success": False,
                    "error": "Product not found"
                })

            product = products[product_id]

            if product_name:
                # Check uniqueness
                for pid, existing in products.items():
                    if pid != product_id and existing.get("product_name") == product_name:
                        return json.dumps({
                            "success": False,
                            "error": "New product_name already exists"
                        })
                product["product_name"] = product_name

            if product_type and product_type not in valid_types:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid product_type. Must be one of {valid_types}"
                })

            if status and status not in valid_status:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid status. Must be one of {valid_status}"
                })

            if vendor_support_id:
                vendor = vendors.get(vendor_support_id)
                if not vendor or vendor.get("status") != "active":
                    return json.dumps({
                        "success": False,
                        "error": "Vendor not found or inactive"
                    })
                product["vendor_support_id"] = vendor_support_id

            # Update allowed fields
            for field, val in [
                ("product_type", product_type), ("version", version),
                ("status", status)
            ]:
                if val is not None:
                    product[field] = val

            # Simulate audit logging
            timestamp = "2025-10-01T00:00:00"
            if not data.get("audit_log"):
                data["audit_log"] = []
            data["audit_log"].append({
                "action": "update_product",
                "product_id": product_id,
                "timestamp": timestamp
            })

            return json.dumps(product)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manage_products",
                "description": (
                    "Create or update product records in the incident management system."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "product_id": {
                            "type": "string",
                            "description": "Existing product ID for updates. "
                                           "If omitted, a new product will be created."
                        },
                        "product_name": {"type": "string"},
                        "product_type": {
                            "type": "string",
                            "description": "Must be one of: payment_processing, "
                                           "banking_system, api_gateway, data_integration, "
                                           "reporting_platform, security_service, "
                                           "backup_service, monitoring_tool"
                        },
                        "version": {"type": "string"},
                        "vendor_support_id": {"type": "string"},
                        "status": {
                            "type": "string",
                            "description": "Product status. Must be one of: "
                                           "active, deprecated, maintenance"
                        }
                    },
                    "required": []
                }
            }
        }

