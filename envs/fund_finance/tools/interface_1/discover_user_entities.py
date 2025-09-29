import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class DiscoverUserEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover user entities.
        
        Supported entities:
        - users: User records by user_id, first_name, last_name, email, role, timezone, status
        """
        if entity_type not in ["users"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'users'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get("users", {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, "user_id": str(entity_id)})
            else:
                results.append({**entity_data, "user_id": str(entity_id)})
        
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
                "name": "discover_user_entities",
                "description": "Discover user entities. Entity types: 'users' (user records; filterable by user_id (string), first_name (string), last_name (string), email (string), role (enum: 'system_administrator', 'fund_manager', 'compliance_officer', 'finance_officer', 'trader'), timezone (string), status (enum: 'active', 'inactive', 'suspended'), created_at (timestamp), updated_at (timestamp)).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'users'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False. For users, filters are: user_id (string), first_name (string), last_name (string), email (string), role (enum: 'system_administrator', 'fund_manager', 'compliance_officer', 'finance_officer', 'trader'), timezone (string), status (enum: 'active', 'inactive', 'suspended'), created_at (timestamp), updated_at (timestamp)"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
