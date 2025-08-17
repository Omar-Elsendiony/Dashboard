import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ExecuteTrade(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str, instrument_id: str,
               quantity: float, price_limit: float, trader_id: str,
               fund_manager_approval: bool) -> str:

        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        if not fund_manager_approval:
            return json.dumps({"error": "Fund Manager approval required. Process halted."})
        

        funds = data.get("funds", {})
        users = data.get("users", {})
        trades = data.get("trades", {})
        instruments = data.get("instruments", {})
        
        # Validate entities exist
        if str(fund_id) not in funds:
            return json.dumps({"error": f"Fund {fund_id} not found"})
        if str(trader_id) not in users:
            return json.dumps({"error": f"Trader {trader_id} not found"})
        if str(instrument_id) not in instruments:
            return json.dumps({"error": f"Instrument {instrument_id} not found"})
        
        trade_id = generate_id(trades)
        timestamp = "2025-10-01T00:00:00"
        
        # Determine trade side
        side = "buy" if quantity > 0 else "sell"
        
        new_trade = {
            "trade_id": trade_id,
            "fund_id": int(fund_id),
            "instrument_id": int(instrument_id),
            "trade_date": timestamp,
            "quantity": abs(quantity),
            "price": price_limit,
            "side": side,
            "status": "executed",
            "created_at": timestamp
        }
        
        trades[str(trade_id)] = new_trade
        
        return json.dumps({"trade_id": str(trade_id), "success": True, "message": "Trade executed"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "execute_trade",
                "description": "Execute a trade after required approvals",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "ID of the fund"},
                        "instrument_id": {"type": "string", "description": "ID of the instrument to trade"},
                        "quantity": {"type": "number", "description": "Trade quantity: positive for buy, negative for sell"},
                        "price_limit": {"type": "number", "description": "Price limit"},
                        "trader_id": {"type": "string", "description": "ID of the trader"},
                        "fund_manager_approval": {"type": "boolean", "description": "Fund Manager approval flag (True/False)"}
                    },
                    "required": ["fund_id", "instrument_id", "quantity", "price_limit", "trader_id", 
                               "fund_manager_approval"]
                }
            }
        }