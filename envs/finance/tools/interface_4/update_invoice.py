import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class update_invoice(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        invoice_id: str,
        amount: Optional[float] = None,
        due_date: Optional[str] = None,
        status: Optional[str] = None
    ) -> str:
        invoices = data.get("invoices", {})

        # Ensure the invoice exists
        if invoice_id not in invoices:
            raise ValueError(f"Invoice {invoice_id} not found")
        invoice = invoices[invoice_id]

        # Update amount if provided
        if amount is not None:
            invoice["amount"] = round(float(amount), 2)

        # Update due_date if provided
        if due_date is not None:
            invoice["due_date"] = due_date

        # Update status if provided
        if status is not None:
            valid_statuses = ["issued", "paid"]
            if status not in valid_statuses:
                raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
            invoice["status"] = status

        # Bump updated_at only if any field changed
        if any(arg is not None for arg in (amount, due_date, status)):
            invoice["updated_at"] = "2025-08-07T00:00:00Z"

        return json.dumps(invoice)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_invoice",
                "description": (
                    "Update one or more fields of an invoice. "
                    "Provide invoice_id and any of: amount, due_date, status."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "invoice_id": {
                            "type": "string",
                            "description": "ID of the invoice to update"
                        },
                        "amount": {
                            "type": "number",
                            "description": "New invoice amount (optional)"
                        },
                        "due_date": {
                            "type": "string",
                            "description": "New due date in YYYY-MM-DD format (optional)"
                        },
                        "status": {
                            "type": "string",
                            "description": "New status (issued or paid; optional)"
                        }
                    },
                    "required": ["invoice_id"]
                }
            }
        }