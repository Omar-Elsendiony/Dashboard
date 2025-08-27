import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class ProcessExpenseReimbursement(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], reimbursement_id: str, status: str, 
               approved_by: str = None, payment_date: str = None) -> str:
        expense_reimbursements = data.get("expense_reimbursements", {})
        users = data.get("users", {})
        
        if reimbursement_id not in expense_reimbursements:
            raise ValueError(f"Expense reimbursement {reimbursement_id} not found")
        
        if approved_by and approved_by not in users:
            raise ValueError(f"Approver user {approved_by} not found")
        
        valid_statuses = ["approved", "rejected", "paid"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        reimbursement = expense_reimbursements[reimbursement_id]
        reimbursement["status"] = status
        reimbursement["approved_by"] = approved_by
        reimbursement["updated_at"] = "2025-10-01T00:00:00"
        
        if payment_date and status == "paid":
            reimbursement["payment_date"] = payment_date
        
        return json.dumps({"message": f"Expense reimbursement {status}"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "process_expense_reimbursement",
                "description": "Process an expense reimbursement request",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reimbursement_id": {"type": "string", "description": "ID of the expense reimbursement"},
                        "status": {"type": "string", "description": "New status (approved, rejected, paid)"},
                        "approved_by": {"type": "string", "description": "ID of the user approving the request"},
                        "payment_date": {"type": "string", "description": "Payment date if status is paid (YYYY-MM-DD)"}
                    },
                    "required": ["reimbursement_id", "status"]
                }
            }
        }