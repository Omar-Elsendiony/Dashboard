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
                "description": "Discover contract entities (subscriptions, SLA agreements). The entity to discover is decided by entity_type. Optional filters can be applied to narrow down the search results.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'subscriptions' or 'sla_agreements'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters to narrow down search results. Only exact matches are supported (AND logic for multiple filters).",
                            "properties": {
                                "subscription_id": {
                                    "type": "string",
                                    "description": "Subscription ID (for subscriptions)"
                                },
                                "client_id": {
                                    "type": "string",
                                    "description": "Client ID (for subscriptions)"
                                },
                                "tier": {
                                    "type": "string",
                                    "description": "Subscription tier: 'premium', 'standard', 'basic' (for subscriptions)"
                                },
                                "start_date": {
                                    "type": "string",
                                    "description": "Start date in YYYY-MM-DD format (for subscriptions)"
                                },
                                "end_date": {
                                    "type": "string",
                                    "description": "End date in YYYY-MM-DD format (for subscriptions)"
                                },
                                "status": {
                                    "type": "string",
                                    "description": "Status: 'active', 'expired', 'cancelled' (for subscriptions)"
                                },
                                "sla_id": {
                                    "type": "string",
                                    "description": "SLA agreement ID (for sla_agreements)"
                                },
                                "severity_level": {
                                    "type": "string",
                                    "description": "Severity level: 'P1', 'P2', 'P3', 'P4' (for sla_agreements)"
                                },
                                "response_time_minutes": {
                                    "type": "integer",
                                    "description": "Response time in minutes (for sla_agreements)"
                                },
                                "resolution_time_minutes": {
                                    "type": "integer",
                                    "description": "Resolution time in minutes (for sla_agreements)"
                                },
                                "availability_guarantee": {
                                    "type": "number",
                                    "description": "Availability guarantee percentage, e.g., 99.9 (for sla_agreements)"
                                },
                                "created_by": {
                                    "type": "string",
                                    "description": "User ID who created the SLA (for sla_agreements)"
                                },
                                "created_at": {
                                    "type": "string",
                                    "description": "Creation timestamp in YYYY-MM-DD format"
                                },
                                "updated_at": {
                                    "type": "string",
                                    "description": "Update timestamp in YYYY-MM-DD format (for subscriptions)"
                                }
                            }
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
