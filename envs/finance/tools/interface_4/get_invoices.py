import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class get_invoices(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        invoice_id: Optional[str] = None,
        fund_id: Optional[str] = None,
        investor_id: Optional[str] = None,
        commitment_id: Optional[str] = None,
        status: Optional[str] = None,
        currency: Optional[str] = None,
        payment_type: Optional[str] = None
    ) -> str:
        invoices = data.get("invoices", {})
        results = []

        for inv in invoices.values():
            if invoice_id is not None and str(inv.get("invoice_id")) != str(invoice_id):
                continue
            if fund_id is not None and str(inv.get("fund_id")) != str(fund_id):
                continue
            if investor_id is not None and str(inv.get("investor_id")) != str(investor_id):
                continue
            if commitment_id is not None and str(inv.get("commitment_id")) != str(commitment_id):
                continue
            if status is not None and inv.get("status") != status:
                continue
            if currency is not None and inv.get("currency") != currency:
                continue
            if payment_type is not None and inv.get("payment_type") != payment_type:
                continue

            results.append(inv)

        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_invoices",
                "description": (
                    "Retrieve invoices filtered by optional parameters: "
                    "invoice_id, fund_id, investor_id, commitment_id, status, currency, or payment_type."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "invoice_id": {
                            "type": "string",
                            "description": "Filter by invoice ID"
                        },
                        "fund_id": {
                            "type": "string",
                            "description": "Filter by fund ID"
                        },
                        "investor_id": {
                            "type": "string",
                            "description": "Filter by investor ID"
                        },
                        "commitment_id": {
                            "type": "string",
                            "description": "Filter by commitment ID"
                        },
                        "status": {
                            "type": "string",
                            "description": "Filter by invoice status (issued, paid)"
                        },
                        "currency": {
                            "type": "string",
                            "description": "Filter by currency (USD, EUR, GBP, NGN)"
                        },
                        "payment_type": {
                            "type": "string",
                            "description": "Filter by payment type (auto-pay, manual)"
                        }
                    },
                    "required": []
                }
            }
        }
