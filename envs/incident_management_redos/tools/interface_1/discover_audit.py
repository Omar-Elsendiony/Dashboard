import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class DiscoverAudit(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover audit entities (audit_trails). The entity to discover is decided by entity_type.
        Optionally, filters can be applied to narrow down the search results.
        
        Supported entities:
        - audit_trails: Audit Trail records
        """
        if entity_type not in ["audit_trails"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'audit_trails'"
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
                    results.append({**entity_data, "audit_id": entity_id})
            else:
                results.append({**entity_data, "audit_id": entity_id})
        
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
                "name": "discover_audit",
                "description": "Discover audit entities (audit trails). The entity to discover is decided by entity_type. Optional filters can be applied to narrow down the search results.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'audit_trails'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters to narrow down search results. Only exact matches are supported (AND logic for multiple filters).",
                            "properties": {
                                "audit_id": {
                                    "type": "string",
                                    "description": "Audit trail ID"
                                },
                                "reference_id": {
                                    "type": "string",
                                    "description": "ID of the record that was changed"
                                },
                                "reference_type": {
                                    "type": "string",
                                    "description": "Type of record: 'user', 'client', 'sla', 'ci', 'incident', 'escalation', 'bridge', 'change', 'rollback', 'work_order', 'problem', 'incident_ci', 'problem_ci', 'client_ci'"
                                },
                                "action": {
                                    "type": "string",
                                    "description": "Action performed: 'create', 'update'"
                                },
                                "user_id": {
                                    "type": "string",
                                    "description": "User ID who performed the action"
                                },
                                "field_name": {
                                    "type": "string",
                                    "description": "Name of the field that was changed"
                                },
                                "old_value": {
                                    "type": "string",
                                    "description": "Previous value before change"
                                },
                                "new_value": {
                                    "type": "string",
                                    "description": "New value after change"
                                },
                                "created_at": {
                                    "type": "string",
                                    "description": "Creation timestamp in YYYY-MM-DD format"
                                }
                            }
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
