import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ListInvoices(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        invoice_id: str = None,
        worker_id: str = None,
        organization_id: str = None,
        status: str = None,
        currency: str = None,
        issue_date: str = None,
        due_date: str = None
    ) -> str:
        invoices = data.get("invoices", {})

        def matches(iid, invoice):
            if invoice_id and iid != invoice_id:
                return False
            if worker_id and invoice.get("worker_id") != worker_id:
                return False
            if organization_id and invoice.get("organization_id") != organization_id:
                return False
            if status and invoice.get("status") != status:
                return False
            if currency and invoice.get("currency") != currency:
                return False
            if issue_date and invoice.get("issue_date") != issue_date:
                return False
            if due_date and invoice.get("due_date") != due_date:
                return False
            return True

        filtered = [
            {**invoice, "invoice_id": iid}
            for iid, invoice in invoices.items()
            if matches(iid, invoice)
        ]

        return json.dumps(filtered)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_invoices",
                "description": (
                    "Fetches a list of invoices with optional filters. "
                    "Supports filtering by invoice_id (key), worker_id, organization_id, "
                    "status (e.g., paid, unpaid), currency, issue_date, and due_date."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "invoice_id": {
                            "type": "string",
                            "description": "Filter by invoice ID (key)"
                        },
                        "worker_id": {
                            "type": "string",
                            "description": "Filter by worker ID"
                        },
                        "organization_id": {
                            "type": "string",
                            "description": "Filter by organization ID"
                        },
                        "status": {
                            "type": "string",
                            "description": "Filter by invoice status (e.g., paid, pending)"
                        },
                        "currency": {
                            "type": "string",
                            "description": "Filter by currency code"
                        },
                        "issue_date": {
                            "type": "string",
                            "description": "Filter by issue date (ISO format: YYYY-MM-DDTHH:MM:SSZ)"
                        },
                        "due_date": {
                            "type": "string",
                            "description": "Filter by due date (ISO format: YYYY-MM-DDTHH:MM:SSZ)"
                        }
                    },
                    "required": []
                }
            }
        }
