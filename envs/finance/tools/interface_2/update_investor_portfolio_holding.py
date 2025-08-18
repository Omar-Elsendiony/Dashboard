import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateInvestorPortfolioHolding(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], portfolio_holding_id: str, quantity: Optional[float] = None,
               cost_basis: Optional[float] = None) -> str:
        
        portfolio_holdings = data.get("portfolio_holdings", {})
        
        # Validate holding exists
        if str(portfolio_holding_id) not in portfolio_holdings:
            raise ValueError(f"Holding {portfolio_holding_id} not found")
        
        holding = portfolio_holdings[str(portfolio_holding_id)]
        
        # Update fields if provided
        if quantity is not None:
            holding["quantity"] = quantity
        if cost_basis is not None:
            holding["cost_basis"] = cost_basis
        
        return json.dumps(holding)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "investor_name": "update_investor_portfolio_holding",
                "description": "Update investor portfolio holding for position adjustments",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "portfolio_holding_id": {"type": "string", "description": "ID of the holding"},
                        "quantity": {"type": "number", "description": "New quantity (optional)"},
                        "cost_basis": {"type": "number", "description": "New cost basis (optional)"}
                    },
                    "required": ["portfolio_holding_id"]
                }
            }
        }
