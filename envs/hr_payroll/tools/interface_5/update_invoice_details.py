import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdateInvoiceDetails(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        invoice_id: str,
        worker_id: str = None,
        amount: float = None,
        issue_date: str = None,
        due_date: str = None,
        status: str = None,
        currency: str = None,
        organization_id: str = None
    ) -> str:
        invoices = data.get("invoices", {})
        if invoice_id not in invoices:
            raise ValueError("Invoice not found")

        invoice = invoices[invoice_id]

        if worker_id is not None:
            invoice["worker_id"] = worker_id
        if amount is not None:
            invoice["amount"] = round(amount, 2)
        if issue_date is not None:
            invoice["issue_date"] = issue_date
        if due_date is not None:
            invoice["due_date"] = due_date
        if status is not None:
            invoice["status"] = status
        if currency is not None:
            invoice["currency"] = currency
        if organization_id is not None:
            invoice["organization_id"] = organization_id

        return json.dumps({
            "invoice_id": invoice_id,
            **invoice
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_invoice_details",
                "description": (
                    "Updates details of an existing invoice including amount, dates, status, currency, "
                    "organization ID, or associated worker."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "invoice_id": {
                            "type": "string",
                            "description": "The ID of the invoice to be updated"
                        },
                        "worker_id": {
                            "type": "string",
                            "description": "Updated worker ID associated with the invoice"
                        },
                        "amount": {
                            "type": "number",
                            "description": "Updated total amount for the invoice"
                        },
                        "issue_date": {
                            "type": "string",
                            "description": "Updated issue date in ISO 8601 format"
                        },
                        "due_date": {
                            "type": "string",
                            "description": "Updated due date in ISO 8601 format"
                        },
                        "status": {
                            "type": "string",
                            "description": "Updated invoice status (e.g., paid, overdue)"
                        },
                        "currency": {
                            "type": "string",
                            "description": "Updated currency code for the invoice"
                        },
                        "organization_id": {
                            "type": "string",
                            "description": "Updated organization ID linked to the invoice"
                        }
                    },
                    "required": ["invoice_id"]
                }
            }
        }
