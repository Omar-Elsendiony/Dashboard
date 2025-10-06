import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class RegisterEscalations(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover escalation entities.
        
        Supported entities:
        - escalations: Escalation records
        """
        if entity_type not in ["escalations"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'escalations'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get("escalations", {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, "escalation_id": str(entity_id)})
            else:
                results.append({**entity_data, "escalation_id": str(entity_id)})
        
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
                "name": "register_escalations",
                "description": "Discover escalation entities. Entity types: 'escalations' (escalation records; filterable by escalation_id (string), escalation_code (string), incident_id (string), escalated_by_id (string), escalated_to_id (string), escalation_reason (enum: 'sla_breach', 'severity_increase', 'resource_unavailable', 'executive_request', 'client_demand'), escalation_level (enum: 'technical', 'management', 'executive', 'vendor'), escalated_at (timestamp), acknowledged_at (timestamp), resolved_at (timestamp), status (enum: 'open', 'acknowledged', 'resolved'), created_at (timestamp)).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'escalations'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False. For escalations, filters are: escalation_id (string), escalation_code (string), incident_id (string), escalated_by_id (string), escalated_to_id (string), escalation_reason (enum: 'sla_breach', 'severity_increase', 'resource_unavailable', 'executive_request', 'client_demand'), escalation_level (enum: 'technical', 'management', 'executive', 'vendor'), escalated_at (timestamp), acknowledged_at (timestamp), resolved_at (timestamp), status (enum: 'open', 'acknowledged', 'resolved'), created_at (timestamp)"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }