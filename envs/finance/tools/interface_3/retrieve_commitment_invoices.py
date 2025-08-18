import json
from typing import Any, Dict, Optional, List
from tau_bench.envs.tool import Tool

class RetrieveCommitmentInvoices(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], invoice_ids: Optional[List[str]] = None) -> str:
        invoices = data.get("invoices", {})
        results = []
        
        if invoice_ids:
            # Retrieve specific invoices
            for commitment_invoice_id in invoice_ids:
                if str(commitment_invoice_id) in invoices:
                    results.append(invoices[str(commitment_invoice_id)])
        else:
            # Retrieve all invoices
            results = list(invoices.values())
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "retrieve_invoices",
                "description": "Retrieve specific invoices by IDs or all invoices",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "invoice_ids": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of invoice IDs to retrieve. If not provided, returns all invoices"
                        }
                    },
                    "required": []
                }
            }
        }
