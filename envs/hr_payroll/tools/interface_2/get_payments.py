import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetPayments(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        payment_id: str = None,
        user_id: str = None,
        invoice_id: str = None,
        status: str = None,
        currency: str = None,
        processed_at: str = None,
        min_amount: float = None,
        max_amount: float = None
    ) -> str:
        payments = data.get("payments", {})

        def matches(pid, payment):
            if payment_id and pid != payment_id:
                return False
            if user_id and payment.get("user_id") != user_id:
                return False
            if invoice_id and payment.get("invoice_id") != invoice_id:
                return False
            if status and payment.get("status") != status:
                return False
            if currency and payment.get("currency") != currency:
                return False
            if processed_at and payment.get("processed_at") != processed_at:
                return False
            if min_amount is not None and payment.get("amount", 0) < min_amount:
                return False
            if max_amount is not None and payment.get("amount", 0) > max_amount:
                return False
            return True

        results = [
            {**payment, "payment_id": pid}
            for pid, payment in payments.items()
            if matches(pid, payment)
        ]
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_payments",
                "description": "Fetches a list of payments with optional filters on ID, user, invoice, status, currency, timestamp, and amount range.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "payment_id": {
                            "type": "string",
                            "description": "Filter by specific payment ID (primary key)"
                        },
                        "user_id": {
                            "type": "string",
                            "description": "Filter by user who received the payment"
                        },
                        "invoice_id": {
                            "type": "string",
                            "description": "Filter by associated invoice ID"
                        },
                        "status": {
                            "type": "string",
                            "description": "Filter by payment status (e.g., success, error)"
                        },
                        "currency": {
                            "type": "string",
                            "description": "Filter by currency code (e.g., USD, BRL)"
                        },
                        "processed_at": {
                            "type": "string",
                            "description": "Filter by exact processing date (ISO 8601 format)"
                        },
                        "min_amount": {
                            "type": "number",
                            "description": "Minimum payment amount"
                        },
                        "max_amount": {
                            "type": "number",
                            "description": "Maximum payment amount"
                        }
                    },
                    "required": []
                }
            }
        }
