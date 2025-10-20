import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class FindContracts(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover contract entities (sla_agreements). The entity to discover is decided by entity_type.
        Optionally, filters can be applied to narrow down the search results.
        
        Supported entities:
        - sla_agreements: SLA Agreement records
        """
        if entity_type not in ["sla_agreements"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'sla_agreements'"
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
                    results.append({**entity_data, "sla_id": entity_id})
            else:
                results.append({**entity_data, "sla_id": entity_id})
        
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
                "name": "find_contracts",
                "description": "Discover contract entities (SLA agreements). The entity to discover is decided by entity_type. Optional filters can be applied to narrow down the search results.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'sla_agreements'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters to narrow down search results. Only exact matches are supported (AND logic for multiple filters).",
                            "properties": {
                                "sla_id": {
                                    "type": "string",
                                    "description": "SLA agreement ID"
                                },
                                "client_id": {
                                    "type": "string",
                                    "description": "Client ID"
                                },
                                "tier": {
                                    "type": "string",
                                    "description": "SLA tier: 'premium', 'standard', 'basic'"
                                },
                                "support_coverage": {
                                    "type": "string",
                                    "description": "Support coverage: '24x7', 'business_hours', 'on_call'"
                                },
                                "effective_date": {
                                    "type": "string",
                                    "description": "Effective date in YYYY-MM-DD format"
                                },
                                "expiration_date": {
                                    "type": "string",
                                    "description": "Expiration date in YYYY-MM-DD format"
                                },
                                "created_by": {
                                    "type": "string",
                                    "description": "User ID who created the SLA"
                                },
                                "status": {
                                    "type": "string",
                                    "description": "Status: 'active', 'inactive', 'expired'"
                                },
                                "created_at": {
                                    "type": "string",
                                    "description": "Creation timestamp in YYYY-MM-DD format"
                                },
                                "updated_at": {
                                    "type": "string",
                                    "description": "Update timestamp in YYYY-MM-DD format"
                                }
                            }
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
