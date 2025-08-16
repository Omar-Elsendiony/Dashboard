import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class AddNewTradeForFund(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str, instrument_id: str,
               quantity: float, price: float, side: str, status: str = "pending") -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        funds = data.get("funds", {})
        instruments = data.get("instruments", {})
        trades = data.get("trades", {})
        
        # Validate fund exists
        if str(fund_id) not in funds:
            raise ValueError(f"Fund {fund_id} not found")
        
        # Validate instrument exists
        if str(instrument_id) not in instruments:
            raise ValueError(f"Instrument {instrument_id} not found")
        
        # Validate side
        valid_sides = ["buy", "sell"]
        if side not in valid_sides:
            raise ValueError(f"Invalid side. Must be one of {valid_sides}")
        
        # Validate status
        valid_statuses = ["approved", "executed", "pending", "failed"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        trade_id = generate_id(trades)
        timestamp = "2025-10-01T00:00:00"
        
        new_trade = {
            "trade_id": trade_id,
            "fund_id": fund_id,
            "instrument_id": instrument_id,
            "trade_date": timestamp,
            "quantity": quantity,
            "price": price,
            "side": side,
            "status": status,
            "created_at": timestamp
        }
        
        trades[str(trade_id)] = new_trade
        return json.dumps({"trade_id": trade_id})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_new_trade_for_fund",
                "description": "Add a new trade for investment execution",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "ID of the fund"},
                        "instrument_id": {"type": "string", "description": "ID of the instrument"},
                        "quantity": {"type": "number", "description": "Trade quantity"},
                        "price": {"type": "number", "description": "Trade price"},
                        "side": {"type": "string", "description": "Trade side (buy, sell)"},
                        "status": {"type": "string", "description": "Trade status (approved, executed, pending, failed), defaults to pending"}
                    },
                    "required": ["fund_id", "instrument_id", "quantity", "price", "side"]
                }
            }
        }
