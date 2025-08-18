import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetRelationsInvestorPortfolio(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], relations_investor_id: str) -> str:
        portfolios = data.get("portfolios", {})
        results = []
        
        for portfolio in portfolios.values():
            if portfolio.get("relations_investor_id") == str(relations_investor_id):
                results.append(portfolio)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_investor_portfolio",
                "description": "Get investor portfolio for client servicing and performance tracking",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "relations_investor_id": {"type": "string", "description": "ID of the investor"}
                    },
                    "required": ["relations_investor_id"]
                }
            }
        }
