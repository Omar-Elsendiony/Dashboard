import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool

class DiscoverTimesheetEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover timesheet entities.
        
        Supported entities:
        - employee_timesheets: Employee timesheet records by timesheet_id, employee_id, work_date, clock_in_time, clock_out_time, break_duration_minutes, total_hours, project_code, approved_by, status, created_at, updated_at
        """
        if entity_type not in ["employee_timesheets"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'employee_timesheets'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get("employee_timesheets", {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, "timesheet_id": entity_id})
            else:
                results.append({**entity_data, "timesheet_id": entity_id})
        
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
                "name": "discover_timesheet_entities",
                "description": "Discover timesheet entities. Entity types: 'employee_timesheets' (employee timesheet records; filterable by timesheet_id (string), employee_id (string), work_date (date), clock_in_time (timestamp), clock_out_time (timestamp), break_duration_minutes (integer), total_hours (decimal), project_code (string), approved_by (string), status (enum: 'draft', 'submitted', 'approved', 'rejected'), created_at (timestamp), updated_at (timestamp)).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'employee_timesheets'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False. For employee_timesheets, filters are: timesheet_id (string), employee_id (string), work_date (date), clock_in_time (timestamp), clock_out_time (timestamp), break_duration_minutes (integer), total_hours (decimal), project_code (string), approved_by (string), status (enum: 'draft', 'submitted', 'approved', 'rejected'), created_at (timestamp), updated_at (timestamp)"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }