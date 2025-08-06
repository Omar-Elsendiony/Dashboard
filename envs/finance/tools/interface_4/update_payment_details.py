import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class update_payment_details(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        payment_id: str,
        amount: Optional[str] = None,
        payment_method: Optional[str] = None,
        status: Optional[str] = None
    ) -> str:
        payments = data.get("payments", {})

        # Validate payment exists
        if payment_id not in payments:
            raise ValueError(f"Payment {payment_id} not found")
        payment = payments[payment_id]

        # Update amount if provided
        if amount is not None:
            payment["amount"] = amount

        # Update payment_method if provided
        if payment_method is not None:
            valid_methods = ["wire", "cheque", "credit_card", "bank_transfer"]
            if payment_method not in valid_methods:
                raise ValueError(f"Invalid payment method. Must be one of {valid_methods}")
            payment["payment_method"] = payment_method

        # Update status if provided
        if status is not None:
            valid_statuses = ["draft", "completed", "failed"]
            if status not in valid_statuses:
                raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
            payment["status"] = status

        return json.dumps(payment)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_payment_details",
                "description": "Update one or more fields of a payment; only provided fields will change.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "payment_id": {
                            "type": "string",
                            "description": "ID of the payment to update"
                        },
                        "amount": {
                            "type": "string",
                            "description": "New payment amount (optional)"
                        },
                        "payment_method": {
                            "type": "string",
                            "description": "New payment method (wire, cheque, credit_card, bank_transfer; optional)"
                        },
                        "status": {
                            "type": "string",
                            "description": "New payment status (draft, completed, failed; optional)"
                        }
                    },
                    "required": ["payment_id"]
                }
            }
        }