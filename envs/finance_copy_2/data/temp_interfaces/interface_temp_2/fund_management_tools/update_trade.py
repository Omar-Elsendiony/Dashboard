import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateTrade(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], trade_id: str, status: Optional[str] = None,
               quantity: Optional[float] = None, price: Optional[float] = None) -> str:
        trades = data.get("trades", {})
        
        # Validate trade exists
        if str(trade_id) not in trades:
            raise ValueError(f"Trade {trade_id} not found")
        
        trade = trades[str(trade_id)]
        
        # Validate status if provided
        if status:
            valid_statuses = ["approved", "executed", "pending", "failed"]
            if status not in valid_statuses:
                raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
            trade["status"] = status
        
        # Update other fields if provided
        if quantity is not None:
            trade["quantity"] = quantity
        
        if price is not None:
            trade["price"] = price
        
        trade["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps(trade)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_trade",
                "description": "Update trade for settlement and corrections",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "trade_id": {"type": "string", "description": "ID of the trade to update"},
                        "status": {"type": "string", "description": "New status (approved, executed, pending, failed)"},
                        "quantity": {"type": "number", "description": "Updated quantity"},
                        "price": {"type": "number", "description": "Updated price"}
                    },
                    "required": ["trade_id"]
                }
            }
        }
