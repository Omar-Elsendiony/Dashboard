import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class CreateExpenseReimbursement(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], employee_id: str, expense_date: str, 
               amount: float, expense_type: str, receipt_file_path: str = None) -> str:
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        employees = data.get("employees", {})
        expense_reimbursements = data.setdefault("expense_reimbursements", {})
        
        # Validate employee exists
        if employee_id not in employees:
            raise ValueError(f"Employee {employee_id} not found")
        
        # Validate expense type
        valid_expense_types = ["travel", "meals", "equipment", "training", "other"]
        if expense_type not in valid_expense_types:
            raise ValueError(f"Invalid expense type. Must be one of {valid_expense_types}")
        
        reimbursement_id = generate_id(expense_reimbursements)
        timestamp = "2025-10-01T00:00:00"
        
        new_reimbursement = {
            "reimbursement_id": reimbursement_id,
            "employee_id": employee_id,
            "expense_date": expense_date,
            "amount": amount,
            "expense_type": expense_type,
            "receipt_file_path": receipt_file_path,
            "status": "submitted",
            "approved_by": None,
            "payment_date": None,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        expense_reimbursements[reimbursement_id] = new_reimbursement
        return json.dumps({"reimbursement_id": reimbursement_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_expense_reimbursement",
                "description": "Create a new expense reimbursement request",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "employee_id": {"type": "string", "description": "ID of the employee"},
                        "expense_date": {"type": "string", "description": "Date of the expense"},
                        "amount": {"type": "number", "description": "Amount to be reimbursed"},
                        "expense_type": {"type": "string", "description": "Type of expense (travel, meals, equipment, training, other)"},
                        "receipt_file_path": {"type": "string", "description": "Path to receipt file (optional)"}
                    },
                    "required": ["employee_id", "expense_date", "amount", "expense_type"]
                }
            }
        }
