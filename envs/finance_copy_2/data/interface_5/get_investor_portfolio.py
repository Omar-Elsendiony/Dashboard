import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetInvestorPortfolio(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_id: str) -> str:
        investors = data.get("investors", {})
        portfolios = data.get("portfolios", {})
        
        # Validate investor exists
        if str(investor_id) not in investors:
            raise ValueError(f"Investor {investor_id} not found")
        
        # Find investor's portfolio
        investor_portfolio = None
        for portfolio in portfolios.values():
            if portfolio.get("investor_id") == investor_id:
                investor_portfolio = portfolio
                break
        
        if not investor_portfolio:
            return json.dumps({"message": "No portfolio found for investor"})
        
        return json.dumps(investor_portfolio)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_investor_portfolio",
                "description": "Get the investor's complete portfolio overview including all holdings and performance metrics",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {"type": "string", "description": "ID of the investor"}
                    },
                    "required": ["investor_id"]
                }
            }
        }
