import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class get_funds(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        fund_id: Optional[str] = None,
        name: Optional[str] = None,
        fund_type: Optional[str] = None,
        base_currency: Optional[str] = None,
        manager_id: Optional[str] = None,
        status: Optional[str] = None
    ) -> str:
        funds = data.get("funds", {})
        results = []

        for fund in funds.values():
            if fund_id is not None and str(fund.get("fund_id")) != str(fund_id):
                continue
            if name is not None and name.lower() not in fund.get("name", "").lower():
                continue
            if fund_type is not None and fund.get("fund_type") != fund_type:
                continue
            if base_currency is not None and fund.get("base_currency") != base_currency:
                continue
            if manager_id is not None and str(fund.get("manager_id")) != str(manager_id):
                continue
            if status is not None and fund.get("status") != status:
                continue

            results.append(fund)

        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_funds",
                "description": (
                    "Retrieve funds filtered by optional parameters: "
                    "fund_id, name (partial match), fund_type, base_currency, manager_id, or status."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {
                            "type": "string",
                            "description": "Filter by fund ID"
                        },
                        "name": {
                            "type": "string",
                            "description": "Partial match on fund name"
                        },
                        "fund_type": {
                            "type": "string",
                            "description": "Filter by fund type (equity, fixed_income, multi_asset, hedge)"
                        },
                        "base_currency": {
                            "type": "string",
                            "description": "Filter by base currency (USD, EUR, GBP, NGN)"
                        },
                        "manager_id": {
                            "type": "string",
                            "description": "Filter by manager user ID"
                        },
                        "status": {
                            "type": "string",
                            "description": "Filter by fund status (open, closed)"
                        }
                    },
                    "required": []
                }
            }
        }