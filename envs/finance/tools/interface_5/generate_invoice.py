import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GenerateInvoice(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], commitment_id: str, invoice_date: str,
               due_date: str, amount: float, status: str = "issued") -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        commitments = data.get("commitments", {})
        invoices = data.get("invoices", {})
        
        # Validate commitment exists
        if str(commitment_id) not in commitments:
            raise ValueError(f"Commitment {commitment_id} not found")
        
        # Validate status
        valid_statuses = ["issued", "paid"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        # Validate amount is positive
        if amount <= 0:
            raise ValueError("Amount must be positive")
        
        invoice_id = generate_id(invoices)
        timestamp = "2025-10-01T00:00:00"
        
        new_invoice = {
            "invoice_id": str(invoice_id),
            "commitment_id": commitment_id,
            "invoice_date": invoice_date,
            "due_date": due_date,
            "amount": amount,
            "status": status,
            "updated_at": timestamp
        }
        
        invoices[str(invoice_id)] = new_invoice
        return json.dumps(new_invoice)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "generate_invoice",
                "description": "Generate a new invoice for a commitment",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "commitment_id": {"type": "string", "description": "ID of the commitment"},
                        "invoice_date": {"type": "string", "description": "Invoice date in YYYY-MM-DD format"},
                        "due_date": {"type": "string", "description": "Due date in YYYY-MM-DD format"},
                        "amount": {"type": "number", "description": "Invoice amount"},
                        "status": {"type": "string", "description": "Invoice status (issued, paid), defaults to issued"}
                    },
                    "required": ["commitment_id", "invoice_date", "due_date", "amount"]
                }
            }
        }
