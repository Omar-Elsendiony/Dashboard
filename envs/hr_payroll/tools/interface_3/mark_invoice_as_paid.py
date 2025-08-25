import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class MarkInvoiceAsPaid(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], invoice_id: str, payment_id: str = None) -> str:
        invoices = data.get("invoices", {})
        payments = data.get("payments", {})

        if invoice_id not in invoices:
            raise ValueError("Invoice not found")

        # Validate payment if provided
        if payment_id:
            if payment_id not in payments:
                raise ValueError("Payment not found")
            if payments[payment_id].get("invoice_id") != invoice_id:
                raise ValueError("Payment does not match the invoice")

        invoices[invoice_id]["status"] = "paid"
        return json.dumps({
            "invoice_id": invoice_id,
            "status": "paid",
            **({"payment_id": payment_id} if payment_id else {})
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "mark_invoice_as_paid",
                "description": "Marks an invoice as paid. Optionally validates against a payment_id if provided.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "invoice_id": {
                            "type": "string",
                            "description": "ID of the invoice to be marked as paid"
                        },
                        "payment_id": {
                            "type": "string",
                            "description": "Optional ID of the payment used to pay the invoice"
                        }
                    },
                    "required": ["invoice_id"]
                }
            }
        }
