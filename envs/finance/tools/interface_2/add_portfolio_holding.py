import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class AddPortfolioHolding(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_portfolio_id: str, investor_fund_id: str,
               investor_quantity: float, investor_cost_basis: float) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        portfolio_holdings = data.get("portfolio_holdings", {})
        portfolios = data.get("portfolios", {})
        funds = data.get("funds", {})
        
        # Validate portfolio exists
        if str(investor_portfolio_id) not in portfolios:
            raise ValueError(f"Portfolio {investor_portfolio_id} not found")
        
        # Validate fund exists
        if str(investor_fund_id) not in funds:
            raise ValueError(f"Fund {investor_fund_id} not found")
        
        portfolio_holding_id = generate_id(portfolio_holdings)
        timestamp = "2025-10-01T00:00:00"
        
        new_holding = {
            "portfolio_holding_id": str(portfolio_holding_id),
            "portfolio_id": str(investor_portfolio_id),
            "target_fund_id": str(investor_fund_id),
            "quantity": investor_quantity,
            "cost_basis": investor_cost_basis,
            "created_at": timestamp
        }
        
        portfolio_holdings[str(portfolio_holding_id)] = new_holding
        return json.dumps(new_holding)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_portfolio_holding",
                "description": "Add new holding for investment execution",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "portfolio_id": {"type": "string", "description": "ID of the portfolio"},
                        "fund_id": {"type": "string", "description": "ID of the fund"},
                        "quantity": {"type": "number", "description": "Quantity of holding"},
                        "cost_basis": {"type": "number", "description": "Cost basis of holding"}
                    },
                    "required": ["portfolio_id", "fund_id", "quantity", "cost_basis"]
                }
            }
        }
