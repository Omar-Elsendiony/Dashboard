import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class AddPayrollDeduction(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], payroll_id: str, deduction_type: str, 
               amount: float, created_by: str) -> str:
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        payroll_records = data.get("payroll_records", {})
        users = data.get("users", {})
        payroll_deductions = data.setdefault("payroll_deductions", {})
        
        # Validate payroll record exists
        if payroll_id not in payroll_records:
            raise ValueError(f"Payroll record {payroll_id} not found")
        
        # Validate user exists
        if created_by not in users:
            raise ValueError(f"User {created_by} not found")
        
        # Validate deduction type
        valid_deduction_types = ["tax", "insurance", "retirement", "garnishment", "equipment", "other"]
        if deduction_type not in valid_deduction_types:
            raise ValueError(f"Invalid deduction type. Must be one of {valid_deduction_types}")
        
        deduction_id = generate_id(payroll_deductions)
        timestamp = "2025-10-01T00:00:00"
        
        new_deduction = {
            "deduction_id": deduction_id,
            "payroll_id": payroll_id,
            "deduction_type": deduction_type,
            "amount": amount,
            "created_by": created_by,
            "created_at": timestamp
        }
        
        payroll_deductions[deduction_id] = new_deduction
        return json.dumps({"deduction_id": deduction_id})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_payroll_deduction",
                "description": "Add a deduction to a payroll record",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "payroll_id": {"type": "string", "description": "ID of the payroll record"},
                        "deduction_type": {"type": "string", "description": "Type of deduction (tax, insurance, retirement, garnishment, equipment, other)"},
                        "amount": {"type": "number", "description": "Deduction amount"},
                        "created_by": {"type": "string", "description": "ID of the user creating the deduction"}
                    },
                    "required": ["payroll_id", "deduction_type", "amount", "created_by"]
                }
            }
        }
