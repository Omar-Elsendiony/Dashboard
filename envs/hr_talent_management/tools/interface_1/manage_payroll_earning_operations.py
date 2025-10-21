import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ManagePayrollEarningOperations(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], operation_type: str, payroll_input_id: str = None,
               earning_type: str = None, amount: float = None, user_id: str = None,
               earning_id: str = None, approval_status: str = None, approved_by: str = None,
               approval_date: str = None) -> str:
        """
        Manage payroll earning operations including creation and approval.
        
        Operations:
        - create_earning: Create additional earning record for employee (requires payroll_input_id, earning_type, amount, user_id)
        - approve_earning: Approve additional earning record (requires earning_id, approval_status, approved_by, approval_date)
        """
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
            
        def is_valid_amount(amount: float) -> bool:
            """Check if amount is valid (positive)"""
            return amount is not None and amount > 0
        
        if operation_type not in ["create_earning", "approve_earning"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid operation_type '{operation_type}'. Must be 'create_earning' or 'approve_earning'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for payroll earning operations"
            })
        
        payroll_earnings = data.get("payroll_earnings", {})
        payroll_inputs = data.get("payroll_inputs", {})
        employees = data.get("employees", {})
        users = data.get("users", {})
        audit_trails = data.get("audit_trails", {})
        
        if operation_type == "create_earning":
            # Validate mandatory fields and identify missing ones
            required_fields = {
                "payroll_input_id": payroll_input_id,
                "earning_type": earning_type,
                "amount": amount,
                "user_id": user_id
            }
            missing_fields = [field for field, value in required_fields.items() if value is None]
            
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Missing mandatory fields - {', '.join(missing_fields)} are required"
                })
            
            # Verify the user is an active HR Payroll Administrator, HR Manager, or HR Director
            if user_id not in users:
                return json.dumps({
                    "success": False,
                    "error": "Halt: User is not an active HR Payroll Administrator - user not found"
                })
            
            user = users[user_id]
            user_role = user.get("role")
            valid_roles = ["hr_payroll_administrator", "hr_manager", "hr_admin"]
            
            if user_role not in valid_roles:
                return json.dumps({
                    "success": False,
                    "error": "Halt: User is not an active HR Payroll Administrator - user must be HR Payroll Administrator, HR Manager, or HR Admin"
                })
            
            if user.get("employment_status") != "active":
                return json.dumps({
                    "success": False,
                    "error": "Halt: User is not an active HR Payroll Administrator - user is not active"
                })
            
            # Verify payroll_input_id exists and is approved
            if payroll_input_id not in payroll_inputs:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Payroll input not found or not approved - payroll input not found"
                })
            
            payroll_input = payroll_inputs[payroll_input_id]
            if payroll_input.get("input_status") != "submitted":
                return json.dumps({
                    "success": False,
                    "error": "Halt: Payroll input not found or not approved - payroll input is not approved"
                })
            
            # Validate earning_type
            valid_earning_types = ["bonus", "incentive", "reimbursement", "commission", "other"]
            if earning_type not in valid_earning_types:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Invalid earning_type - must be one of: {', '.join(valid_earning_types)}"
                })
            
            # Validate amount
            if not is_valid_amount(amount):
                return json.dumps({
                    "success": False,
                    "error": "Halt: Amount ≤ 0 - amount must be positive"
                })
            
            # Generate new earning ID
            new_earning_id = generate_id(payroll_earnings)
            
            # Create payroll earning
            new_earning = {
                "earning_id": new_earning_id,
                "payroll_input_id": payroll_input_id,
                "earning_type": earning_type,
                "amount": amount,
                "approval_status": "pending",
                "approved_by": None,
                "approval_date": None,
                "created_at": "2025-10-01T12:00:00"
            }
            
            payroll_earnings[new_earning_id] = new_earning
            
            # Create audit entry for earning creation
            audit_id = generate_id(audit_trails)
            audit_entry = {
                "audit_id": audit_id,
                "reference_id": new_earning_id,
                "reference_type": "payroll",
                "action": "create",
                "user_id": user_id,
                "field_name": None,
                "old_value": None,
                "new_value": json.dumps(new_earning),
                "created_at": "2025-10-01T12:00:00"
            }
            audit_trails[audit_id] = audit_entry
            
            return json.dumps({
                "success": True,
                "operation": "create_earning",
                "earning_id": new_earning_id,
                "message": f"Payroll earning {new_earning_id} created successfully",
                "earning_data": new_earning
            })
        
        elif operation_type == "approve_earning":
            # Validate mandatory fields for approval and identify missing ones
            required_fields = {
                "earning_id": earning_id,
                "approval_status": approval_status,
                "approved_by": approved_by,
                "approval_date": approval_date
            }
            missing_fields = [field for field, value in required_fields.items() if value is None]
            
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Missing mandatory fields - {', '.join(missing_fields)} are required"
                })
            
            # Verify earning exists and is in 'pending' status
            if earning_id not in payroll_earnings:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Earning not found or not in 'pending' status - earning not found"
                })
            
            earning = payroll_earnings[earning_id]
            if earning.get("approval_status") != "pending":
                return json.dumps({
                    "success": False,
                    "error": "Halt: Earning not found or not in 'pending' status - earning is not in pending status"
                })
            
            # Confirm approver exists and is active
            if approved_by not in users:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Approver not authorized - approver not found"
                })
            
            approver = users[approved_by]
            if approver.get("employment_status") != "active":
                return json.dumps({
                    "success": False,
                    "error": "Halt: Approver not authorized - approver is not active"
                })
            
            # Confirm approver is the employee's manager
            payroll_input_id = earning.get("payroll_input_id")
            if payroll_input_id not in payroll_inputs:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Approver not authorized - payroll input not found"
                })
            
            payroll_input = payroll_inputs[payroll_input_id]
            employee_id = payroll_input.get("employee_id")
            
            if employee_id not in employees:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Approver not authorized - employee not found"
                })
            
            employee = employees[employee_id]
            if employee.get("manager_id") != approved_by:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Approver not authorized - approver is not the employee's manager"
                })
            
            # Validate approval status
            valid_approval_statuses = ["approved", "rejected"]
            if approval_status not in valid_approval_statuses:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Invalid approval_status - must be one of: {', '.join(valid_approval_statuses)}"
                })
            
            # Update payroll earning with approval details
            updated_earning = earning.copy()
            updated_earning.update({
                "approval_status": approval_status,
                "approved_by": approved_by,
                "approval_date": approval_date
            })
            
            payroll_earnings[earning_id] = updated_earning
            
            # Create audit entry for approval
            audit_id = generate_id(audit_trails)
            audit_entry = {
                "audit_id": audit_id,
                "reference_id": earning_id,
                "reference_type": "payroll",
                "action": "approve" if approval_status == "approved" else "reject",
                "user_id": approved_by,
                "field_name": "approval_status",
                "old_value": "pending",
                "new_value": approval_status,
                "created_at": "2025-10-01T12:00:00"
            }
            audit_trails[audit_id] = audit_entry
            
            return json.dumps({
                "success": True,
                "operation": "approve_earning",
                "earning_id": earning_id,
                "message": f"Payroll earning {earning_id} {approval_status} successfully",
                "earning_data": updated_earning
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manage_payroll_earning_operations",
				"description": "Create and approve additional earnings (bonuses, incentives, reimbursements, commissions) tied to approved payroll inputs.\n\nWhat this tool does:\n- create_earning: Adds an earning line item for an employee against an approved payroll input.\n- approve_earning: Lets the employee's manager approve or reject the earning.\n\nWho can use it:\n- create_earning: Active users with role in {hr_payroll_administrator, hr_manager, hr_admin}.\n- approve_earning: The employee's manager (active user matching employees[payroll_input.employee_id].manager_id).\n\nInput guidance:\n- operation_type: 'create_earning' or 'approve_earning'.\n- For create_earning:\n  - payroll_input_id: Existing payroll input with input_status 'submitted'.\n \n  - earning_type: One of bonus, incentive, reimbursement, commission, other.\n  - amount: Positive number (> 0).\n  - user_id: Authorized active user id.\n- For approve_earning:\n  - earning_id: Existing earning with approval_status 'pending'.\n  - approval_status: 'approved' or 'rejected'.\n  - approved_by: Active user id who is the employee's manager.\n  - approval_date: YYYY-MM-DD.\n\nExample create_earning:\n{\n  \"operation_type\": \"create_earning\",\n  \"payroll_input_id\": \"pi_55\",\n  \"earning_type\": \"bonus\",\n  \"amount\": 500,\n  \"user_id\": \"u_hr_1\"\n}\n\nExample approve_earning:\n{\n  \"operation_type\": \"approve_earning\",\n  \"earning_id\": \"pe_77\",\n  \"approval_status\": \"approved\",\n  \"approved_by\": \"u_mgr_7\",\n  \"approval_date\": \"2025-01-12\"\n}\n\nTypical errors if inputs are incorrect:\n- Missing mandatory fields for the chosen operation.\n- Requester not authorized or inactive.\n- Payroll input not found/not approved; employee mismatch with payroll input.\n- Invalid earning_type or non-positive amount.\n- For approval: approver not employee's manager; earning not pending; invalid approval status.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation_type": {
                            "type": "string",
							"description": "Operation to execute. Use 'create_earning' to add an earning; 'approve_earning' for manager decision.",
                            "enum": ["create_earning", "approve_earning"]
                        },
                        "payroll_input_id": {
                            "type": "string",
							"description": "Payroll input id (required for create_earning). Must exist and have input_status 'submitted'."
                        },
                        "earning_type": {
                            "type": "string",
							"description": "Type of earning (required for create_earning). Allowed: bonus, incentive, reimbursement, commission, other.",
                            "enum": ["bonus", "incentive", "reimbursement", "commission", "other"]
                        },
                        "amount": {
                            "type": "number",
							"description": "Earning amount (required for create_earning). Must be a positive number (> 0)."
                        },
                        "user_id": {
                            "type": "string",
							"description": "Requester user id (required for create_earning). Must exist, be 'active', and role in {hr_payroll_administrator, hr_manager, hr_admin}."
                        },
                        "earning_id": {
                            "type": "string",
							"description": "Payroll earning id (required for approve_earning). Must exist and be in 'pending' status."
                        },
                        "approval_status": {
                            "type": "string",
							"description": "Manager decision (required for approve_earning). Choose 'approved' or 'rejected'.",
                            "enum": ["approved", "rejected"]
                        },
                        "approved_by": {
                            "type": "string",
							"description": "Approver user id (required for approve_earning). Must be the employee's manager and 'active'."
                        },
                        "approval_date": {
                            "type": "string",
							"description": "Approval date (YYYY-MM-DD, required for approve_earning)."
                        }
                    },
                    "required": ["operation_type"]
                }
            }
        }
