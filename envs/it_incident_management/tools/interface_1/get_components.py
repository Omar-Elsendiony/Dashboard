import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetComponents(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        component_id: str = None,
        product_id: str = None,
        component_name: str = None,
        component_name_contains: str = None,
        component_type: str = None,
        environment: str = None,
        status: str = None,
        location: str = None
    ) -> str:
        components = data.get("infrastructure_components", {})
        results = []

        for comp in components.values():
            if component_id and comp.get("component_id") != component_id:
                continue
            if product_id and comp.get("product_id") != product_id:
                continue
            if component_name and comp.get("component_name") != component_name:
                continue
            if component_name_contains and component_name_contains.lower() not in (comp.get("component_name","").lower()):
                continue
            if component_type and comp.get("component_type") != component_type:
                continue
            if environment and comp.get("environment") != environment:
                continue
            if status and comp.get("status") != status:
                continue
            if location and comp.get("location") != location:
                continue
            results.append(comp)

        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_components",
                "description": "Unified get/list for infrastructure components with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "component_id": {"type": "string"},
                        "product_id": {"type": "string"},
                        "component_name": {"type": "string", "description": "Exact name match"},
                        "component_name_contains": {"type": "string", "description": "Case-insensitive contains"},
                        "component_type": {"type": "string", "description": "sftp_server|api_endpoint|database|load_balancer|firewall|authentication_service|payment_gateway|file_storage|monitoring_system"},
                        "environment": {"type": "string", "description": "production|staging|development|test"},
                        "status": {"type": "string", "description": "online|offline|maintenance|degraded"},
                        "location": {"type": "string"}
                    },
                    "required": []
                }
            }
        }
