import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class FindSubscriptionAgreements(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover subscription and SLA agreement entities.
        
        Supported entities:
        - client_subscriptions: Client subscription records by subscription_id, client_id, product_id, subscription_type, start_date, end_date, sla_tier, rto_hours, status
        - sla_agreements: SLA agreement records by sla_id, subscription_id, severity_level, response_time_minutes, resolution_time_hours, availability_percentage
        """
        if entity_type not in ["client_subscriptions", "sla_agreements"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'client_subscriptions' or 'sla_agreements'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get(entity_type, {})
        
        # Determine the ID field based on entity type
        id_field = "subscription_id" if entity_type == "client_subscriptions" else "sla_id"
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, id_field: str(entity_id)})
            else:
                results.append({**entity_data, id_field: str(entity_id)})
        
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
                "name": "find_subscription_agreements",
                "description": "Discover subscription and SLA agreement entities. Entity types: 'client_subscriptions' (client subscription records; filterable by subscription_id (string), client_id (string), product_id (string), subscription_type (enum: 'full_service', 'limited_service', 'trial', 'custom'), start_date (date YYYY-MM-DD), end_date (date YYYY-MM-DD), sla_tier (enum: 'premium', 'standard', 'basic'), rto_hours (integer), status (enum: 'active', 'expired', 'cancelled', 'suspended'), created_at (timestamp), updated_at (timestamp)); 'sla_agreements' (SLA agreement records; filterable by sla_id (string), subscription_id (string), severity_level (enum: 'P1', 'P2', 'P3', 'P4'), response_time_minutes (integer), resolution_time_hours (integer), availability_percentage (decimal), created_at (timestamp)).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'client_subscriptions' or 'sla_agreements'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False. For client_subscriptions, filters are: subscription_id (string), client_id (string), product_id (string), subscription_type (enum: 'full_service', 'limited_service', 'trial', 'custom'), start_date (date YYYY-MM-DD), end_date (date YYYY-MM-DD), sla_tier (enum: 'premium', 'standard', 'basic'), rto_hours (integer), status (enum: 'active', 'expired', 'cancelled', 'suspended'), created_at (timestamp), updated_at (timestamp). For sla_agreements, filters are: sla_id (string), subscription_id (string), severity_level (enum: 'P1', 'P2', 'P3', 'P4'), response_time_minutes (integer), resolution_time_hours (integer), availability_percentage (decimal), created_at (timestamp)"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }