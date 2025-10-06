import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class GetVendors(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover vendor entities.
        
        Supported entities:
        - vendors: Vendor records by vendor_id, vendor_name, vendor_type, contact_email, status
        """
        if entity_type not in ["vendors"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'vendors'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get("vendors", {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, "vendor_id": str(entity_id)})
            else:
                results.append({**entity_data, "vendor_id": str(entity_id)})
        
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
                "name": "get_vendors",
                "description": "Discover vendor entities. Entity types: 'vendors' (vendor records; filterable by vendor_id (string), vendor_name (string), vendor_type (enum: 'cloud_provider', 'payment_processor', 'software_vendor', 'infrastructure_provider', 'security_vendor'), contact_email (string), contact_phone (string), status (enum: 'active', 'inactive', 'suspended'), created_at (timestamp)).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'vendors'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False. For vendors, filters are: vendor_id (string), vendor_name (string), vendor_type (enum: 'cloud_provider', 'payment_processor', 'software_vendor', 'infrastructure_provider', 'security_vendor'), contact_email (string), contact_phone (string), status (enum: 'active', 'inactive', 'suspended'), created_at (timestamp)"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
