import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class RecordPayment(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], payment_id: str, status: str) -> str:
        payments = data.get("payments", {})
        
        # Validate payment exists
        if str(payment_id) not in payments:
            raise ValueError(f"Payment {payment_id} not found")
        
        # Validate status
        valid_statuses = ["draft", "completed", "failed"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        payment = payments[str(payment_id)]
        payment["status"] = status
        
        # If completing payment, update related invoice status
        if status == "completed":
            invoices = data.get("invoices", {})
            invoice_id = payment.get("invoice_id")
            if invoice_id and str(invoice_id) in invoices:
                invoices[str(invoice_id)]["status"] = "paid"
                invoices[str(invoice_id)]["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps({
            "payment_id": payment_id,
            "status": status,
            "message": f"Payment {payment_id} status updated to {status}"
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "record_payment",
                "description": "Record the final status of a payment for transaction settlement",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "payment_id": {"type": "string", "description": "ID of the payment to update"},
                        "status": {"type": "string", "description": "Final payment status (draft, completed, failed)"}
                    },
                    "required": ["payment_id", "status"]
                }
            }
        }
