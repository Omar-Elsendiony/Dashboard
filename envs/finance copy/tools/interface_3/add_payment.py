import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class add_payment(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], invoice_id: str, payment_date: str, 
               amount: float, payment_method: str, status: str = 'completed') -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return '1'
            return str(max(int(k) for k in table.keys()) + 1)
        
        invoices = data.get("invoices", {})
        payments = data.get("payments", {})
        
        # Validate invoice exists
        if str(invoice_id) not in invoices:
            raise ValueError(f"Invoice {invoice_id} not found")
        
        # Validate payment method
        valid_methods = ["wire", "cheque", "credit_card", "bank_transfer"]
        if payment_method not in valid_methods:
            raise ValueError(f"Invalid payment method. Must be one of {valid_methods}")
        
        valid_statuses = ['draft', 'completed','failed']
        if status not in valid_statuses:
            raise ValueError(f"Invalid payment status. Must be one of {valid_statuses}")
        
        payment_id = generate_id(payments)
        timestamp = "2025-08-07T00:00:00Z"
        
        new_payment = {
            "payment_id": payment_id,
            "invoice_id": invoice_id,
            "payment_date": payment_date,
            "amount": round(float(amount), 2),
            "payment_method": payment_method,
            "status": status,
            "created_at": timestamp
        }
        
        payments[str(payment_id)] = new_payment
        return json.dumps(new_payment)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_payment",
                "description": "Add a payment for an invoice",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "invoice_id": {"type": "string", "description": "ID of the invoice"},
                        "payment_date": {"type": "string", "description": "Payment date in ISO format"},
                        "amount": {"type": "number", "description": "Payment amount"},
                        "payment_method": {"type": "string", "description": "Payment method (wire, cheque, credit_card, bank_transfer)"},
                        "status": {"type": "string", "description": "Payment status (draft, completed, failed)"}
                    },
                    "required": ["invoice_id", "payment_date", "amount", "payment_method"]
                }
            }
        }
