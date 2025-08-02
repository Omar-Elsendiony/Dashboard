import json
import uuid
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreatePayment(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        user_id: str,
        invoice_id: str,
        amount: float,
        currency: str
    ) -> str:
        payments = data.setdefault("payments", {})
        payment_id = str(uuid.uuid4())

        payments[payment_id] = {
            "user_id": user_id,
            "invoice_id": invoice_id,
            "amount": round(amount, 2),
            "status": "pending",
            "currency": currency,
            "processed_at": None
        }

        return json.dumps({
            "payment_id": payment_id,
            **payments[payment_id]
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_payment",
                "description": "Creates a new pending payment entry linked to a user and invoice.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "User ID to whom the payment will be made"
                        },
                        "invoice_id": {
                            "type": "string",
                            "description": "Invoice ID for which the payment is being created"
                        },
                        "amount": {
                            "type": "number",
                            "description": "Amount to be paid"
                        },
                        "currency": {
                            "type": "string",
                            "description": "Currency code for the payment (e.g., USD, EUR)"
                        }
                    },
                    "required": ["user_id", "invoice_id", "amount", "currency"]
                }
            }
        }
