import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateLeaveRequest(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], leave_id: str, start_date: str = None, 
               end_date: str = None, days_requested: float = None, 
               reason: str = None) -> str:
        leave_requests = data.get("leave_requests", {})
        
        if leave_id not in leave_requests:
            raise ValueError(f"Leave request {leave_id} not found")
        
        leave_request = leave_requests[leave_id]
        
        # Only allow updates if status is pending
        if leave_request.get("status") != "pending":
            raise ValueError("Cannot update leave request that is not pending")
        
        if start_date is not None:
            leave_request["start_date"] = start_date
        
        if end_date is not None:
            leave_request["end_date"] = end_date
        
        if days_requested is not None:
            leave_request["days_requested"] = days_requested
        
        if reason is not None:
            leave_request["reason"] = reason
        
        leave_request["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps({"success": True, "message": "Leave request updated"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_leave_request",
                "description": "Update a pending leave request",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "leave_id": {"type": "string", "description": "ID of the leave request to update"},
                        "start_date": {"type": "string", "description": "Updated start date"},
                        "end_date": {"type": "string", "description": "Updated end date"},
                        "days_requested": {"type": "number", "description": "Updated number of days requested"},
                        "reason": {"type": "string", "description": "Updated reason for leave"}
                    },
                    "required": ["leave_id"]
                }
            }
        }
