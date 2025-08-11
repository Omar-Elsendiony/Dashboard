import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool
from datetime import datetime

class GetFilteredInvoices(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        invoice_id: str = None,
        worker_id: str = None,
        organization_id: str = None,
        status: str = None,
        currency: str = None,
        amount: float = None,
        min_amount: float = None,
        max_amount: float = None,
        issue_date: str = None,
        issue_date_from: str = None,
        issue_date_to: str = None,
        due_date: str = None,
        due_date_from: str = None,
        due_date_to: str = None
    ) -> str:
        invoices = data.get("invoices", {})

        def in_range(val, min_val, max_val):
            return (min_val is None or val >= min_val) and (max_val is None or val <= max_val)

        def date_equals(date_str, target):
            try:
                return datetime.fromisoformat(date_str.replace("Z", "+00:00")) == datetime.fromisoformat(target.replace("Z", "+00:00"))
            except:
                return False

        def in_date_range(date_str, from_str, to_str):
            try:
                dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            except:
                return False
            if from_str:
                from_dt = datetime.fromisoformat(from_str.replace("Z", "+00:00"))
                if dt < from_dt:
                    return False
            if to_str:
                to_dt = datetime.fromisoformat(to_str.replace("Z", "+00:00"))
                if dt > to_dt:
                    return False
            return True

        result = []
        for inv_id, inv in invoices.items():
            if invoice_id and inv_id != invoice_id:
                continue
            if worker_id and inv.get("worker_id") != worker_id:
                continue
            if organization_id and inv.get("organization_id") != organization_id:
                continue
            if status and inv.get("status") != status:
                continue
            if currency and inv.get("currency") != currency:
                continue
            if amount is not None and inv.get("amount") != amount:
                continue
            if not in_range(inv.get("amount", 0), min_amount, max_amount):
                continue
            if issue_date and not date_equals(inv.get("issue_date", ""), issue_date):
                continue
            if not in_date_range(inv.get("issue_date", ""), issue_date_from, issue_date_to):
                continue
            if due_date and not date_equals(inv.get("due_date", ""), due_date):
                continue
            if not in_date_range(inv.get("due_date", ""), due_date_from, due_date_to):
                continue

            result.append({**inv, "invoice_id": inv_id})

        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_filtered_invoices",
                "description": (
                    "Returns invoices filtered by invoice_id, worker_id, status, amount (exact or range), "
                    "issue_date/due_date (exact or range), organization, and currency. Invoice ID is the dictionary key."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "invoice_id": {"type": "string"},
                        "worker_id": {"type": "string"},
                        "organization_id": {"type": "string"},
                        "status": {"type": "string"},
                        "currency": {"type": "string"},
                        "amount": {"type": "number", "description": "Exact amount match"},
                        "min_amount": {"type": "number"},
                        "max_amount": {"type": "number"},
                        "issue_date": {"type": "string", "description": "Exact ISO8601 issue date"},
                        "issue_date_from": {"type": "string"},
                        "issue_date_to": {"type": "string"},
                        "due_date": {"type": "string", "description": "Exact ISO8601 due date"},
                        "due_date_from": {"type": "string"},
                        "due_date_to": {"type": "string"}
                    },
                    "required": []
                }
            }
        }
