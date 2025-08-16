import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetInvestorPortfolioHoldings(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_id: str) -> str:
        investors = data.get("investors", {})
        portfolios = data.get("portfolios", {})
        portfolio_holdings = data.get("portfolio_holdings", {})
        funds = data.get("funds", {})
        
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
            return json.dumps([])
        
        # Get holdings for this portfolio
        holdings = []
        for holding in portfolio_holdings.values():
            if holding.get("portfolio_id") == investor_portfolio.get("portfolio_id"):
                # Enrich with fund details
                fund_id = holding.get("fund_id")
                fund_details = funds.get(str(fund_id), {})
                
                enriched_holding = {
                    **holding,
                    "fund_name": fund_details.get("name"),
                    "fund_type": fund_details.get("fund_type"),
                    "fund_status": fund_details.get("status")
                }
                holdings.append(enriched_holding)
        
        return json.dumps(holdings)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_investor_portfolio_holdings",
                "description": "Retrieve detailed breakdown of all fund holdings within the investor's portfolio",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {"type": "string", "description": "ID of the investor"}
                    },
                    "required": ["investor_id"]
                }
            }
        }
