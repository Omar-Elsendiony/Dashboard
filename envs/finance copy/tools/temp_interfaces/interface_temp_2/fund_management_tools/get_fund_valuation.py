import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetFundValuation(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str, nav_date: Optional[str] = None) -> str:
        nav_records = data.get("nav_records", {})
        funds = data.get("funds", {})
        results = []
        
        # Validate fund exists
        if str(fund_id) not in funds:
            raise ValueError(f"Fund {fund_id} not found")
        
        for nav in nav_records.values():
            if nav.get("fund_id") != fund_id:
                continue
            if nav_date and nav.get("nav_date") != nav_date:
                continue
            results.append(nav)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_fund_valuation",
                "description": "Get fund performance measurement through NAV records",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "ID of the fund"},
                        "nav_date": {"type": "string", "description": "Filter by specific NAV date (optional)"}
                    },
                    "required": ["fund_id"]
                }
            }
        }
