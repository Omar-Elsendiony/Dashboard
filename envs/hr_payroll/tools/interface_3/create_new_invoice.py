import json
import uuid
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateNewInvoice(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        amount: float,
        due_date: str,
        worker_id: str = None,
        organization_id: str = None,
        currency: str = None,
        issue_date: str = "2025-07-01",
        status: str = "issued",
        contract_id: str = None
    ) -> str:
        contracts = data.get("contracts", {})

        # Optional backward compatibility via contract_id
        if contract_id:
            if contract_id not in contracts:
                raise ValueError("Contract not found")
            contract = contracts[contract_id]
            worker_id = worker_id or contract.get("worker_id")
            organization_id = organization_id or contract.get("organization_id")
            currency = currency or contract.get("currency")

        if not all([worker_id, organization_id, currency]):
            raise ValueError("Missing required fields: worker_id, organization_id, and currency")

        invoice_id = str(uuid.uuid4())
        invoice = {
            "worker_id": worker_id,
            "organization_id": organization_id,
            "issue_date": issue_date,
            "due_date": due_date,
            "amount": round(amount, 2),
            "status": status,
            "currency": currency
        }

        invoices = data.setdefault("invoices", {})
        invoices[invoice_id] = invoice

        return json.dumps({
            "invoice_id": invoice_id,
            **invoice
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_new_invoice",
                "description": (
                    "Creates a new invoice. You may provide contract_id for backward compatibility "
                    "or directly specify worker_id, organization_id, and currency. Returns full invoice data."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "contract_id": {
                            "type": "string",
                            "description": "Optional. Used for backward compatibility to derive worker/org/currency."
                        },
                        "worker_id": {
                            "type": "string",
                            "description": "Worker associated with the invoice"
                        },
                        "organization_id": {
                            "type": "string",
                            "description": "Organization issuing the invoice"
                        },
                        "currency": {
                            "type": "string",
                            "description": "Currency code (e.g. USD, EUR)"
                        },
                        "amount": {
                            "type": "number",
                            "description": "Invoice amount"
                        },
                        "issue_date": {
                            "type": "string",
                            "description": "Issue date in ISO format",
                            "default": "2025-07-01"
                        },
                        "due_date": {
                            "type": "string",
                            "description": "Due date in ISO format"
                        },
                        "status": {
                            "type": "string",
                            "description": "Invoice status (e.g. issued, paid, overdue)",
                            "default": "issued"
                        }
                    },
                    "required": ["amount", "due_date"]
                }
            }
        }
