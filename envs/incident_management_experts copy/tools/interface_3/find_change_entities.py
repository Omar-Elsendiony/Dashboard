import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class FindChangeEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover change and rollback request entities.
        
        Supported entities:
        - change_requests: Change request records
        - rollback_requests: Rollback request records
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
        
        id_field = "change_id" if entity_type == "change_requests" else "rollback_id"
        
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
                "name": "find_change_entities",
                "description": "Discover change and rollback request entities. Entity types: 'change_requests' (change request records; filterable by change_id (string), change_code (string), incident_id (string), title (string), change_type (enum: 'emergency', 'standard', 'normal'), requested_by_id (string), approved_by_id (string), risk_level (enum: 'high', 'medium', 'low'), scheduled_start (timestamp), scheduled_end (timestamp), actual_start (timestamp), actual_end (timestamp), status (enum: 'requested', 'approved', 'scheduled', 'in_progress', 'completed', 'failed', 'rolled_back'), created_at (timestamp)), 'rollback_requests' (rollback request records; filterable by rollback_id (string), rollback_code (string), change_id (string), incident_id (string), requested_by_id (string), approved_by_id (string), executed_at (timestamp), validation_completed (boolean: True/False), status (enum: 'requested', 'approved', 'in_progress', 'completed', 'failed'), created_at (timestamp)).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'change_requests' or 'rollback_requests'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False. For change_requests, filters are: change_id (string), change_code (string), incident_id (string), title (string), change_type (enum: 'emergency', 'standard', 'normal'), requested_by_id (string), approved_by_id (string), risk_level (enum: 'high', 'medium', 'low'), scheduled_start (timestamp), scheduled_end (timestamp), actual_start (timestamp), actual_end (timestamp), status (enum: 'requested', 'approved', 'scheduled', 'in_progress', 'completed', 'failed', 'rolled_back'), created_at (timestamp). For rollback_requests, filters are: rollback_id (string), rollback_code (string), change_id (string), incident_id (string), requested_by_id (string), approved_by_id (string), executed_at (timestamp), validation_completed (boolean: True/False), status (enum: 'requested', 'approved', 'in_progress', 'completed', 'failed'), created_at (timestamp)"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
