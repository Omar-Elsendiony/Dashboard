import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateCommitmentInvoice(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], commitment_id: str, invoice_date: str,
               commitment_due_date: str, commitment_amount: float, commitment_status: str = "issued") -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        commitments = data.get("commitments", {})
        invoices = data.get("invoices", {})
        
        # Validate commitment exists
        if str(commitment_id) not in commitments:
            raise ValueError(f"Commitment {commitment_id} not found")
        
        # Validate commitment_status
        valid_statuses = ["issued", "paid"]
        if commitment_status not in valid_statuses:
            raise ValueError(f"Invalid commitment_status. Must be one of {valid_statuses}")
        
        # Validate commitment_amount is positive
        if commitment_amount <= 0:
            raise ValueError("Amount must be positive")
        
        commitment_invoice_id = generate_id(invoices)
        timestamp = "2025-10-01T00:00:00"
        
        new_invoice = {
            "commitment_invoice_id": str(commitment_invoice_id),
            "commitment_id": commitment_id,
            "invoice_date": invoice_date,
            "commitment_due_date": commitment_due_date,
            "commitment_amount": commitment_amount,
            "commitment_status": commitment_status,
            "updated_at": timestamp
        }
        
        invoices[str(commitment_invoice_id)] = new_invoice
        return json.dumps(new_invoice)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_invoice",
                "description": "Create a new invoice for a commitment",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "commitment_id": {"type": "string", "description": "ID of the commitment"},
                        "invoice_date": {"type": "string", "description": "Invoice date in YYYY-MM-DD format"},
                        "commitment_due_date": {"type": "string", "description": "Due date in YYYY-MM-DD format"},
                        "commitment_amount": {"type": "number", "description": "Invoice commitment_amount"},
                        "commitment_status": {"type": "string", "description": "Invoice commitment_status (issued, paid), defaults to issued"}
                    },
                    "required": ["commitment_id", "invoice_date", "commitment_due_date", "commitment_amount"]
                }
            }
        }
