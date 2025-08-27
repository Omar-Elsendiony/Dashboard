import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetLeaveRequests(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], leave_id: str = None, employee_id: str = None, 
               leave_type: str = None, status: str = None) -> str:
        leave_requests = data.get("leave_requests", {})
        results = []
        
        for leave in leave_requests.values():
            if leave_id and leave.get("leave_id") != leave_id:
                continue
            if employee_id and leave.get("employee_id") != employee_id:
                continue
            if leave_type and leave.get("leave_type") != leave_type:
                continue
            if status and leave.get("status") != status:
                continue
            results.append(leave)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_leave_requests",
                "description": "Retrieve leave requests with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "leave_id": {"type": "string", "description": "Filter by leave request ID"},
                        "employee_id": {"type": "string", "description": "Filter by employee ID"},
                        "leave_type": {"type": "string", "description": "Filter by leave type"},
                        "status": {"type": "string", "description": "Filter by status"}
                    },
                    "required": []
                }
            }
        }
