import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class DiscoverRootCauseAnalysisEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover root cause analysis entities.
        
        Supported entities:
        - root_cause_analysis: Root cause analysis records
        """
        if entity_type not in ["root_cause_analysis"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'root_cause_analysis'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get("root_cause_analysis", {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, "rca_id": str(entity_id)})
            else:
                results.append({**entity_data, "rca_id": str(entity_id)})
        
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
                "name": "discover_root_cause_analysis_entities",
                "description": "Discover root cause analysis entities. Entity types: 'root_cause_analysis' (root cause analysis records; filterable by rca_id (string), incident_id (string), analysis_method (enum: 'five_whys', 'fishbone', 'timeline_analysis', 'fault_tree'), conducted_by_id (string), completed_at (timestamp), status (enum: 'in_progress', 'completed', 'approved'), created_at (timestamp)).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'root_cause_analysis'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False. For root_cause_analysis, filters are: rca_id (string), incident_id (string), analysis_method (enum: 'five_whys', 'fishbone', 'timeline_analysis', 'fault_tree'), conducted_by_id (string), completed_at (timestamp), status (enum: 'in_progress', 'completed', 'approved'), created_at (timestamp)"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
