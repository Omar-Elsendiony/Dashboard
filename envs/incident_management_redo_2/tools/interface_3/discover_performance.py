import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class DiscoverPerformance(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover performance entities (performance_metrics). The entity to discover is decided by entity_type.
        Optionally, filters can be applied to narrow down the search results.
        
        Supported entities:
        - performance_metrics: Performance Metric records
        """
        if entity_type not in ["performance_metrics"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'performance_metrics'"
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
                    results.append({**entity_data, "metric_id": entity_id})
            else:
                results.append({**entity_data, "metric_id": entity_id})
        
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
                "name": "discover_performance",
                "description": "Discover performance entities (performance metrics). The entity to discover is decided by entity_type. Optional filters can be applied to narrow down the search results.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'performance_metrics'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters to narrow down search results. Only exact matches are supported (AND logic for multiple filters).",
                            "properties": {
                                "metric_id": {
                                    "type": "string",
                                    "description": "Performance metric ID"
                                },
                                "incident_id": {
                                    "type": "string",
                                    "description": "Associated incident ID"
                                },
                                "metric_type": {
                                    "type": "string",
                                    "description": "Type of metric: 'MTTA', 'MTTD', 'MTTR', 'MTTM', 'FTR'"
                                },
                                "calculated_value_minutes": {
                                    "type": "integer",
                                    "description": "Calculated value in minutes"
                                },
                                "sla_target_minutes": {
                                    "type": "integer",
                                    "description": "SLA target in minutes"
                                },
                                "recorded_by": {
                                    "type": "string",
                                    "description": "User ID who recorded the metric"
                                },
                                "recorded_date": {
                                    "type": "string",
                                    "description": "Recording timestamp in YYYY-MM-DD format"
                                }
                            }
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
