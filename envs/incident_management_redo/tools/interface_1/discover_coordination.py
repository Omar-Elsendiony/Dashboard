import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class DiscoverCoordination(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover coordination entities (escalations, bridges, bridge_participants). 
        The entity to discover is decided by entity_type.
        Optionally, filters can be applied to narrow down the search results.
        
        Supported entities:
        - escalations: Escalation records
        - bridges: Bridge records
        - bridge_participants: Bridge Participant records
        """
        valid_types = ["escalations", "bridges", "bridge_participants"]
        if entity_type not in valid_types:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be one of {valid_types}"
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
                    id_field_map = {
                        "escalations": "escalation_id",
                        "bridges": "bridge_id",
                        "bridge_participants": "participant_id"
                    }
                    id_field = id_field_map[entity_type]
                    results.append({**entity_data, id_field: entity_id})
            else:
                id_field_map = {
                    "escalations": "escalation_id",
                    "bridges": "bridge_id",
                    "bridge_participants": "participant_id"
                }
                id_field = id_field_map[entity_type]
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
                "description": "Discover coordination entities (escalations, bridges, bridge participants). The entity to discover is decided by entity_type. Optional filters can be applied to narrow down the search results. Entity types: 'escalations' (escalation records; filterable by escalation_id (string), incident_id (string), escalated_from (string), escalated_to (string), escalation_level (enum: 'L1_to_L2', 'L2_to_L3', 'L3_to_management', 'management_to_executive'), escalation_reason (text), status (enum: 'pending', 'approved', 'denied', 'cancelled'), requested_at (timestamp), responded_at (timestamp)), 'bridges' (bridge records; filterable by bridge_id (string), bridge_number (string), incident_id (string), bridge_type (enum: 'major_incident', 'coordination', 'technical'), bridge_host (string), start_time (timestamp), end_time (timestamp), status (enum: 'active', 'closed'), created_at (timestamp)), 'bridge_participants' (bridge participant records; filterable by participant_id (string), bridge_id (string), user_id (string), role_in_bridge (enum: 'host', 'technical_support', 'account_manager', 'vendor', 'executive'), joined_at (timestamp)).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'escalations', 'bridges', or 'bridge_participants'",
                            "enum": ["escalations", "bridges", "bridge_participants"]
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False. For escalations: escalation_id, incident_id, escalated_from, escalated_to, escalation_level, escalation_reason, status, requested_at, responded_at. For bridges: bridge_id, bridge_number, incident_id, bridge_type, bridge_host, start_time, end_time, status, created_at. For bridge_participants: participant_id, bridge_id, user_id, role_in_bridge, joined_at"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }

