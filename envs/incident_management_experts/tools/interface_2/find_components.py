import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class FindComponents(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover infrastructure component entities.
        
        Supported entities:
        - infrastructure_components: Infrastructure component records by component_id, product_id, component_name, component_type, environment, location, port_number, status
        """
        if entity_type not in ["infrastructure_components"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'infrastructure_components'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get("infrastructure_components", {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, "component_id": str(entity_id)})
            else:
                results.append({**entity_data, "component_id": str(entity_id)})
        
        return json.dumps({
            "success": True,
            "entity_type": entity_type,
            "count": len(results),
            "results": results
        })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "find_components",
                "description": "Discover infrastructure component entities. Entity types: 'infrastructure_components' (infrastructure component records; filterable by component_id (string), product_id (string), component_name (string), component_type (enum: 'sftp_server', 'api_endpoint', 'database', 'load_balancer', 'firewall', 'authentication_service', 'payment_gateway', 'file_storage', 'monitoring_system'), environment (enum: 'production', 'staging', 'development', 'test'), location (string), port_number (integer), status (enum: 'online', 'offline', 'maintenance', 'degraded'), created_at (timestamp), updated_at (timestamp)).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'infrastructure_components'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False. For infrastructure_components, filters are: component_id (string), product_id (string), component_name (string), component_type (enum: 'sftp_server', 'api_endpoint', 'database', 'load_balancer', 'firewall', 'authentication_service', 'payment_gateway', 'file_storage', 'monitoring_system'), environment (enum: 'production', 'staging', 'development', 'test'), location (string), port_number (integer), status (enum: 'online', 'offline', 'maintenance', 'degraded'), created_at (timestamp), updated_at (timestamp)"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
