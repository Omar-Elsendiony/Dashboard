import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class DiscoverAssets(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover asset entities (products, configuration_items). The entity to discover is decided by entity_type.
        Optionally, filters can be applied to narrow down the search results.
        
        Supported entities:
        - products: Product records
        - configuration_items: Configuration Item (CI) records
        """
        if entity_type not in ["products", "configuration_items"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'products' or 'configuration_items'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get(entity_type, {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    # Add appropriate ID field based on entity type
                    if entity_type == "products":
                        id_field = "product_id"
                    else:  # configuration_items
                        id_field = "ci_id"
                    results.append({**entity_data, id_field: entity_id})
            else:
                if entity_type == "products":
                    id_field = "product_id"
                else:  # configuration_items
                    id_field = "ci_id"
                results.append({**entity_data, id_field: entity_id})
        
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
                "name": "discover_assets",
                "description": "Discover asset entities (products, configuration items). The entity to discover is decided by entity_type. Optional filters can be applied to narrow down the search results. Entity types: 'products' (product records; filterable by product_id (string), product_name (string), product_code (string), description (text), status (enum: 'active', 'deprecated', 'retired'), created_at (timestamp)), 'configuration_items' (CI records; filterable by ci_id (string), ci_name (string), product_id (string), ci_type (enum: 'server', 'application', 'database', 'network', 'storage', 'service'), environment (enum: 'production', 'staging', 'development', 'testing'), location (string), operational_status (enum: 'operational', 'degraded', 'down', 'maintenance'), created_at (timestamp), updated_at (timestamp)).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'products' or 'configuration_items'",
                            "enum": ["products", "configuration_items"]
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False. For products: product_id, product_name, product_code, description, status, created_at. For configuration_items: ci_id, ci_name, product_id, ci_type, environment, location, operational_status, created_at, updated_at"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }

