import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class DiscoverContracts(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover contract entities (subscriptions, sla_agreements). The entity to discover is decided by entity_type.
        Optionally, filters can be applied to narrow down the search results.
        
        Supported entities:
        - subscriptions: Subscription records
        - sla_agreements: SLA Agreement records
        """
        if entity_type not in ["subscriptions", "sla_agreements"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'subscriptions' or 'sla_agreements'"
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
                    if entity_type == "subscriptions":
                        id_field = "subscription_id"
                    else:  # sla_agreements
                        id_field = "sla_id"
                    results.append({**entity_data, id_field: entity_id})
            else:
                if entity_type == "subscriptions":
                    id_field = "subscription_id"
                else:  # sla_agreements
                    id_field = "sla_id"
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
                "name": "discover_contracts",
                "description": "Discover contract entities (subscriptions, SLA agreements). The entity to discover is decided by entity_type. Optional filters can be applied to narrow down the search results. Entity types: 'subscriptions' (subscription records; filterable by subscription_id (string), client_id (string), tier (enum: 'premium', 'standard', 'basic'), start_date (date), end_date (date), status (enum: 'active', 'expired', 'cancelled'), created_at (timestamp), updated_at (timestamp)), 'sla_agreements' (SLA agreement records; filterable by sla_id (string), subscription_id (string), severity_level (enum: 'P1', 'P2', 'P3', 'P4'), response_time_minutes (integer), resolution_time_minutes (integer), availability_guarantee (decimal), created_by (string), created_at (timestamp)).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'subscriptions' or 'sla_agreements'",
                            "enum": ["subscriptions", "sla_agreements"]
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False. For subscriptions: subscription_id, client_id, tier, start_date, end_date, status, created_at, updated_at. For sla_agreements: sla_id, subscription_id, severity_level, response_time_minutes, resolution_time_minutes, availability_guarantee, created_by, created_at"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }

