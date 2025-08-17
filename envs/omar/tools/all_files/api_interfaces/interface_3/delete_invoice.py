import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class DeleteInvoice(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], invoice_id: str) -> str:
        invoices = data.get("invoices", {})
        payments = data.get("payments", {})
        
        # Validate invoice exists
        if str(invoice_id) not in invoices:
            raise ValueError(f"Invoice {invoice_id} not found")
        
        # Check if invoice has associated payments
        for payment in payments.values():
            if payment.get("invoice_id") == invoice_id:
                raise ValueError(f"Cannot delete invoice {invoice_id} - it has associated payments")
        
        # Delete the invoice
        deleted_invoice = invoices.pop(str(invoice_id))
        
        return json.dumps({
            "status": "deleted",
            "deleted_invoice": deleted_invoice
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "delete_invoice",
                "description": "Delete an invoice (only if no payments are associated)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "invoice_id": {"type": "string", "description": "ID of the invoice to delete"}
                    },
                    "required": ["invoice_id"]
                }
            }
        }
