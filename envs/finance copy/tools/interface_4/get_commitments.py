import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class get_commitments(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        commitment_id: Optional[str] = None,
        fund_id: Optional[str] = None,
        investor_id: Optional[str] = None,
        currency: Optional[str] = None,
        status: Optional[str] = None,
        commitment_date: Optional[str] = None
    ) -> str:
        commitments = data.get("commitments", {})
        results = []

        for c in commitments.values():
            if commitment_id is not None and str(c.get("commitment_id")) != str(commitment_id):
                continue
            if fund_id is not None and str(c.get("fund_id")) != str(fund_id):
                continue
            if investor_id is not None and str(c.get("investor_id")) != str(investor_id):
                continue
            if currency is not None and c.get("currency") != currency:
                continue
            if status is not None and c.get("status") != status:
                continue
            if commitment_date is not None and c.get("commitment_date") != commitment_date:
                continue

            results.append(c)

        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_commitments",
                "description": (
                    "Retrieve commitments filtered by optional parameters: "
                    "commitment_id, fund_id, investor_id, currency, status, or commitment_date."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "commitment_id": {
                            "type": "string",
                            "description": "Filter by commitment ID"
                        },
                        "fund_id": {
                            "type": "string",
                            "description": "Filter by fund ID"
                        },
                        "investor_id": {
                            "type": "string",
                            "description": "Filter by investor ID"
                        },
                        "currency": {
                            "type": "string",
                            "description": "Filter by currency (USD, EUR, GBP, NGN)"
                        },
                        "status": {
                            "type": "string",
                            "description": "Filter by status (pending, fulfilled)"
                        },
                        "commitment_date": {
                            "type": "string",
                            "description": "Filter by commitment date (YYYY-MM-DD)"
                        }
                    },
                    "required": []
                }
            }
        }
