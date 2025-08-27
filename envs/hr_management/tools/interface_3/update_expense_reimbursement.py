import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateExpenseReimbursement(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], reimbursement_id: str, amount: float = None, 
               description: str = None, receipt_file_path: str = None) -> str:
        expense_reimbursements = data.get("expense_reimbursements", {})
        
        if reimbursement_id not in expense_reimbursements:
            raise ValueError(f"Expense reimbursement {reimbursement_id} not found")
        
        reimbursement = expense_reimbursements[reimbursement_id]
        
        # Only allow updates if status is submitted
        if reimbursement.get("status") != "submitted":
            raise ValueError("Cannot update expense reimbursement that is not in submitted status")
        
        if amount is not None:
            reimbursement["amount"] = amount
        
        if description is not None:
            reimbursement["description"] = description
        
        if receipt_file_path is not None:
            reimbursement["receipt_file_path"] = receipt_file_path
        
        reimbursement["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps({"message": "Expense reimbursement updated"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_expense_reimbursement",
                "description": "Update a submitted expense reimbursement",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reimbursement_id": {"type": "string", "description": "ID of the expense reimbursement to update"},
                        "amount": {"type": "number", "description": "Updated amount"},
                        "description": {"type": "string", "description": "Updated description"},
                        "receipt_file_path": {"type": "string", "description": "Updated receipt file path"}
                    },
                    "required": ["reimbursement_id"]
                }
            }
        }
