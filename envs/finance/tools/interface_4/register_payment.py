import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class register_payment(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        invoice_id: str,
        payment_date: str,
        amount: float,
        payment_method: str,
        status: Optional[str] = None
    ) -> str:
        def generate_id(table: Dict[str, Any]) -> str:
            return str(max((int(k) for k in table.keys()), default=0) + 1)

        invoices = data.get("invoices", {})
        payments = data.setdefault("payments", {})

        # Validate invoice exists
        if invoice_id not in invoices:
            raise ValueError(f"Invoice {invoice_id} not found")

        # Validate payment method
        valid_methods = ["wire", "cheque", "credit_card", "bank_transfer"]
        if payment_method not in valid_methods:
            raise ValueError(f"Invalid payment method. Must be one of {valid_methods}")

        # Determine and validate status
        valid_statuses = ["draft", "completed", "failed"]
        st = status or "completed"
        if st not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")

        payment_id = generate_id(payments)
        timestamp = "2025-08-07T00:00:00Z"

        new_payment = {
            "payment_id": payment_id,
            "invoice_id": invoice_id,
            "payment_date": payment_date,
            "amount": round(float(amount), 2),
            "payment_method": payment_method,
            "status": st,
            "created_at": timestamp
        }

        payments[payment_id] = new_payment
        return json.dumps(new_payment)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "register_payment",
                "description": "Register a new payment; status is optional (defaults to 'completed').",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "invoice_id": {
                            "type": "string",
                            "description": "ID of the invoice"
                        },
                        "payment_date": {
                            "type": "string",
                            "description": "Payment date in ISO format"
                        },
                        "amount": {
                            "type": "number",
                            "description": "Payment amount"
                        },
                        "payment_method": {
                            "type": "string",
                            "description": "Payment method (wire, cheque, credit_card, bank_transfer)"
                        },
                        "status": {
                            "type": "string",
                            "description": "Payment status (draft, completed, failed); defaults to 'completed'"
                        }
                    },
                    "required": ["invoice_id", "payment_date", "amount", "payment_method"]
                }
            }
        }