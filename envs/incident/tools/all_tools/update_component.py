import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdateComponent(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        component_id: str,
        product_id: str = None,
        component_name: str = None,
        component_type: str = None,   # sftp_server|api_endpoint|database|load_balancer|firewall|authentication_service|payment_gateway|file_storage|monitoring_system
        environment: str = None,      # production|staging|development|test
        location: str = None,
        port_number: int = None,
        status: str = None            # online|offline|maintenance|degraded
    ) -> str:
        try:
            comps = data.get("infrastructure_components", {})
            if component_id not in comps:
                return json.dumps({"success": False, "error": f"Component {component_id} not found"})

            valid_ct = {
                "sftp_server","api_endpoint","database","load_balancer","firewall",
                "authentication_service","payment_gateway","file_storage","monitoring_system"
            }
            valid_env = {"production","staging","development","test"}
            valid_status = {"online","offline","maintenance","degraded"}

            if component_type and component_type not in valid_ct:
                return json.dumps({"success": False, "error": f"Invalid component_type. Must be one of {sorted(valid_ct)}"})
            if environment and environment not in valid_env:
                return json.dumps({"success": False, "error": f"Invalid environment. Must be one of {sorted(valid_env)}"})
            if status and status not in valid_status:
                return json.dumps({"success": False, "error": f"Invalid status. Must be one of {sorted(valid_status)}"})
            if port_number is not None and isinstance(port_number, int) and port_number < 0:
                return json.dumps({"success": False, "error": "port_number must be non-negative"})

            c = comps[component_id]
            if product_id is not None: c["product_id"] = product_id
            if component_name is not None: c["component_name"] = component_name
            if component_type is not None: c["component_type"] = component_type
            if environment is not None: c["environment"] = environment
            if location is not None: c["location"] = location
            if port_number is not None: c["port_number"] = port_number
            if status is not None: c["status"] = status

            c["updated_at"] = "2025-10-01T00:00:00"
            return json.dumps(c)
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

    @staticmethod
    def get_info()->Dict[str,Any]:
        return{
            "type":"function",
            "function":{
                "name":"update_component",
                "description":"Update an infrastructure component; sets updated_at",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "component_id":{"type":"string"},
                        "product_id":{"type":"string"},
                        "component_name":{"type":"string"},
                        "component_type":{"type":"string","description":"sftp_server|api_endpoint|database|load_balancer|firewall|authentication_service|payment_gateway|file_storage|monitoring_system"},
                        "environment":{"type":"string","description":"production|staging|development|test"},
                        "location":{"type":"string"},
                        "port_number":{"type":"integer"},
                        "status":{"type":"string","description":"online|offline|maintenance|degraded"}
                    },
                    "required":["component_id"]
                }
            }
        }
