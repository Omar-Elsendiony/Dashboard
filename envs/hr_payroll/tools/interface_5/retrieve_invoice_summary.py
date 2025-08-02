import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool
from collections import defaultdict
from datetime import datetime

class RetrieveInvoiceSummary(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        organization_id: str = None,
        worker_id: str = None,
        status: str = None,
        currency: str = None,
        start_date: str = None,
        end_date: str = None,
        min_amount: float = None,
        max_amount: float = None
    ) -> str:
        invoices = data.get("invoices", {})
        summary = defaultdict(float)

        def matches(inv):
            if organization_id and inv.get("organization_id") != organization_id:
                return False
            if worker_id and inv.get("worker_id") != worker_id:
                return False
            if status and inv.get("status") != status:
                return False
            if currency and inv.get("currency") != currency:
                return False
            if start_date and inv.get("issue_date") < start_date:
                return False
            if end_date and inv.get("issue_date") > end_date:
                return False
            if min_amount is not None and inv.get("amount", 0) < min_amount:
                return False
            if max_amount is not None and inv.get("amount", 0) > max_amount:
                return False
            return True

        for invoice in invoices.values():
            if matches(invoice):
                summary[invoice["organization_id"]] += invoice.get("amount", 0)

        return json.dumps(dict(summary))

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "retrieve_invoice_summary",
                "description": (
                    "Fetches total invoice amounts grouped by organization, "
                    "with optional filters for organization, worker, status, currency, "
                    "issue_date range, and amount range."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "organization_id": {
                            "type": "string",
                            "description": "Filter by organization ID"
                        },
                        "worker_id": {
                            "type": "string",
                            "description": "Filter by worker ID"
                        },
                        "status": {
                            "type": "string",
                            "description": "Filter by invoice status (e.g., paid, overdue)"
                        },
                        "currency": {
                            "type": "string",
                            "description": "Filter by currency (e.g., USD, INR)"
                        },
                        "start_date": {
                            "type": "string",
                            "description": "Minimum issue_date (inclusive, ISO format)"
                        },
                        "end_date": {
                            "type": "string",
                            "description": "Maximum issue_date (inclusive, ISO format)"
                        },
                        "min_amount": {
                            "type": "number",
                            "description": "Minimum invoice amount"
                        },
                        "max_amount": {
                            "type": "number",
                            "description": "Maximum invoice amount"
                        }
                    },
                    "required": []
                }
            }
        }
