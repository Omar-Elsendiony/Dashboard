import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetRelationsPortfolioHoldings(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], relations_portfolio_id: str) -> str:
        portfolio_holdings = data.get("portfolio_holdings", {})
        results = []
        
        for holding in portfolio_holdings.values():
            if holding.get("relations_portfolio_id") == str(relations_portfolio_id):
                results.append(holding)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_portfolio_holdings",
                "description": "Get portfolio holdings for holdings analysis and risk management",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "relations_portfolio_id": {"type": "string", "description": "ID of the portfolio"}
                    },
                    "required": ["relations_portfolio_id"]
                }
            }
        }
