
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ExecutePayrollDeduction(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, deduction_data: Dict[str, Any] = None) -> str:
        """
        Create payroll deduction records. Updates are not supported as per schema design.
        """
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        if action not in ["create"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid action '{action}'. Only 'create' is supported for payroll deductions"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for payroll deductions"
            })
        
        payroll_deductions = data.get("payroll_deductions", {})
        payroll_records = data.get("payroll_records", {})
        users = data.get("users", {})
        
        if action == "create":
            if not deduction_data:
                return json.dumps({
                    "success": False,
                    "error": "deduction_data is required for create action"
                })
            
            # Validate required fields
            required_fields = ["payroll_id", "deduction_type", "amount", "created_by"]
            missing_fields = [field for field in required_fields if field not in deduction_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Payroll record not found - missing fields: {', '.join(missing_fields)}"
                })
            
            # Validate that payroll record exists in the system
            payroll_id = str(deduction_data["payroll_id"])
            if payroll_id not in payroll_records:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Payroll record not found"
                })
            
            # Validate that creator exists in the user system
            created_by = str(deduction_data["created_by"])
            if created_by not in users:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Creator not found"
                })
            
            # Validate deduction_type enum according to schema
            valid_types = ["tax", "insurance", "retirement", "garnishment", "equipment", "other"]
            if deduction_data["deduction_type"] not in valid_types:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Invalid deduction type or amount - deduction_type must be one of: {', '.join(valid_types)}"
                })
            
            # Validate amount is positive monetary value
            try:
                amount = float(deduction_data["amount"])
                if amount <= 0:
                    return json.dumps({
                        "success": False,
                        "error": "Halt: Invalid deduction type or amount - amount must be positive"
                    })
            except (ValueError, TypeError):
                return json.dumps({
                    "success": False,
                    "error": "Halt: Invalid deduction type or amount - invalid amount format"
                })
            
            # Validate only allowed fields are present
            allowed_fields = ["payroll_id", "deduction_type", "amount", "created_by"]
            invalid_fields = [field for field in deduction_data.keys() if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for payroll deduction creation: {', '.join(invalid_fields)}"
                })
            
            # Generate new deduction ID
            new_deduction_id = generate_id(payroll_deductions)
            
            # Create new deduction record
            new_deduction = {
                "deduction_id": str(new_deduction_id),
                "payroll_id": payroll_id,
                "deduction_type": deduction_data["deduction_type"],
                "amount": deduction_data["amount"],
                "created_by": created_by,
                "created_at": "2025-10-01T12:00:00"
            }
            
            payroll_deductions[str(new_deduction_id)] = new_deduction
            
            return json.dumps({
                "success": True,
                "action": "create",
                "deduction_id": str(new_deduction_id),
                "message": f"Payroll deduction {new_deduction_id} created successfully",
                "deduction_data": new_deduction
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "execute_payroll_deduction",
                "description": "Create payroll deduction records in the HR payroll system. This tool manages payroll deductions with comprehensive validation and data integrity checks. Establishes new deductions with proper validation of payroll record existence, creator verification, deduction type compliance. Validates deduction amounts are positive monetary values, ensures payroll record exists, and verifies creator exists in user system. Essential for payroll processing, deduction management, and maintaining accurate payroll records.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' to establish new payroll deduction",
                            "enum": ["create"]
                        },
                        "deduction_data": {
                            "type": "object",
                            "description": "Deduction data object. For create: requires payroll_id (must exist), deduction_type, amount (positive), created_by (must exist in users). SYNTAX: {\"key\": \"value\"}",
                            "properties": {
                                "payroll_id": {
                                    "type": "string",
                                    "description": "Payroll record identifier (required for create, must exist in system)"
                                },
                                "deduction_type": {
                                    "type": "string",
                                    "description": "Type of payroll deduction",
                                    "enum": ["tax", "insurance", "retirement", "garnishment", "equipment", "other"]
                                },
                                "amount": {
                                    "type": "number",
                                    "description": "Deduction amount (must be positive monetary value)"
                                },
                                "created_by": {
                                    "type": "string",
                                    "description": "User who created the deduction (required for create, must exist in user system)"
                                }
                            }
                        }
                    },
                    "required": ["action"]
                }
            }
        }

