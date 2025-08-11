
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetInvoiceStatusByOrg(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], org_id: str) -> str:
        invoices = data.get("invoices", {})
        results = [
            {"invoice_id": inv_id, "status": inv.get("status"), "amount": inv.get("amount")}
            for inv_id, inv in invoices.items()
            if inv.get("organization_id") == org_id
        ]
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_invoice_status_by_org",
                "description": "Returns invoice statuses for an organization",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "org_id": {
                            "type": "string",
                            "description": "The organization ID whose invoices are to be queried"
                        }
                    },
                    "required": ["org_id"]
                }
            }
        }
