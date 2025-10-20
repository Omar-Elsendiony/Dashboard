import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class DiscoverCoordination(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover coordination entities (escalations, bridges, bridge_participants). The entity to discover is decided by entity_type.
        Optionally, filters can be applied to narrow down the search results.
        
        Supported entities:
        - escalations: Escalation records
        - bridges: Bridge records
        - bridge_participants: Bridge Participant records
        """
        if entity_type not in ["escalations", "bridges", "bridge_participants"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'escalations', 'bridges', or 'bridge_participants'"
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
                    if entity_type == "escalations":
                        id_field = "escalation_id"
                    elif entity_type == "bridges":
                        id_field = "bridge_id"
                    else:  # bridge_participants
                        id_field = "participant_id"
                    results.append({**entity_data, id_field: entity_id})
            else:
                if entity_type == "escalations":
                    id_field = "escalation_id"
                elif entity_type == "bridges":
                    id_field = "bridge_id"
                else:  # bridge_participants
                    id_field = "participant_id"
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
                "name": "discover_coordination",
                "description": "Discover coordination entities (escalations, bridges, bridge participants). The entity to discover is decided by entity_type. Optional filters can be applied to narrow down the search results.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'escalations', 'bridges', or 'bridge_participants'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters to narrow down search results. Only exact matches are supported (AND logic for multiple filters).",
                            "properties": {
                                "escalation_id": {
                                    "type": "string",
                                    "description": "Escalation ID (for escalations)"
                                },
                                "incident_id": {
                                    "type": "string",
                                    "description": "Associated incident ID"
                                },
                                "escalated_from": {
                                    "type": "string",
                                    "description": "User ID who requested escalation (for escalations)"
                                },
                                "escalated_to": {
                                    "type": "string",
                                    "description": "User ID receiving escalation (for escalations)"
                                },
                                "escalation_reason": {
                                    "type": "string",
                                    "description": "Reason for escalation (for escalations)"
                                },
                                "approver": {
                                    "type": "string",
                                    "description": "User ID who approved/denied the escalation (for escalations)"
                                },
                                "status": {
                                    "type": "string",
                                    "description": "Status: 'pending', 'approved', 'denied', 'cancelled'"
                                },
                                "requested_at": {
                                    "type": "string",
                                    "description": "Request timestamp in YYYY-MM-DD format (for escalations)"
                                },
                                "responded_at": {
                                    "type": "string",
                                    "description": "Response timestamp in YYYY-MM-DD format (for escalations)"
                                },
                                "bridge_id": {
                                    "type": "string",
                                    "description": "Bridge ID"
                                },
                                "bridge_number": {
                                    "type": "string",
                                    "description": "Bridge number, e.g., BRG0001234 (for bridges)"
                                },
                                "bridge_type": {
                                    "type": "string",
                                    "description": "Bridge type: 'major_incident', 'coordination', 'technical' (for bridges)"
                                },
                                "bridge_host": {
                                    "type": "string",
                                    "description": "User ID hosting the bridge (for bridges)"
                                },
                                "start_time": {
                                    "type": "string",
                                    "description": "Start timestamp in YYYY-MM-DD format (for bridges)"
                                },
                                "end_time": {
                                    "type": "string",
                                    "description": "End timestamp in YYYY-MM-DD format (for bridges)"
                                },
                                "participant_id": {
                                    "type": "string",
                                    "description": "Participant ID (for bridge_participants)"
                                },
                                "user_id": {
                                    "type": "string",
                                    "description": "User ID of the participant (for bridge_participants)"
                                },
                                "role_in_bridge": {
                                    "type": "string",
                                    "description": "Role in bridge: 'host', 'technical_support', 'account_manager', 'executive' (for bridge_participants)"
                                },
                                "joined_at": {
                                    "type": "string",
                                    "description": "Join timestamp in YYYY-MM-DD format (for bridge_participants)"
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
