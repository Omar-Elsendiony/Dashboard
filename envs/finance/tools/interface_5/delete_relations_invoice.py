import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class DeleteRelationsInvoice(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], relations_invoice_id: str) -> str:
        invoices = data.get("invoices", {})
        payments = data.get("payments", {})
        
        # Validate invoice exists
        if str(relations_invoice_id) not in invoices:
            raise ValueError(f"Invoice {relations_invoice_id} not found")
        
        # Check if invoice has associated payments
        for payment in payments.values():
            if payment.get("relations_invoice_id") == relations_invoice_id:
                raise ValueError(f"Cannot delete invoice {relations_invoice_id} - it has associated payments")
        
        # Delete the invoice
        deleted_invoice = invoices.pop(str(relations_invoice_id))
        
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
                        "relations_invoice_id": {"type": "string", "description": "ID of the invoice to delete"}
                    },
                    "required": ["relations_invoice_id"]
                }
            }
        }
