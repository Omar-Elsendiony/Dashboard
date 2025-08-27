import json
from datetime import datetime
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class CreateLeaveRequest(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], employee_id: str, leave_type: str, 
               start_date: str, end_date: str, days_requested: float) -> str:
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        def parse_date(date_str: str) -> datetime:
            try:
                return datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Invalid date format. Use YYYY-MM-DD")
        
        employees = data.get("employees", {})
        leave_requests = data.setdefault("leave_requests", {})
        
        # Validate employee exists
        if employee_id not in employees:
            return json.dumps("Halt: Invalid leave request details: [employee not found]")
        
        # Validate leave type
        valid_leave_types = ["annual", "sick", "fmla", "personal", "bereavement", "jury_duty"]
        if leave_type not in valid_leave_types:
            return json.dumps("Halt: Invalid leave request details: [invalid leave type]")
        
        # Validate dates are provided and logical
        if not start_date or not end_date:
            return json.dumps("Halt: Invalid leave request details: [invalid dates]")
        
        try:
            start_dt = parse_date(start_date)
            end_dt = parse_date(end_date)
            current_date = datetime(2025, 10, 1)
            
            # Check if start date is before end date
            if start_dt >= end_dt:
                return json.dumps("Halt: Invalid leave request details: [invalid dates]")
            
            # Check if dates are not in the past
            if start_dt.date() < current_date.date():
                return json.dumps("Halt: Invalid leave request details: [invalid dates]. They must be after today '2025-10-01'")
            # Calculate actual days between start and end date
            actual_days = (end_dt - start_dt).days

            # Validate that days_requested matches the calculated difference
            if days_requested != actual_days:
                return json.dumps("Halt: Invalid leave request details: [days requested does not match date range]")
            
        except ValueError:
            return json.dumps("Halt: Invalid leave request details: [invalid dates]")
        
        # Leave Request Balance Calculation
        # Retrieve all leave requests for the employee in 2025 for the requested leave type
        total_used_days = 0
        for request in leave_requests.values():
            if (request["employee_id"] == employee_id and 
                request["leave_type"] == leave_type and
                request["status"] in ["approved", "pending"]):
                
                # Check if request is in 2025
                try:
                    request_start = datetime.strptime(request["start_date"], "%Y-%m-%d")
                    if request_start.year == 2025:
                        total_used_days += request["days_requested"]
                except (ValueError, KeyError):
                    continue
        
        # Get allocation for employee and leave type, default to 15 if no allocation record exists
        total_allocation = 15  # Default allocation as specified in requirements
        
        # Calculate available balance
        available_balance = total_allocation - total_used_days
        
        # Leave Request Availability Checks
        if days_requested > available_balance:
            return json.dumps(f"Halt: Insufficient leave balance: [{available_balance} days available]")
        
        # Leave Request Record Creation
        remaining_balance = available_balance - days_requested
        
        leave_id = generate_id(leave_requests)
        timestamp = "2025-10-01T00:00:00"
        
        new_leave_request = {
            "leave_id": leave_id,
            "employee_id": employee_id,
            "leave_type": leave_type,
            "start_date": start_date,
            "end_date": end_date,
            "days_requested": days_requested,
            "status": "pending",
            "approved_by": None,
            "approval_date": None,
            "remaining_balance": remaining_balance,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        leave_requests[leave_id] = new_leave_request
        return json.dumps({"new_leave_request": new_leave_request})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_leave_request",
                "description": "Create a new leave request for an employee",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "employee_id": {"type": "string", "description": "ID of the employee"},
                        "leave_type": {"type": "string", "description": "Type of leave (annual, sick, fmla, personal, bereavement, jury_duty)"},
                        "start_date": {"type": "string", "description": "Start date of leave (YYYY-MM-DD)"},
                        "end_date": {"type": "string", "description": "End date of leave (YYYY-MM-DD)"},
                        "days_requested": {"type": "number", "description": "Number of days requested"}
                    },
                    "required": ["employee_id", "leave_type", "start_date", "end_date", "days_requested"]
                }
            }
        }