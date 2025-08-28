import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class QueryJobPositions(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], position_id: Optional[str] = None, title: Optional[str] = None, department_id: Optional[str] = None, job_level: Optional[str] = None, hourly_rate_min: Optional[str] = None, hourly_rate_max: Optional[str] = None, status: Optional[str] = None) -> str:

        job_positions = data.get("job_positions", {})
        results = []
        
        for position in job_positions.values():
            if position_id and position.get("position_id") != position_id:
                continue
            if department_id and position.get("department_id") != department_id:
                continue
            if job_level and position.get("job_level") != job_level:
                continue
            if status and position.get("status") != status:
                continue
            if title:
                if title.lower() != position.get("title").lower():
                    continue
            if hourly_rate_min and position.get("hourly_rate_min", 0) < float(hourly_rate_min):
                continue
            if hourly_rate_max and position.get("hourly_rate_max", 0) > float(hourly_rate_max):
                continue
            results.append(position)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "query_job_positions",
                "description": "Query job positions with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "position_id": {"type": "string", "description": "Filter by position ID"},
                        "department_id": {"type": "string", "description": "Filter by department ID"},
                        "job_level": {"type": "string", "description": "Filter by job level"},
                        "status": {"type": "string", "description": "Filter by status"},
                        "hourly_rate_min": {"type": "string", "description": "Filter by the positions that have hourly rate greater than or equal to the hourly_rate_min"},
                        "hourly_rate_max": {"type": "string", "description": "Filter by the positions that have hourly rate less than or equal to the hourly_rate_max"},
                        "title": {"type": "string", "description": "Filter by title case insensitively"}
                    },
                    "required": []
                }
            }
        }