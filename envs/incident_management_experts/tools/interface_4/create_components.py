import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class CreateComponents(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        # approval: bool,
        # For Create
        component_name: Optional[str] = None,
        component_type: Optional[str] = None,
        environment: Optional[str] = None,
        product_id: Optional[str] = None,
        location: Optional[str] = None,
        port_number: Optional[int] = None,
        status: Optional[str] = "online",
        # For Update
        component_id: Optional[str] = None
    ) -> str:

        components = data.get("components", {})
        products = data.get("products", {})

        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1

        valid_types = [
            "sftp_server", "api_endpoint", "database", "load_balancer",
            "firewall", "authentication_service", "payment_gateway",
            "file_storage", "monitoring_system"
        ]
        valid_envs = ["production", "staging", "development", "test"]
        valid_status = ["online", "offline", "maintenance", "degraded"]

        # ----- Check Approval -----
        # if not approval:
        #     return json.dumps({
        #         "success": False,
        #         "error": "Approval missing for component management action"
        #     })

        # ----- CREATE -----
        if not component_id:
            if not component_name or not component_type or not environment:
                return json.dumps({
                    "success": False,
                    "error": "Missing or invalid inputs"
                })

            if component_type not in valid_types:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid component_type. Must be one of {valid_types}"
                })

            if environment not in valid_envs:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid environment. Must be one of {valid_envs}"
                })

            if status and status not in valid_status:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid status. Must be one of {valid_status}"
                })

            # Validate product if provided
            if product_id:
                product = products.get(product_id)
                if not product or product.get("status") != "active":
                    return json.dumps({
                        "success": False,
                        "error": "Product not found or inactive"
                    })

            # Ensure component_name uniqueness within product_id scope
            for comp in components.values():
                if comp.get("product_id") == product_id and comp.get("component_name") == component_name:
                    return json.dumps({
                        "success": False,
                        "error": "Component name already exists within product"
                    })

            # Create new component
            new_id = str(generate_id(components))
            timestamp = "2025-10-01T00:00:00"

            new_component = {
                "component_id": new_id,
                "component_name": component_name,
                "component_type": component_type,
                "environment": environment,
                "product_id": product_id,
                "location": location,
                "port_number": port_number,
                "status": status,
                "created_at": timestamp
            }
            components[new_id] = new_component

            # Audit logging
            if not data.get("audit_log"):
                data["audit_log"] = []
            data["audit_log"].append({
                "action": "create_component",
                "component_id": new_id,
                "timestamp": timestamp
            })

            return json.dumps(new_component)

        # ----- UPDATE -----
        else:
            if component_id not in components:
                return json.dumps({
                    "success": False,
                    "error": "Component not found"
                })

            component = components[component_id]

            if component_name:
                # Ensure uniqueness within product scope
                for cid, existing in components.items():
                    if cid != component_id and existing.get("product_id") == (product_id or component["product_id"]) and existing.get("component_name") == component_name:
                        return json.dumps({
                            "success": False,
                            "error": "New component_name already exists within product"
                        })
                component["component_name"] = component_name

            if component_type and component_type not in valid_types:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid component_type. Must be one of {valid_types}"
                })

            if environment and environment not in valid_envs:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid environment. Must be one of {valid_envs}"
                })

            if status and status not in valid_status:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid status. Must be one of {valid_status}"
                })

            if product_id:
                product = products.get(product_id)
                if not product or product.get("status") != "active":
                    return json.dumps({
                        "success": False,
                        "error": "Product not found or inactive"
                    })
                component["product_id"] = product_id

            # Apply updates
            for field, val in [
                ("component_type", component_type), ("environment", environment),
                ("location", location), ("port_number", port_number),
                ("status", status)
            ]:
                if val is not None:
                    component[field] = val

            # Audit logging
            timestamp = "2025-10-01T00:00:00"
            if not data.get("audit_log"):
                data["audit_log"] = []
            data["audit_log"].append({
                "action": "update_component",
                "component_id": component_id,
                "timestamp": timestamp
            })

            return json.dumps(component)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_components",
                "description": (
                    "Create or update infrastructure component records in the incident management system."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "component_id": {
                            "type": "string",
                            "description": "Existing component ID for updates. "
                                           "If omitted, a new component will be created."
                        },
                        "component_name": {"type": "string"},
                        "component_type": {
                            "type": "string",
                            "description": "Must be one of: sftp_server, api_endpoint, database, "
                                           "load_balancer, firewall, authentication_service, "
                                           "payment_gateway, file_storage, monitoring_system"
                        },
                        "environment": {
                            "type": "string",
                            "description": "Must be one of: production, staging, development, test"
                        },
                        "product_id": {"type": "string"},
                        "location": {"type": "string"},
                        "port_number": {"type": "number"},
                        "status": {
                            "type": "string",
                            "description": "Must be one of: online, offline, maintenance, degraded"
                        }
                    },
                    "required": []
                }
            }
        }

