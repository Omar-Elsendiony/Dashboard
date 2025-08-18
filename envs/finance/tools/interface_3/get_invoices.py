import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetInvoices(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], commitment_id: Optional[str] = None,
               status: Optional[str] = None, due_date_from: Optional[str] = None,
               due_date_to: Optional[str] = None) -> str:
        invoices = data.get("invoices", {})
        results = []
        
        for invoice in invoices.values():
            if commitment_id and invoice.get("commitment_id") != commitment_id:
                continue
            if status and invoice.get("status") != status:
                continue
            if due_date_from and invoice.get("due_date") < due_date_from:
                continue
            if due_date_to and invoice.get("due_date") > due_date_to:
                continue
            results.append(invoice)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_invoices",
                "description": "Get invoices with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "commitment_id": {"type": "string", "description": "Filter by commitment ID"},
                        "status": {"type": "string", "description": "Filter by status (issued, paid)"},
                        "due_date_from": {"type": "string", "description": "Filter invoices due from this date (YYYY-MM-DD)"},
                        "due_date_to": {"type": "string", "description": "Filter invoices due until this date (YYYY-MM-DD)"}
                    },
                    "required": []
                }
            }
        }
