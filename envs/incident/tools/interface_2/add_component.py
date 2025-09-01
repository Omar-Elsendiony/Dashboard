import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class AddComponent(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        component_name: str,
        component_type: str,
        environment: str,
        status: str,
        product_id: str = None,
        location: str = None,
        port_number: int = None
    ) -> str:
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        try:
            components = data.setdefault("infrastructure_components", {})

            valid_types = [
                "sftp_server","api_endpoint","database","load_balancer","firewall",
                "authentication_service","payment_gateway","file_storage","monitoring_system"
            ]
            if component_type not in valid_types:
                return json.dumps({"success": False, "error": f"Invalid component_type. Must be one of {valid_types}"})

            valid_env = ["production","staging","development","test"]
            if environment not in valid_env:
                return json.dumps({"success": False, "error": f"Invalid environment. Must be one of {valid_env}"})

            valid_status = ["online","offline","maintenance","degraded"]
            if status not in valid_status:
                return json.dumps({"success": False, "error": f"Invalid status. Must be one of {valid_status}"})

            component_id = generate_id(components)
            timestamp = "2025-10-01T00:00:00"

            new_component = {
                "component_id": component_id,
                "product_id": product_id,
                "component_name": component_name,
                "component_type": component_type,
                "environment": environment,
                "location": location,
                "port_number": port_number,
                "status": status,
                "created_at": timestamp,
                "updated_at": timestamp
            }

            components[component_id] = new_component
            return json.dumps({"component_id": component_id, "success": True})
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_component",
                "description": "Create a new infrastructure component",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "component_name": {"type": "string"},
                        "component_type": {"type": "string", "description": "sftp_server|api_endpoint|database|load_balancer|firewall|authentication_service|payment_gateway|file_storage|monitoring_system"},
                        "environment": {"type": "string", "description": "production|staging|development|test"},
                        "status": {"type": "string", "description": "online|offline|maintenance|degraded"},
                        "product_id": {"type": "string"},
                        "location": {"type": "string"},
                        "port_number": {"type": "integer"}
                    },
                    "required": ["component_name","component_type","environment","status"]
                }
            }
        }
