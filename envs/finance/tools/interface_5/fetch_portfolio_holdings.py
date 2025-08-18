import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class FetchPortfolioHoldings(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], portfolio_id: str) -> str:
        portfolio_holdings = data.get("portfolio_holdings", {})
        results = []
        
        for holding in portfolio_holdings.values():
            if holding.get("portfolio_id") == str(portfolio_id):
                results.append(holding)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "fetch_portfolio_holdings",
                "description": "Fetch portfolio holdings for holdings analysis and risk management",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "portfolio_id": {"type": "string", "description": "ID of the portfolio"}
                    },
                    "required": ["portfolio_id"]
                }
            }
        }
