import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class HandleTimesheetEntries(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, timesheet_data: Dict[str, Any] = None, timesheet_id: str = None) -> str:
        """
        Create or update timesheet entry records.
        
        Actions:
        - create: Create new timesheet entry (requires employee_id, work_date, clock_in_time, clock_out_time)
        - update: Update existing timesheet entry (requires timesheet_id, timesheet_data)
        """
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
            
        def is_valid_time_order(clock_in: str, clock_out: str) -> bool:
            """Check if clock_in time is before clock_out time - simplified for demo"""
            return clock_in < clock_out
            
        def calculate_total_hours(clock_in: str, clock_out: str, break_minutes: int = 0) -> float:
            """Calculate total hours worked - simplified calculation for demo"""
            # In a real implementation, this would parse timestamps and calculate actual duration
            # For demo purposes, we'll do a simple calculation
            try:
                # Assuming format like "2025-10-01T08:00:00"
                in_hour = int(clock_in.split('T')[1].split(':')[0])
                out_hour = int(clock_out.split('T')[1].split(':')[0])
                total_minutes = (out_hour - in_hour) * 60 - break_minutes
                return round(total_minutes / 60, 2)
            except:
                return 0.0
        
        if action not in ["create", "update"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid action '{action}'. Must be 'create' or 'update'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for timesheet entries"
            })
        
        employee_timesheets = data.get("employee_timesheets", {})
        employees = data.get("employees", {})
        users = data.get("users", {})
        
        if action == "create":
            if not timesheet_data:
                return json.dumps({
                    "success": False,
                    "error": "timesheet_data is required for create action"
                })
            
            # Validate required fields
            required_fields = ["employee_id", "work_date", "clock_in_time", "clock_out_time"]
            missing_fields = [field for field in required_fields if field not in timesheet_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Employee not found or inactive - missing fields: {', '.join(missing_fields)}"
                })
            
            # Validate that employee exists and has active status
            employee_id = str(timesheet_data["employee_id"])
            if employee_id not in employees:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Employee not found or inactive"
                })
            
            employee = employees[employee_id]
            if employee.get("employment_status") != "active":
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Employee not found or inactive"
                })
            
            # Validate that clock_in_time is before clock_out_time
            clock_in_time = timesheet_data["clock_in_time"]
            clock_out_time = timesheet_data["clock_out_time"]
            if not is_valid_time_order(clock_in_time, clock_out_time):
                return json.dumps({
                    "success": False,
                    "error": "Halt: Invalid work date or times - clock_in_time must be before clock_out_time"
                })
            
            # Validate break_duration_minutes if provided
            break_duration = timesheet_data.get("break_duration_minutes", 0)
            try:
                break_duration = int(break_duration)
                if break_duration < 0:
                    return json.dumps({
                        "success": False,
                        "error": "Halt: Invalid break duration - break_duration_minutes must be non-negative"
                    })
            except (ValueError, TypeError):
                return json.dumps({
                    "success": False,
                    "error": "Halt: Invalid break duration - invalid break_duration_minutes format"
                })
            
            # Validate only allowed fields are present
            allowed_fields = ["employee_id", "work_date", "clock_in_time", "clock_out_time", 
                            "break_duration_minutes", "project_code", "total_hours", "status"]
            invalid_fields = [field for field in timesheet_data.keys() if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for timesheet creation: {', '.join(invalid_fields)}"
                })
            
            # Generate new timesheet ID
            new_timesheet_id = generate_id(employee_timesheets)
            
            # Calculate total hours if not provided
            total_hours = timesheet_data.get("total_hours")
            if total_hours is None:
                total_hours = calculate_total_hours(clock_in_time, clock_out_time, break_duration)
            
            # Create timesheet entry with required information
            new_timesheet = {
                "timesheet_id": str(new_timesheet_id),
                "employee_id": employee_id,
                "work_date": timesheet_data["work_date"],
                "clock_in_time": clock_in_time,
                "clock_out_time": clock_out_time,
                "break_duration_minutes": break_duration,
                "total_hours": total_hours,
                "project_code": timesheet_data.get("project_code"),
                "approved_by": None,
                "status": timesheet_data.get("status", "draft"),  # Default to draft if not specified
                "created_at": "2025-10-01T12:00:00",
                "updated_at": "2025-10-01T12:00:00"
            }
            
            employee_timesheets[str(new_timesheet_id)] = new_timesheet
            
            return json.dumps({
                "success": True,
                "action": "create",
                "timesheet_id": str(new_timesheet_id),
                "message": f"Timesheet entry {new_timesheet_id} created successfully",
                "timesheet_data": new_timesheet
            })
        
        elif action == "update":
            if not timesheet_id:
                return json.dumps({
                    "success": False,
                    "error": "timesheet_id is required for update action"
                })
            
            if timesheet_id not in employee_timesheets:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Timesheet not found"
                })
            
            if not timesheet_data:
                return json.dumps({
                    "success": False,
                    "error": "timesheet_data is required for update action"
                })
            
            # Validate at least one optional field is provided
            update_fields = ["clock_in_time", "clock_out_time", "break_duration_minutes", "total_hours", 
                           "project_code", "status", "approved_by"]
            provided_fields = [field for field in update_fields if field in timesheet_data]
            if not provided_fields:
                return json.dumps({
                    "success": False,
                    "error": "At least one optional field must be provided for updates"
                })
            
            # Get current timesheet for validation
            current_timesheet = employee_timesheets[timesheet_id]
            
            # Validate only allowed fields for updates
            invalid_fields = [field for field in timesheet_data.keys() if field not in update_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for timesheet update: {', '.join(invalid_fields)}"
                })
            
            # Validate status if provided
            if "status" in timesheet_data:
                valid_statuses = ["draft", "submitted", "approved", "rejected"]
                if timesheet_data["status"] not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: Timesheet approval/correction failed - status must be one of: {', '.join(valid_statuses)}"
                    })
            
            # Validate time order if both clock times are being updated
            if "clock_in_time" in timesheet_data or "clock_out_time" in timesheet_data:
                clock_in = timesheet_data.get("clock_in_time", current_timesheet.get("clock_in_time"))
                clock_out = timesheet_data.get("clock_out_time", current_timesheet.get("clock_out_time"))
                
                if clock_in and clock_out and not is_valid_time_order(clock_in, clock_out):
                    return json.dumps({
                        "success": False,
                        "error": "Halt: Timesheet approval/correction failed - clock_in_time must be before clock_out_time"
                    })
            
            # Validate break_duration_minutes if provided
            if "break_duration_minutes" in timesheet_data:
                try:
                    break_duration = int(timesheet_data["break_duration_minutes"])
                    if break_duration < 0:
                        return json.dumps({
                            "success": False,
                            "error": "Halt: Timesheet approval/correction failed - break_duration_minutes must be non-negative"
                        })
                except (ValueError, TypeError):
                    return json.dumps({
                        "success": False,
                        "error": "Halt: Timesheet approval/correction failed - invalid break_duration_minutes format"
                    })
            
            # Validate approved_by user exists if provided
            if "approved_by" in timesheet_data and timesheet_data["approved_by"] is not None:
                approver_id = str(timesheet_data["approved_by"])
                if approver_id not in users:
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: Timesheet approval/correction failed - approver not found"
                    })
            
            # Update timesheet entry
            updated_timesheet = current_timesheet.copy()
            for key, value in timesheet_data.items():
                updated_timesheet[key] = value
            
            # Recalculate total_hours if times or break changed but total_hours not explicitly provided
            if ("clock_in_time" in timesheet_data or "clock_out_time" in timesheet_data or 
                "break_duration_minutes" in timesheet_data) and "total_hours" not in timesheet_data:
                clock_in = updated_timesheet.get("clock_in_time")
                clock_out = updated_timesheet.get("clock_out_time")
                break_min = updated_timesheet.get("break_duration_minutes", 0)
                if clock_in and clock_out:
                    updated_timesheet["total_hours"] = calculate_total_hours(clock_in, clock_out, break_min)
            
            updated_timesheet["updated_at"] = "2025-10-01T12:00:00"
            employee_timesheets[timesheet_id] = updated_timesheet
            
            return json.dumps({
                "success": True,
                "action": "update",
                "timesheet_id": timesheet_id,
                "message": f"Timesheet entry {timesheet_id} updated successfully",
                "timesheet_data": updated_timesheet
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "handle_timesheet_entries",
                "description": "Create or update timesheet entry records in the HR system. This tool manages employee time tracking with comprehensive validation and workflow controls. For creation, establishes new timesheet entries with proper validation of employee existence, work time logic, and break duration. For updates, modifies existing entries while enforcing proper time validation and status transitions. Validates clock times are in proper order, ensures break durations are non-negative, validates status values, and verifies approver existence. Essential for time tracking, payroll processing, and maintaining accurate work hour records.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' to establish new timesheet entry, 'update' to modify existing entry",
                            "enum": ["create", "update"]
                        },
                        "timesheet_data": {
                            "type": "object",
                            "description": "Timesheet data object. For create: requires employee_id, work_date, clock_in_time, clock_out_time. Optional: break_duration_minutes, project_code, total_hours, status. For update: at least one of clock_in_time, clock_out_time, break_duration_minutes, total_hours, project_code, status, approved_by. SYNTAX: {\"key\": \"value\"}",
                            "properties": {
                                "employee_id": {
                                    "type": "string",
                                    "description": "Employee identifier (required for create, must exist with active status)"
                                },
                                "work_date": {
                                    "type": "string",
                                    "description": "Work date in YYYY-MM-DD format (required for create)"
                                },
                                "clock_in_time": {
                                    "type": "string",
                                    "description": "Clock in timestamp (required for create, must be before clock_out_time)"
                                },
                                "clock_out_time": {
                                    "type": "string",
                                    "description": "Clock out timestamp (required for create, must be after clock_in_time)"
                                },
                                "break_duration_minutes": {
                                    "type": "integer",
                                    "description": "Break duration in minutes (must be non-negative, default: 0)"
                                },
                                "project_code": {
                                    "type": "string",
                                    "description": "Project code for time allocation"
                                },
                                "total_hours": {
                                    "type": "number",
                                    "description": "Total hours worked (auto-calculated if not provided)"
                                },
                                "status": {
                                    "type": "string",
                                    "description": "Timesheet status (default: draft for creation)",
                                    "enum": ["draft", "submitted", "approved", "rejected"]
                                },
                                "approved_by": {
                                    "type": "string",
                                    "description": "User ID of approver (must exist in user system)"
                                }
                            }
                        },
                        "timesheet_id": {
                            "type": "string",
                            "description": "Unique identifier of the timesheet entry (required for update action only)"
                        }
                    },
                    "required": ["action"]
                }
            }
        }