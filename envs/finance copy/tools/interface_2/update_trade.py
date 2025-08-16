import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class update_trade(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        trade_id: str,
        quantity: Optional[float] = None,
        price: Optional[float] = None,
        status: Optional[str] = None
    ) -> str:
        trades = data.get("trades", {})

        # Validate trade exists
        if str(trade_id) not in trades:
            raise ValueError(f"Trade with ID {trade_id} not found")
        trade = trades[str(trade_id)]

        # Validate and apply updates
        if status is not None:
            valid_statuses = ["executed", "pending", "failed"]
            if status not in valid_statuses:
                raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
            trade["status"] = status

        if quantity is not None:
            if quantity < 0:
                raise ValueError("Quantity must be non-negative")
            trade["quantity"] = quantity

        if price is not None:
            if price < 0:
                raise ValueError("Price must be non-negative")
            trade["price"] = price

        return json.dumps(trade)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_trade_for_fund",
                "description": "Update fields of an existing trade; only provided fields will be changed.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "trade_id": {"type": "string", "description": "ID of the trade to update"},
                        "quantity": {"type": "number", "description": "New trade quantity"},
                        "price": {"type": "number", "description": "New trade price"},
                        "status": {
                            "type": "string",
                            "description": "New trade status (executed, pending, failed)"
                        }
                    },
                    "required": ["trade_id"]
                }
            }
        }