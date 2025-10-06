import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class DiscoverProducts(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover product entities.
        
        Supported entities:
        - products: Product records by product_id, product_name, product_type, version, vendor_support_id, status
        """
        if entity_type not in ["products"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'products'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get("products", {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, "product_id": str(entity_id)})
            else:
                results.append({**entity_data, "product_id": str(entity_id)})
        
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
                "name": "discover_products",
                "description": "Discover product entities. Entity types: 'products' (product records; filterable by product_id (string), product_name (string), product_type (enum: 'payment_processing', 'banking_system', 'api_gateway', 'data_integration', 'reporting_platform', 'security_service', 'backup_service', 'monitoring_tool'), version (string), vendor_support_id (string), status (enum: 'active', 'deprecated', 'maintenance'), created_at (timestamp), updated_at (timestamp)).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'products'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False. For products, filters are: product_id (string), product_name (string), product_type (enum: 'payment_processing', 'banking_system', 'api_gateway', 'data_integration', 'reporting_platform', 'security_service', 'backup_service', 'monitoring_tool'), version (string), vendor_support_id (string), status (enum: 'active', 'deprecated', 'maintenance'), created_at (timestamp), updated_at (timestamp)"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
