import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class DiscoverClients(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover client entities.
        
        Supported entities:
        - clients: Client records by client_id, client_name, client_type, industry, country, status
        """
        if entity_type not in ["clients"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'clients'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get("clients", {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, "client_id": str(entity_id)})
            else:
                results.append({**entity_data, "client_id": str(entity_id)})
        
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
                "name": "discover_clients",
                "description": "Discover client entities. Entity types: 'clients' (client records; filterable by client_id (string), client_name (string), registration_number (string), contact_email (string), client_type (enum: 'enterprise', 'mid_market', 'small_business', 'startup'), industry (string), country (string), status (enum: 'active', 'inactive', 'suspended'), created_at (timestamp), updated_at (timestamp)).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'clients'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False. For clients, filters are: client_id (string), client_name (string), registration_number (string), contact_email (string), client_type (enum: 'enterprise', 'mid_market', 'small_business', 'startup'), industry (string), country (string), status (enum: 'active', 'inactive', 'suspended'), created_at (timestamp), updated_at (timestamp)"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
