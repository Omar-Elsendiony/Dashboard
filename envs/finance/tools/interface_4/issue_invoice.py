import json
from datetime import datetime
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class issue_invoice(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        fund_id: str,
        investor_id: str,
        commitment_id: str,
        invoice_date: str,
        due_date: str,
        amount: str,
        currency: str,
        payment_type: Optional[str] = None
    ) -> str:
        def generate_id(table: Dict[str, Any]) -> str:
            return str(max((int(k) for k in table.keys()), default=0) + 1)

        funds = data.get("funds", {})
        investors = data.get("investors", {})
        commitments = data.get("commitments", {})
        invoices = data.setdefault("invoices", {})

        # Validate fund exists
        if fund_id not in funds:
            raise ValueError(f"Fund {fund_id} not found")

        # Validate investor exists
        if investor_id not in investors:
            raise ValueError(f"Investor {investor_id} not found")

        # Validate commitment exists
        if commitment_id not in commitments:
            raise ValueError(f"Commitment {commitment_id} not found")

        # Validate currency
        valid_currencies = ["USD", "EUR", "GBP", "NGN"]
        if currency not in valid_currencies:
            raise ValueError(f"Invalid currency. Must be one of {valid_currencies}")

        # Determine payment_type
        valid_payment_types = ["auto-pay", "manual"]
        pt = payment_type or "manual"
        if pt not in valid_payment_types:
            raise ValueError(f"Invalid payment_type. Must be one of {valid_payment_types}")

        invoice_id = generate_id(invoices)
        timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

        new_invoice = {
            "invoice_id": invoice_id,
            "fund_id": fund_id,
            "investor_id": investor_id,
            "commitment_id": commitment_id,
            "invoice_date": invoice_date,
            "due_date": due_date,
            "amount": amount,
            "payment_type": pt,
            "currency": currency,
            "status": "issued",
            "updated_at": timestamp
        }

        invoices[invoice_id] = new_invoice
        return json.dumps(new_invoice)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "issue_invoice",
                "description": "Issue a new invoice; payment_type is optional and defaults to 'manual'.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "ID of the fund"},
                        "investor_id": {"type": "string", "description": "ID of the investor"},
                        "commitment_id": {"type": "string", "description": "ID of the commitment"},
                        "invoice_date": {"type": "string", "description": "Invoice date in YYYY-MM-DD format"},
                        "due_date": {"type": "string", "description": "Due date in YYYY-MM-DD format"},
                        "amount": {"type": "string", "description": "Invoice amount"},
                        "currency": {"type": "string", "description": "Currency (USD, EUR, GBP, NGN)"},
                        "payment_type": {
                            "type": "string",
                            "description": "Payment type (auto-pay or manual), defaults to manual"
                        }
                    },
                    "required": ["fund_id", "investor_id", "commitment_id", "invoice_date", "due_date", "amount", "currency"]
                }
            }
        }
