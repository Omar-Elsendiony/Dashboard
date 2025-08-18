import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateCommitmentInvoice(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], commitment_invoice_id: str, 
               invoice_date: Optional[str] = None, commitment_due_date: Optional[str] = None,
               commitment_amount: Optional[float] = None, commitment_status: Optional[str] = None) -> str:
        invoices = data.get("invoices", {})
        
        # Validate invoice exists
        if str(commitment_invoice_id) not in invoices:
            raise ValueError(f"Invoice {commitment_invoice_id} not found")
        
        invoice = invoices[str(commitment_invoice_id)]
        
        # Validate commitment_status if provided
        if commitment_status:
            valid_statuses = ["issued", "paid"]
            if commitment_status not in valid_statuses:
                raise ValueError(f"Invalid commitment_status. Must be one of {valid_statuses}")
        
        # Validate commitment_amount if provided
        if commitment_amount is not None and commitment_amount <= 0:
            raise ValueError("Amount must be positive")
        
        # Update fields
        if invoice_date:
            invoice["invoice_date"] = invoice_date
        if commitment_due_date:
            invoice["commitment_due_date"] = commitment_due_date
        if commitment_amount is not None:
            invoice["commitment_amount"] = commitment_amount
        if commitment_status:
            invoice["commitment_status"] = commitment_status
        
        invoice["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps(invoice)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_invoice",
                "description": "Update an existing invoice",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "commitment_invoice_id": {"type": "string", "description": "ID of the invoice to update"},
                        "invoice_date": {"type": "string", "description": "New invoice date in YYYY-MM-DD format"},
                        "commitment_due_date": {"type": "string", "description": "New due date in YYYY-MM-DD format"},
                        "commitment_amount": {"type": "number", "description": "New invoice commitment_amount"},
                        "commitment_status": {"type": "string", "description": "New commitment_status (issued, paid)"}
                    },
                    "required": ["commitment_invoice_id"]
                }
            }
        }
