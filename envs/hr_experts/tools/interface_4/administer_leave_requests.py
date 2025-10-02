import json
from typing import Any, Dict, Optional
import datetime
from tau_bench.envs.tool import Tool

class AdministerLeaveRequests(Tool):
    """
    Execute leave requests, including creation and status updates.
    """

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        operation: str,
        employee_id: Optional[str] = None,
        leave_type: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        days_requested: Optional[float] = None,
        leave_id: Optional[str] = None,
        status: Optional[str] = None,
        approved_by: Optional[str] = None,
    ) -> str:
        """
        Executes the specified operation (create or update) on leave requests.
        """
        def generate_id(table: Dict[str, Any]) -> str:
            """Generates a new unique ID for a record."""
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        timestamp = "2025-10-01T12:00:00"
        leave_requests = data.get("leave_requests", {})
        employees = data.get("employees", {})
        users = data.get("users", {})

        if operation == "create":
            if not all([employee_id, leave_type, start_date, end_date, days_requested]):
                return json.dumps({"error": "Missing required parameters for create operation."})
            
            if employee_id not in employees:
                return json.dumps({"error": f"Employee with ID {employee_id} not found."})
            
            # --- Start of revised validation logic ---
            try:
                start_date_obj = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
                end_date_obj = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

                if start_date_obj > end_date_obj:
                    return json.dumps({"error": "Validation failed: The start_date cannot be after the end_date."})
            except ValueError:
                return json.dumps({"error": "Invalid date format. Please use YYYY-MM-DD."})
            # --- End of revised validation logic ---
            
            valid_leave_types = ["annual", "sick", "fmla", "personal", "bereavement", "jury_duty"]
            if leave_type not in valid_leave_types:
                return json.dumps({"error": f"Invalid leave type. Must be one of {valid_leave_types}."})

            new_leave_id = generate_id(leave_requests)
            new_request = {
                "leave_id": new_leave_id,
                "employee_id": employee_id,
                "leave_type": leave_type,
                "start_date": start_date,
                "end_date": end_date,
                "days_requested": days_requested,
                "status": "pending",
                "approved_by": None,
                "approval_date": None,
                "created_at": timestamp,
                "updated_at": timestamp,
            }
            leave_requests[new_leave_id] = new_request
            return json.dumps(new_request)

        elif operation == "update":
            if not all([leave_id, status, approved_by]):
                return json.dumps({"error": "Missing required parameters for update operation."})

            if leave_id not in leave_requests:
                return json.dumps({"error": f"Leave request with ID {leave_id} not found."})
            
            if approved_by not in users:
                return json.dumps({"error": f"User with ID {approved_by} not found."})

            valid_statuses = ["approved", "rejected", "cancelled"]
            if status not in valid_statuses:
                return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}."})

            request_to_update = leave_requests[leave_id]
            request_to_update["status"] = status
            request_to_update["approved_by"] = approved_by
            request_to_update["approval_date"] = timestamp
            request_to_update["updated_at"] = timestamp
            return json.dumps(request_to_update)

        else:
            return json.dumps({"error": "Invalid operation. Must be 'create' or 'update'."})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        """
        Returns the schema for the ManageLeaveRequests tool.
        """
        return {
            "type": "function",
            "function": {
                "name": "administer_leave_requests",
                "description": "Handles the creation of new leave requests by employees and the subsequent updating of their status (e.g., approval, rejection) by authorized personnel.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation": {"type": "string", "description": "Action: 'create', 'update'."},
                        "employee_id": {"type": "string", "description": "ID of the employee requesting leave. Required for 'create'."},
                        "leave_type": {"type": "string", "description": "Type of leave: 'annual', 'sick', 'fmla', 'personal', 'bereavement', 'jury_duty'. Required for 'create'."},
                        "start_date": {"type": "string", "description": "The first day of the leave period (YYYY-MM-DD). Required for 'create'."},
                        "end_date": {"type": "string", "description": "The last day of the leave period (YYYY-MM-DD). Required for 'create'."},
                        "days_requested": {"type": "number", "description": "The total number of leave days requested. Required for 'create'."},
                        "leave_id": {"type": "string", "description": "The ID of the leave request to be updated. Required for 'update'."},
                        "status": {"type": "string", "description": "New status: 'approved', 'rejected', 'cancelled'. Required for 'update'."},
                        "approved_by": {"type": "string", "description": "The user ID of the manager or HR personnel approving or rejecting the request. Required for 'update'."},
                    },
                    "required": ["operation"],
                },
            },
        }