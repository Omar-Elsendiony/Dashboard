import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class update_investor_portfolio_holding(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        holding_id: str,
        quantity: float = None,
        cost_basis: float = None
    ) -> str:
        portfolio_holdings = data.get("portfolio_holdings", {})

        # Validate holding exists
        if str(holding_id) not in portfolio_holdings:
            raise ValueError(f"Holding {holding_id} not found")

        # Retrieve current holding state
        holding = portfolio_holdings[str(holding_id)]

        # Update fields if provided
        if quantity is not None:
            holding["quantity"] = round(float(quantity), 4)
        if cost_basis is not None:
            holding["cost_basis"] = round(float(cost_basis), 4)

        # Return updated state
        return json.dumps(holding)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_investor_portfolio_holding",
                "description": "Update quantity and/or cost basis of a portfolio holding; only provided fields will be changed.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "holding_id": {"type": "string", "description": "ID of the holding"},
                        "quantity": {"type": "number", "description": "New quantity of the holding"},
                        "cost_basis": {"type": "number", "description": "New cost basis per unit of the holding"}
                    },
                    "required": ["holding_id"]
                }
            }
        }
