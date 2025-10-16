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
                "description": "Discover asset entities (products, configuration items). The entity to discover is decided by entity_type. Optional filters can be applied to narrow down the search results.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'products' or 'configuration_items'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters to narrow down search results. Only exact matches are supported (AND logic for multiple filters).",
                            "properties": {
                                "product_id": {
                                    "type": "string",
                                    "description": "Product ID (for products)"
                                },
                                "product_name": {
                                    "type": "string",
                                    "description": "Product name (for products)"
                                },
                                "product_code": {
                                    "type": "string",
                                    "description": "Product code (for products)"
                                },
                                "description": {
                                    "type": "string",
                                    "description": "Product description (for products)"
                                },
                                "status": {
                                    "type": "string",
                                    "description": "Status: 'active', 'deprecated', 'retired' (for products)"
                                },
                                "ci_id": {
                                    "type": "string",
                                    "description": "Configuration Item ID (for configuration_items)"
                                },
                                "ci_name": {
                                    "type": "string",
                                    "description": "Configuration Item name (for configuration_items)"
                                },
                                "ci_type": {
                                    "type": "string",
                                    "description": "CI type: 'server', 'application', 'database', 'network', 'storage', 'service' (for configuration_items)"
                                },
                                "environment": {
                                    "type": "string",
                                    "description": "Environment: 'production', 'staging', 'development', 'testing' (for configuration_items)"
                                },
                                "location": {
                                    "type": "string",
                                    "description": "Physical or logical location (for configuration_items)"
                                },
                                "operational_status": {
                                    "type": "string",
                                    "description": "Operational status: 'operational', 'degraded', 'down', 'maintenance' (for configuration_items)"
                                },
                                "created_at": {
                                    "type": "string",
                                    "description": "Creation timestamp in YYYY-MM-DD format"
                                },
                                "updated_at": {
                                    "type": "string",
                                    "description": "Update timestamp in YYYY-MM-DD format (for configuration_items)"
                                }
                            }
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
