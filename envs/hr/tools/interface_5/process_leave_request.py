import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class ProcessLeaveRequest(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], leave_id: str, status: str, 
               approved_by: str = None) -> str:
        leave_requests = data.get("leave_requests", {})
        users = data.get("users", {})
        
        if leave_id not in leave_requests:
            return json.dumps(f"Halt: Leave request {leave_id} not found")
        
        if approved_by and approved_by not in users:
            return json.dumps(f"Halt: Approver user {approved_by} not found")
        
        valid_statuses = ["approved", "rejected", "cancelled"]
        if status not in valid_statuses:
            return json.dumps(f"Halt: Invalid status. Must be one of {valid_statuses}")
        
        leave_request = leave_requests[leave_id]
        
        # Calculate remaining balance if status is approved
        if status == "approved":
            employee_id = leave_request["employee_id"]
            leave_type = leave_request["leave_type"]
            days_requested = leave_request["days_requested"]
            
            # Calculate total used days for this employee and leave type in 2025
            total_used_days = 0
            for request in leave_requests.values():
                if (request["employee_id"] == employee_id and 
                    request["leave_type"] == leave_type and
                    request["status"] in ["approved", "pending"]):
                    
                    # Check if request is in 2025
                    try:
                        from datetime import datetime
                        request_start = datetime.strptime(request["start_date"], "%Y-%m-%d")
                        if request_start.year == 2025:
                            total_used_days += request["days_requested"]
                    except (ValueError, KeyError):
                        continue
            
            # Default allocation of 15 days
            total_allocation = 15
            available_balance = total_allocation - total_used_days
            remaining_balance = available_balance - days_requested
            
            leave_request["remaining_balance"] = remaining_balance
        
        leave_request["status"] = status
        leave_request["approved_by"] = approved_by
        leave_request["approval_date"] = "2025-10-01T00:00:00"
        leave_request["updated_at"] = "2025-10-01T00:00:00"

        return json.dumps({"leave": leave_request})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "process_leave_request",
                "description": "Approve or reject a leave request",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "leave_id": {"type": "string", "description": "ID of the leave request"},
                        "status": {"type": "string", "description": "New status (approved, rejected, cancelled)"},
                        "approved_by": {"type": "string", "description": "ID of the user approving the request"}
                    },
                    "required": ["leave_id", "status"]
                }
            }
        }