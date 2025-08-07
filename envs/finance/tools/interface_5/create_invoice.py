import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class create_invoice(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        fund_id: str,
        investor_id: str,
        invoice_date: str,
        due_date: str,
        amount: float,
        currency: str,
        payment_type: Optional[str] = "manual",
        commitment_id: Optional[str] = None
    ) -> str:
        def generate_id(table: Dict[str, Any]) -> int:
            return max((int(k) for k in table.keys()), default=0) + 1

        invoices = data.setdefault("invoices", {})
        funds = data.get("funds", {})
        investors = data.get("investors", {})
        commitments = data.get("commitments", {})

        # Validate fund exists
        if fund_id not in funds:
            raise ValueError(f"Fund {fund_id} not found")

        # Validate investor exists
        if investor_id not in investors:
            raise ValueError(f"Investor {investor_id} not found")

        # Validate commitment if provided
        if commitment_id is not None and commitment_id not in commitments:
            raise ValueError(f"Commitment {commitment_id} not found")

        # Validate currency
        valid_currencies = ["USD", "EUR", "GBP", "NGN"]
        if currency not in valid_currencies:
            raise ValueError(f"Invalid currency. Must be one of {valid_currencies}")

        # Validate payment_type
        valid_payment_types = ["auto-pay", "manual"]
        if payment_type not in valid_payment_types:
            raise ValueError(f"Invalid payment_type. Must be one of {valid_payment_types}")

        invoice_id = generate_id(invoices)
        timestamp = "2025-08-07T00:00:00Z"

        new_invoice = {
            "invoice_id": str(invoice_id),
            "fund_id": fund_id,
            "investor_id": investor_id,
            "commitment_id": commitment_id,
            "invoice_date": invoice_date,
            "due_date": due_date,
            "amount": round(float(amount), 2),
            "payment_type": payment_type,
            "currency": currency,
            "status": "issued",
            "updated_at": timestamp
        }

        invoices[str(invoice_id)] = new_invoice
        return json.dumps(new_invoice)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_invoice",
                "description": (
                    "Create a new invoice. Provide fund_id, investor_id, "
                    "invoice_date, due_date, amount, currency, and optional payment_type "
                    "(defaults to 'manual')."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {
                            "type": "string",
                            "description": "ID of the fund"
                        },
                        "investor_id": {
                            "type": "string",
                            "description": "ID of the investor"
                        },
                        "commitment_id": {
                            "type": "string",
                            "description": "ID of the commitment (optional)"
                        },
                        "invoice_date": {
                            "type": "string",
                            "description": "Invoice date (YYYY-MM-DD)"
                        },
                        "due_date": {
                            "type": "string",
                            "description": "Due date (YYYY-MM-DD)"
                        },
                        "amount": {
                            "type": "number",
                            "description": "Invoice amount"
                        },
                        "currency": {
                            "type": "string",
                            "description": "Currency (USD, EUR, GBP, NGN)"
                        },
                        "payment_type": {
                            "type": "string",
                            "description": "Payment type (auto-pay or manual), defaults to 'manual'"
                        }
                    },
                    "required": [
                        "fund_id",
                        "investor_id",
                        "invoice_date",
                        "due_date",
                        "amount",
                        "currency"
                    ]
                }
            }
        }