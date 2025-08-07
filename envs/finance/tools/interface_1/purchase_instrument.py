import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class purchase_instrument(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        portfolio_id: str,
        instrument_id: str,
        quantity: float,
        cost_basis: float
    ) -> str:
        def generate_id(table: Dict[str, Any]) -> str:
            return str(max((int(k) for k in table.keys()), default=0) + 1)

        portfolios = data.get("portfolios", {})
        instruments = data.get("instruments", {})
        portfolio_holdings = data.setdefault("portfolio_holdings", {})

        # Validate portfolio exists
        if portfolio_id not in portfolios:
            raise ValueError(f"Portfolio {portfolio_id} not found")

        # Validate instrument exists
        if instrument_id not in instruments:
            raise ValueError(f"Instrument {instrument_id} not found")

        holding_id = generate_id(portfolio_holdings)
        now = "2025-08-07T00:00:00Z"

        new_holding = {
            "holding_id": holding_id,
            "portfolio_id": portfolio_id,
            "instrument_id": instrument_id,
            "quantity": round(float(quantity), 4),
            "cost_basis": round(float(cost_basis), 4),
            "created_at": now
        }

        portfolio_holdings[holding_id] = new_holding
        return json.dumps(new_holding)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "purchase_instrument",
                "description": "Purchase an instrument and add it to a portfolio",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "portfolio_id": {
                            "type": "string",
                            "description": "ID of the portfolio"
                        },
                        "instrument_id": {
                            "type": "string",
                            "description": "ID of the instrument to purchase"
                        },
                        "quantity": {
                            "type": "number",
                            "description": "Quantity of the instrument to purchase"
                        },
                        "cost_basis": {
                            "type": "number",
                            "description": "Cost basis per unit of the instrument"
                        }
                    },
                    "required": ["portfolio_id", "instrument_id", "quantity", "cost_basis"]
                }
            }
        }