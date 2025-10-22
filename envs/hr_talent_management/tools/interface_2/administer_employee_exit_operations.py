import json
import re
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool
from datetime import datetime, date


class AdministerEmployeeExitOperations(Tool):
    
    @staticmethod
    def invoke(data: Dict[str, Any], operation_type: str, **kwargs) -> str:
        """
        Manages employee exit operations: creation, clearance updates, and final settlement processing.
        """
        
        # --- Utility Functions ---
        def generate_id(table: Dict[str, Any]) -> int:
            """Utility to generate a new sequential ID for the employee_exits table."""
            if not table:
                return 9001
            return max(int(k) for k in table.keys()) + 1

        def validate_date_format(date_str: str, field_name: str, allow_future: bool = True) -> Optional[str]:
            """Validates date format (YYYY-MM-DD) and checks if it's not in the future."""
            if date_str:
                date_pattern = r'^\d{4}-\d{2}-\d{2}$'
                if not re.match(date_pattern, date_str):
                    return f"Invalid {field_name} format. Must be YYYY-MM-DD"
                
                try:
                    dt_obj = datetime.strptime(date_str, '%Y-%m-%d')
                    # Check for future date if not allowed
                    if not allow_future:
                        simulated_today = date(2025, 10, 1) # Using same simulated date as other tools
                        if dt_obj.date() > simulated_today:
                             return f"{field_name} cannot be in the future (compared to the system date)."
                except ValueError:
                    return f"Invalid date value provided for {field_name}. Please check year/month/day validity."
            return None

        def convert_date_format(date_str: str) -> str:
            """Convert YYYY-MM-DD format for internal storage."""
            if date_str and re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
                return date_str
            return date_str

        def validate_status_field(status_value: str, field_name: str, valid_statuses: list) -> Optional[str]:
            """Validate status field against allowed values."""
            if status_value and status_value not in valid_statuses:
                return f"Invalid {field_name}. Must be one of: {', '.join(valid_statuses)}"
            return None
        
        valid_operations = ["create_exit", "update_clearance", "process_settlement"]
        if operation_type not in valid_operations:
            return json.dumps({
                "success": False,
                "exit_id": None,
                "message": f"Invalid operation_type '{operation_type}'. Must be one of: {', '.join(valid_operations)}"
            })

        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "exit_id": None,
                "message": "Invalid data format for employee exit operations"
            })
        
        exits = data.get("employee_exits", {})
        employees = data.get("employees", {})
        users = data.get("users", {})
        
        simulated_today = date(2025, 10, 1) # Used for past date checks

        # --- Employee Exit Creation (create_exit) ---
        if operation_type == "create_exit":
            required_fields = ["employee_id", "exit_date", "exit_reason", "user_id"]
            missing_fields = [field for field in required_fields if field not in kwargs or kwargs[field] is None]
            
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "exit_id": None,
                    "message": f"Halt: Missing mandatory fields: {', '.join(missing_fields)}",
                    "transfer_to_human": True
                })

            # 1. Validation Checks
            employee_id_str = str(kwargs["employee_id"])
            requester_id_str = str(kwargs["user_id"]) if kwargs.get("user_id") is not None else None

            # SOP: Verify user is an active HR Admin, HR Manager, or HR Director
            requester = users.get(requester_id_str)
            if not requester:
                return json.dumps({"success": False, "exit_id": None, "message": "Halt: Operation failed due to system errors - requester user not found", "transfer_to_human": True})
            
            if requester.get("employment_status") != "active" or requester.get("role") not in ["hr_manager", "hr_admin", "hr_payroll_administrator"]:
                return json.dumps({"success": False, "exit_id": None, "message": "Halt: Unauthorized requester attempting to initiate exit - must be active HR Admin/Manager/Director", "transfer_to_human": True})

            # SOP: Verify employee exists and is active
            employee = employees.get(employee_id_str)
            if not employee or employee.get("employment_status") not in ["active", "on_leave"]:
                return json.dumps({"success": False, "exit_id": None, "message": "Halt: Employee not found or inactive", "transfer_to_human": True})

            # Check for existing exit record (Employee already in exit process)
            if any(e.get("employee_id") == employee_id_str for e in exits.values()):
                return json.dumps({"success": False, "exit_id": None, "message": f"Halt: Employee {employee_id_str} is already in the exit process.", "transfer_to_human": True})

            # Validate exit_date format and ensure it's not in the past
            date_error = validate_date_format(kwargs["exit_date"], "exit_date")
            if date_error:
                return json.dumps({"success": False, "exit_id": None, "message": f"Halt: {date_error}", "transfer_to_human": True})
            
            converted_exit_date = convert_date_format(kwargs["exit_date"])
            exit_date_obj = datetime.strptime(converted_exit_date, '%Y-%m-%d').date()
            if exit_date_obj < simulated_today:
                return json.dumps({"success": False, "exit_id": None, "message": "Halt: Exit date cannot be in the past", "transfer_to_human": True})

            # Validate exit_reason
            valid_reasons = ["resignation", "termination", "retirement", "contract_end"]
            reason_error = validate_status_field(kwargs["exit_reason"], "exit_reason", valid_reasons)
            if reason_error:
                return json.dumps({"success": False, "exit_id": None, "message": f"Halt: {reason_error}", "transfer_to_human": True})

            # 2. Create Exit Record
            new_exit_id = generate_id(exits)
            timestamp = "2025-10-10T12:00:00"

            new_exit = {
                "exit_id": str(new_exit_id),
                "employee_id": employee_id_str,
                "exit_date": converted_exit_date,
                "exit_reason": kwargs["exit_reason"],
                "manager_clearance": "pending",
                "it_equipment_return": "pending",
                "clearance_status": "pending",
                "final_pay_amount": None,
                "leave_encashment_amount": None,
                "finance_settlement_status": "draft",
                "approved_by": None,
                "approval_date": None,
                "paid_date": None,
                "created_at": timestamp,
                "updated_at": timestamp
            }
            
            exits[str(new_exit_id)] = new_exit
            
            # SOP: Create Audit Entry
            try:
                audit_trails = data.setdefault("audit_trails", {})
                new_audit_id = str(max([int(k) for k in audit_trails.keys()] + [0]) + 1)
                audit_entry = {
                    "audit_id": new_audit_id,
                    "reference_id": str(new_exit_id),
                    "reference_type": "exit",
                    "action": "create",
                    "user_id": requester_id_str,
                    "field_name": None,
                    "old_value": None,
                    "new_value": json.dumps({"created_by": requester_id_str}),
                    "created_at": timestamp
                }
                audit_trails[new_audit_id] = audit_entry
            except Exception:
                # If audit fails, we still report success for the primary operation
                pass

            return json.dumps({
                "success": True,
                "exit_id": str(new_exit_id),
                "message": f"Employee exit record {new_exit_id} created successfully. Clearance process initiated."
            })

        # --- Exit Clearance Management (update_clearance) ---
        elif operation_type == "update_clearance":
            required_fields = ["exit_id", "user_id"] # Only exit_id and user_id are mandatory, others are optional updates
            optional_fields = ["manager_clearance", "it_equipment_return", "finance_settlement_status"]
            
            missing_fields = [field for field in required_fields if field not in kwargs or kwargs[field] is None]
            if missing_fields:
                return json.dumps({"success": False, "exit_id": None, "message": f"Missing mandatory fields: {', '.join(missing_fields)}"})

            exit_id_str = str(kwargs["exit_id"])
            exit_record = exits.get(exit_id_str)
            
            # 1. Verify Exit Record Exists
            if not exit_record:
                return json.dumps({"success": False, "exit_id": exit_id_str, "message": f"Exit record {exit_id_str} not found."})

            # 2. Validate and Update Clearance Statuses
            manager_clearance = kwargs.get("manager_clearance")
            it_equipment_return = kwargs.get("it_equipment_return")
            finance_settlement_status = kwargs.get("finance_settlement_status")
            
            valid_manager_clearance = ["pending", "approved", "rejected"]
            valid_it_return = ["pending", "returned", "not_applicable"]
            valid_finance_settlement = ["draft", "calculated", "approved", "paid", "failed"]

            if manager_clearance:
                error = validate_status_field(manager_clearance, "manager_clearance", valid_manager_clearance)
                if error: return json.dumps({"success": False, "exit_id": exit_id_str, "message": error})
                exit_record["manager_clearance"] = manager_clearance

            if it_equipment_return:
                error = validate_status_field(it_equipment_return, "it_equipment_return", valid_it_return)
                if error: return json.dumps({"success": False, "exit_id": exit_id_str, "message": error})
                exit_record["it_equipment_return"] = it_equipment_return

            if finance_settlement_status:
                error = validate_status_field(finance_settlement_status, "finance_settlement_status", valid_finance_settlement)
                if error: return json.dumps({"success": False, "exit_id": exit_id_str, "message": error})
                exit_record["finance_settlement_status"] = finance_settlement_status
            
            # 3. Determine Overall clearance_status
            # Clearance is 'cleared' only if manager and IT clearance are finalized (approved/returned/not_applicable)
            is_manager_final = exit_record["manager_clearance"] == "approved"
            is_it_final = exit_record["it_equipment_return"] in ["returned", "not_applicable"]
            
            if is_manager_final and is_it_final:
                exit_record["clearance_status"] = "cleared"
            elif exit_record["manager_clearance"] == "rejected":
                 exit_record["clearance_status"] = "rejected"
            else:
                exit_record["clearance_status"] = "pending"

            exit_record["updated_at"] = "2025-10-10T12:00:00"
            
            return json.dumps({
                "success": True,
                "exit_id": exit_id_str,
                "message": f"Exit clearance updated successfully. Current clearance_status: '{exit_record['clearance_status']}'."
            })

        # --- Exit Settlement Processing (process_settlement) ---
        elif operation_type == "process_settlement":
            required_fields = ["exit_id", "final_pay_amount", "leave_encashment_amount", "approved_by", "approval_date", "user_id"]
            missing_fields = [field for field in required_fields if field not in kwargs or kwargs[field] is None]

            if missing_fields:
                return json.dumps({"success": False, "exit_id": None, "message": f"Missing mandatory fields for settlement processing: {', '.join(missing_fields)}"})

            exit_id_str = str(kwargs["exit_id"])
            exit_record = exits.get(exit_id_str)

            # 1. Verify Exit Record Exists and Clearances are Completed
            if not exit_record:
                return json.dumps({"success": False, "exit_id": exit_id_str, "message": f"Exit record {exit_id_str} not found."})
            
            if exit_record.get("clearance_status") != "cleared":
                return json.dumps({
                    "success": False, 
                    "exit_id": exit_id_str, 
                    "message": f"Exit record {exit_id_str} clearances are not completed ('cleared'). Current status: {exit_record.get('clearance_status')}"
                })

            # 2. Validate Amounts
            try:
                final_pay = float(kwargs["final_pay_amount"])
                leave_encashment = float(kwargs["leave_encashment_amount"])
                if final_pay < 0 or leave_encashment < 0:
                    return json.dumps({"success": False, "exit_id": exit_id_str, "message": "Negative final pay or leave encashment amounts are not allowed."})
            except ValueError:
                 return json.dumps({"success": False, "exit_id": exit_id_str, "message": "Final pay and leave encashment amounts must be valid numbers."})

            # 3. Validate Approval Date (must not be in the future)
            date_error = validate_date_format(kwargs["approval_date"], "approval_date", allow_future=False)
            if date_error:
                return json.dumps({"success": False, "exit_id": exit_id_str, "message": date_error})

            # 4. Process Settlement (Update financial fields and set status to 'approved' by finance)
            converted_approval_date = convert_date_format(kwargs["approval_date"])

            exit_record["final_pay_amount"] = final_pay
            exit_record["leave_encashment_amount"] = leave_encashment
            exit_record["approved_by"] = str(kwargs["approved_by"]) # Assuming approved_by is the finance approver/HR Admin
            exit_record["approval_date"] = converted_approval_date
            exit_record["finance_settlement_status"] = "approved" # Settlement is calculated and approved in this SOP step

            exit_record["updated_at"] = "2025-10-10T12:00:00"
            
            return json.dumps({
                "success": True,
                "exit_id": exit_id_str,
                "message": f"Exit settlement processed and approved successfully. Final Pay: {final_pay:.2f}, Leave Encashment: {leave_encashment:.2f}. Settlement status set to 'approved'."
            })
        
        return json.dumps({
            "success": False,
            "exit_id": None,
            "message": "Unhandled operation type"
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "administer_employee_exit_operations",
                "description": "Manages the employee separation lifecycle. 'create_exit' initiates the process and sets initial clearance statuses to 'pending'. 'update_clearance' tracks and updates individual clearance items (manager, IT, finance status) and calculates the overall 'clearance_status'. 'process_settlement' finalizes financial amounts and marks the settlement as 'approved' after all clearances are complete.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation_type": {
                            "type": "string",
                            "description": "Type of operation to perform: 'create_exit', 'update_clearance', or 'process_settlement'.",
                            "enum": ["create_exit", "update_clearance", "process_settlement"]
                        },
                        "employee_id": {
                            "type": "string",
                            "description": "Unique identifier of the employee (required for create_exit)."
                        },
                        "exit_date": {
                            "type": "string",
                            "description": "The official last day of employment (YYYY-MM-DD, required for create_exit, must be current or future)."
                        },
                        "exit_reason": {
                            "type": "string",
                            "description": "Reason for separation (required for create_exit).",
                            "enum": ["resignation", "termination", "retirement", "contract_end"]
                        },
                        "user_id": {
                            "type": "string",
                            "description": "Unique identifier of the HR Admin initiating the action (required for all operations)."
                        },
                        "exit_id": {
                            "type": "string",
                            "description": "Unique identifier of the employee exit record (required for update_clearance and process_settlement)."
                        },
                        "manager_clearance": {
                            "type": "string",
                            "description": "Manager sign-off status (optional for update_clearance).",
                            "enum": ["pending", "approved", "rejected"]
                        },
                        "it_equipment_return": {
                            "type": "string",
                            "description": "IT equipment return status (optional for update_clearance).",
                            "enum": ["pending", "returned", "not_applicable"]
                        },
                        "finance_settlement_status": {
                            "type": "string",
                            "description": "Current finance status (optional for update_clearance, used for tracking).",
                            "enum": ["draft", "calculated", "approved", "paid", "failed"]
                        },
                        "final_pay_amount": {
                            "type": "number",
                            "description": "The calculated final salary amount (required for process_settlement)."
                        },
                        "leave_encashment_amount": {
                            "type": "number",
                            "description": "The calculated amount for unused leave (required for process_settlement)."
                        },
                        "approved_by": {
                            "type": "string",
                            "description": "Unique identifier of the Finance/HR manager approving the settlement (required for process_settlement)."
                        },
                        "approval_date": {
                            "type": "string",
                            "description": "The date the final settlement was approved (YYYY-MM-DD, required for process_settlement, must not be in the future)."
                        }
                    },
                    "required": ["operation_type"]
                }
            }
        }
