import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class ListExpenseReimbursements(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], reimbursement_id: str = None, 
               employee_id: str = None, expense_type: str = None, 
               status: str = None) -> str:
        expense_reimbursements = data.get("expense_reimbursements", {})
        results = []
        
        for reimbursement in expense_reimbursements.values():
            if reimbursement_id and reimbursement.get("reimbursement_id") != reimbursement_id:
                continue
            if employee_id and reimbursement.get("employee_id") != employee_id:
                continue
            if expense_type and reimbursement.get("expense_type") != expense_type:
                continue
            if status and reimbursement.get("status") != status:
                continue
            results.append(reimbursement)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_expense_reimbursements",
                "description": "Retrieve expense reimbursements with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reimbursement_id": {"type": "string", "description": "Filter by reimbursement ID"},
                        "employee_id": {"type": "string", "description": "Filter by employee ID"},
                        "expense_type": {"type": "string", "description": "Filter by expense type"},
                        "status": {"type": "string", "description": "Filter by status"}
                    },
                    "required": []
                }
            }
        }
