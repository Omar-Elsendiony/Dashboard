import json
import uuid
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class SubmitInvoicePayment(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        invoice_id: str = None,
        payment_id: str = None,
        worker_id: str = None,
        amount: float = None,
        issue_date: str = None,
        due_date: str = None,
        status: str = None,
        currency: str = None,
        organization_id: str = None
    ) -> str:
        invoices = data.setdefault("invoices", {})
        payments = data.setdefault("payments", {})

        # Generate invoice ID if not provided
        if invoice_id is None:
            invoice_id = str(uuid.uuid4())

        # Use existing invoice or initialize new one
        invoice = invoices.get(invoice_id, {})

        # Set or update invoice fields
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
        else:
            invoice["status"] = "paid"
        if currency is not None:
            invoice["currency"] = currency
        if organization_id is not None:
            invoice["organization_id"] = organization_id

        # Save or update invoice
        invoices[invoice_id] = invoice

        # Link and complete payment if provided
        if payment_id:
            if payment_id not in payments:
                raise ValueError("Payment not found")
            payment = payments[payment_id]
            payment["invoice_id"] = invoice_id
            payment["status"] = "completed"

        return json.dumps({
            "invoice_id": invoice_id,
            **invoice
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "submit_invoice_payment",
                "description": (
                    "Creates or updates an invoice. If no invoice ID is provided, a new one is generated. "
                    "If a payment ID is given, it links the payment to the invoice and marks it as completed."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "invoice_id": {
                            "type": "string",
                            "description": "The ID of the invoice to update (if omitted, a new one is created)"
                        },
                        "payment_id": {
                            "type": "string",
                            "description": "Optional payment ID to link and mark as completed"
                        },
                        "worker_id": {
                            "type": "string",
                            "description": "Worker associated with the invoice"
                        },
                        "amount": {
                            "type": "number",
                            "description": "Total invoice amount"
                        },
                        "issue_date": {
                            "type": "string",
                            "description": "Invoice issue timestamp (ISO 8601 format)"
                        },
                        "due_date": {
                            "type": "string",
                            "description": "Invoice due timestamp (ISO 8601 format)"
                        },
                        "status": {
                            "type": "string",
                            "description": "Invoice status (default is 'paid' if not supplied)"
                        },
                        "currency": {
                            "type": "string",
                            "description": "Currency of the invoice (e.g., USD, INR)"
                        },
                        "organization_id": {
                            "type": "string",
                            "description": "Organization ID associated with the invoice"
                        }
                    },
                    "required": []
                }
            }
        }
