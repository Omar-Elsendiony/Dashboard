import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class LookupChangeControl(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover change control entities (change_requests, rollback_requests). The entity to discover is decided by entity_type.
        Optionally, filters can be applied to narrow down the search results.
        
        Supported entities:
        - change_requests: Change Request records
        - rollback_requests: Rollback Request records
        """
        if entity_type not in ["change_requests", "rollback_requests"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'change_requests' or 'rollback_requests'"
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
                    if entity_type == "change_requests":
                        id_field = "change_id"
                    else:  # rollback_requests
                        id_field = "rollback_id"
                    results.append({**entity_data, id_field: entity_id})
            else:
                if entity_type == "change_requests":
                    id_field = "change_id"
                else:  # rollback_requests
                    id_field = "rollback_id"
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
                "name": "lookup_change_control",
                "description": "Discover change control entities (change requests, rollback requests). The entity to discover is decided by entity_type. Optional filters can be applied to narrow down the search results.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'change_requests' or 'rollback_requests'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters to narrow down search results. Only exact matches are supported (AND logic for multiple filters).",
                            "properties": {
                                "change_id": {
                                    "type": "string",
                                    "description": "Change request ID (for change_requests)"
                                },
                                "change_number": {
                                    "type": "string",
                                    "description": "Change request number, e.g., CHG0001234 (for change_requests)"
                                },
                                "incident_id": {
                                    "type": "string",
                                    "description": "Associated incident ID"
                                },
                                "problem_ticket_id": {
                                    "type": "string",
                                    "description": "Associated problem ticket ID (for change_requests)"
                                },
                                "title": {
                                    "type": "string",
                                    "description": "Change/rollback title"
                                },
                                "description": {
                                    "type": "string",
                                    "description": "Change description (for change_requests)"
                                },
                                "change_type": {
                                    "type": "string",
                                    "description": "Type of change: 'standard', 'normal', 'emergency' (for change_requests)"
                                },
                                "risk_level": {
                                    "type": "string",
                                    "description": "Risk level of change: 'low', 'medium', 'high', 'critical' (for change_requests)"
                                },
                                "requested_by": {
                                    "type": "string",
                                    "description": "User ID who requested the change/rollback"
                                },
                                "approved_by": {
                                    "type": "string",
                                    "description": "User ID who approved the change (for change_requests)"
                                },
                                "status": {
                                    "type": "string",
                                    "description": "Status of the change/rollback"
                                },
                                "implementation_date": {
                                    "type": "string",
                                    "description": "Implementation date in YYYY-MM-DD format (for change_requests)"
                                },
                                "rollback_id": {
                                    "type": "string",
                                    "description": "Rollback request ID (for rollback_requests)"
                                },
                                "rollback_number": {
                                    "type": "string",
                                    "description": "Rollback request number, e.g., RBK0001234 (for rollback_requests)"
                                },
                                "rollback_reason": {
                                    "type": "string",
                                    "description": "Reason for rollback (for rollback_requests)"
                                },
                                "executed_at": {
                                    "type": "string",
                                    "description": "Execution timestamp in YYYY-MM-DD format (for rollback_requests)"
                                },
                                "created_at": {
                                    "type": "string",
                                    "description": "Creation timestamp in YYYY-MM-DD format"
                                },
                                "updated_at": {
                                    "type": "string",
                                    "description": "Update timestamp in YYYY-MM-DD format (for change_requests)"
                                }
                            }
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
