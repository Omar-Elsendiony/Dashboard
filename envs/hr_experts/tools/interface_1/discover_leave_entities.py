import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class DiscoverLeaveEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover leave entities.
        
        Supported entities:
        - leave_requests: Leave requests by leave_id, employee_id, leave_type, start_date, end_date, days_requested, status, approved_by, approval_date, remaining_balance, created_at, updated_at
        """
        if entity_type not in ["leave_requests"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'leave_requests'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get("leave_requests", {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, "leave_id": entity_id})
            else:
                results.append({**entity_data, "leave_id": entity_id})
        
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
                "name": "discover_leave_entities",
                "description": "Discover leave entities. Entity types: 'leave_requests' (leave requests; filterable by leave_id (string), employee_id (string), leave_type (enum: 'annual', 'sick', 'fmla', 'personal', 'bereavement', 'jury_duty'), start_date (date), end_date (date), days_requested (decimal), status (enum: 'pending', 'approved', 'rejected', 'cancelled'), approved_by (string), approval_date (timestamp), remaining_balance (decimal), created_at (timestamp), updated_at (timestamp)).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'leave_requests'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False. For leave_requests, filters are: leave_id (string), employee_id (string), leave_type (enum: 'annual', 'sick', 'fmla', 'personal', 'bereavement', 'jury_duty'), start_date (date), end_date (date), days_requested (decimal), status (enum: 'pending', 'approved', 'rejected', 'cancelled'), approved_by (string), approval_date (timestamp), remaining_balance (decimal), created_at (timestamp), updated_at (timestamp)"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
