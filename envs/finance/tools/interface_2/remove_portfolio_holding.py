import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class RemovePortfolioHolding(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], portfolio_holding_id: str) -> str:
        portfolio_holdings = data.get("portfolio_holdings", {})
        
        # Validate holding exists
        if str(portfolio_holding_id) not in portfolio_holdings:
            raise ValueError(f"Holding {portfolio_holding_id} not found")
        
        # Get holding details before deletion
        deleted_holding = portfolio_holdings.pop(str(portfolio_holding_id))
        
        return json.dumps({
            "investor_status": "removed",
            "removed_holding": deleted_holding
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "remove_holding",
                "description": "Remove a holding from a portfolio",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "portfolio_holding_id": {"type": "string", "description": "ID of the holding to remove"}
                    },
                    "required": ["portfolio_holding_id"]
                }
            }
        }
