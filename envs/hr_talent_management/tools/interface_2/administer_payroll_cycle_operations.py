import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class AdministerPayrollCycleOperations(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], operation_type: str, cycle_start_date: str, cycle_end_date: str, frequency: str, cutoff_date: str, requesting_user_id: str) -> str:
        """
        Manage payroll cycle operations including creation, updates, and status changes.
        
        Operations:
        - create_cycle: Create a new payroll cycle (requires cycle_start_date, cycle_end_date, frequency, cutoff_date, requesting_user_id)
        """
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
            
        def is_valid_date_order(start_date: str, end_date: str) -> bool:
            """Check if start date is before end date"""
            return start_date <= end_date
            
        def is_cutoff_within_range(cutoff_date: str, start_date: str, end_date: str) -> bool:
            """Check if cutoff date is within the cycle range"""
            return start_date <= cutoff_date <= end_date
            
        def check_overlapping_cycles(start_date: str, end_date: str, existing_cycles: Dict[str, Any]) -> bool:
            """Check if the new cycle overlaps with existing cycles"""
            for cycle in existing_cycles.values():
                existing_start = cycle.get("cycle_start_date", "")
                existing_end = cycle.get("cycle_end_date", "")
                # Check for overlap: new start <= existing end AND new end >= existing start
                if start_date <= existing_end and end_date >= existing_start:
                    return True
            return False
        
        if operation_type not in ["create_cycle"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid operation_type '{operation_type}'. Must be 'create_cycle'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for payroll cycle operations"
            })
        
        payroll_cycles = data.get("payroll_cycles", {})
        users = data.get("users", {})
        
        if operation_type == "create_cycle":
            if not requesting_user_id:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Missing mandatory fields - requesting_user_id is required"
                })
            
            # Validate that user is an active HR Payroll Administrator, HR Manager, or HR Director
            if requesting_user_id not in users:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Missing or invalid inputs - user not found"
                })
            
            user = users[requesting_user_id]
            user_role = user.get("role")
            valid_roles = ["hr_payroll_administrator", "hr_manager", "hr_director", "hr_admin"]
            
            if user_role not in valid_roles:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Access denied - user role '{user_role}' is not authorized. Required roles: hr_payroll_administrator, hr_manager, hr_director, or hr_admin"
                })
            
            if user.get("employment_status") != "active":
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Access denied - user employment status '{user.get('employment_status')}' is not active. User must be active to create payroll cycles"
                })
            
            # Validate mandatory fields
            required_fields = {
                "cycle_start_date": cycle_start_date,
                "cycle_end_date": cycle_end_date,
                "frequency": frequency,
                "cutoff_date": cutoff_date
            }
            missing_fields = [field for field, value in required_fields.items() if not value]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Missing mandatory fields - missing fields: {', '.join(missing_fields)}"
                })
            
            # Validate date relationships
            if not is_valid_date_order(cycle_start_date, cycle_end_date):
                return json.dumps({
                    "success": False,
                    "error": "Halt: Invalid date relationships - start date must be before end date"
                })
            
            if not is_cutoff_within_range(cutoff_date, cycle_start_date, cycle_end_date):
                return json.dumps({
                    "success": False,
                    "error": "Halt: Invalid date relationships - cutoff date must be within cycle range"
                })
            
            # Check for overlapping cycles
            if check_overlapping_cycles(cycle_start_date, cycle_end_date, payroll_cycles):
                return json.dumps({
                    "success": False,
                    "error": "Halt: Overlapping cycles detected - new cycle overlaps with existing cycle"
                })
            
            # Validate frequency
            valid_frequencies = ["weekly", "bi_weekly", "monthly"]
            if frequency not in valid_frequencies:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Invalid frequency - must be one of: {', '.join(valid_frequencies)}"
                })
            
            # Generate new cycle ID
            new_cycle_id = generate_id(payroll_cycles)
            
            # Create payroll cycle
            new_cycle = {
                "cycle_id": new_cycle_id,
                "cycle_start_date": cycle_start_date,
                "cycle_end_date": cycle_end_date,
                "frequency": frequency,
                "cutoff_date": cutoff_date,
                "status": "open",
                "created_at": "2025-10-01T12:00:00",
                "updated_at": "2025-10-01T12:00:00"
            }
            
            payroll_cycles[new_cycle_id] = new_cycle
            
            # Create audit entry for cycle creation
            audit_trails = data.get("audit_trails", {})
            audit_id = generate_id(audit_trails)
            audit_entry = {
                "audit_id": audit_id,
                "reference_id": new_cycle_id,
                "reference_type": "payroll",
                "action": "create",
                "user_id": requesting_user_id,
                "field_name": None,
                "old_value": None,
                "new_value": json.dumps(new_cycle),
                "created_at": "2025-10-01T12:00:00"
            }
            audit_trails[audit_id] = audit_entry
            
            return json.dumps({
                "success": True,
                "operation": "create_cycle",
                "cycle_id": new_cycle_id,
                "message": f"Payroll cycle {new_cycle_id} created successfully",
                "cycle_data": new_cycle
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "administer_payroll_cycle_operations",
				"description": "Create and validate payroll cycles when setting up payroll processing periods.\n\nWhat this tool does:\n- Creates a payroll cycle with required dates and frequency.\n- Validates date relationships (start < end, cutoff within the range).\n- Ensures frequency is supported.\n- Prevents overlapping cycles.\n- Verifies the requester is an active HR user with appropriate role.\n\nWho can use it:\n- Active users with role one of: hr_payroll_administrator, hr_manager, hr_admin, hr_director.\n\nInput guidance (enter exactly as described):\n- operation_type: Use 'create_cycle' to create a new payroll cycle.\n- cycle_start_date: Enter date in YYYY-MM-DD (e.g., 2025-01-01). Must be before cycle_end_date.\n- cycle_end_date: Enter date in YYYY-MM-DD (e.g., 2025-01-31). Must be after cycle_start_date.\n- frequency: Choose one of: weekly, bi_weekly, monthly.\n- cutoff_date: Enter date in YYYY-MM-DD that lies between cycle_start_date and cycle_end_date (inclusive).\n- requesting_user_id: Provide a valid user id present in data.users with an allowed role and employment_status 'active'.\n\nBusiness rules enforced:\n- Dates must be valid and in correct order.\n- cutoff_date must be within [cycle_start_date, cycle_end_date].\n- No overlap with any existing payroll cycle date ranges.\n- frequency must be one of the allowed values.\n- Requester must exist, be active, and have a permitted role.\n\nExample input object (JSON):\n{\n  \"operation_type\": \"create_cycle\",\n  \"cycle_start_date\": \"2025-01-01\",\n  \"cycle_end_date\": \"2025-01-31\",\n  \"frequency\": \"monthly\",\n  \"cutoff_date\": \"2025-01-25\",\n  \"requesting_user_id\": \"u_123\"\n}\n\nTypical errors if inputs are incorrect:\n- Missing mandatory fields\n- Invalid date relationships (start >= end, cutoff out of range)\n- Overlapping cycle exists\n- Unsupported frequency\n- Requester not found / inactive / role not permitted",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation_type": {
                            "type": "string",
							"description": "Type of operation to perform. Use 'create_cycle' to establish a new payroll cycle.",
                            "enum": ["create_cycle"]
                        },
                        "cycle_start_date": {
                            "type": "string",
							"description": "Cycle start date (YYYY-MM-DD). Required. Must be strictly before cycle_end_date. Example: 2025-01-01."
                        },
                        "cycle_end_date": {
                            "type": "string",
							"description": "Cycle end date (YYYY-MM-DD). Required. Must be strictly after cycle_start_date. Example: 2025-01-31."
                        },
                        "frequency": {
                            "type": "string",
							"description": "Payroll frequency. Allowed values: weekly, bi_weekly, monthly.",
                            "enum": ["weekly", "bi_weekly", "monthly"]
                        },
                        "cutoff_date": {
                            "type": "string",
							"description": "Cutoff date (YYYY-MM-DD). Required. Must lie within the inclusive range [cycle_start_date, cycle_end_date]. Example: 2025-01-25."
                        },
                        "requesting_user_id": {
                            "type": "string",
							"description": "User id of the requester. Required. User must exist in data.users, have employment_status 'active', and role in {hr_payroll_administrator, hr_manager, hr_director, hr_admin}."
                        }
                    },
                    "required": ["operation_type", "cycle_start_date", "cycle_end_date", "frequency", "cutoff_date", "requesting_user_id"]
                }
            }
        }
