import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ProcessTrade(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str, instrument_id: str, 
               quantity: float, side: str, trade_date: str, price: float) -> str:
        """
        Execute a trade for a fund after all approvals are obtained.
        
        This tool performs step 3 of the Trade Execution & Post-Trade Controls SOP.
        Prerequisites: Fund Manager approval must be verified before calling this tool.
        """
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        funds = data.get("funds", {})
        instruments = data.get("instruments", {})
        trades = data.get("trades", {})
        
        # Validate required parameters
        if not fund_id:
            return json.dumps({"error": "fund_id is required"})
        
        if not instrument_id:
            return json.dumps({"error": "instrument_id is required"})
        
        if not side:
            return json.dumps({"error": "side is required"})
        
        if not trade_date:
            return json.dumps({"error": "trade_date is required"})
        
        # Validate fund exists
        if str(fund_id) not in funds:
            return json.dumps({"error": f"Fund {fund_id} not found"})
        
        # Validate instrument exists
        if str(instrument_id) not in instruments:
            return json.dumps({"error": f"Instrument {instrument_id} not found"})
        
        # Validate side
        valid_sides = ["buy", "sell"]
        if side.lower() not in valid_sides:
            return json.dumps({"error": f"Invalid side. Must be one of {valid_sides}"})
        
        # Validate quantity
        try:
            quantity = float(quantity)
            if quantity <= 0:
                return json.dumps({"error": "Quantity must be positive"})
        except (ValueError, TypeError):
            return json.dumps({"error": "Invalid quantity format"})
        
        # Validate price
        try:
            price = float(price)
            if price <= 0:
                return json.dumps({"error": "Price must be positive"})
        except (ValueError, TypeError):
            return json.dumps({"error": "Invalid price format"})
        
        # Validate fund status is open
        fund = funds[str(fund_id)]
        if fund.get("status", "").lower() != "open":
            return json.dumps({"error": f"Fund {fund_id} is not open for trading"})
        
        # Validate instrument status is active
        instrument = instruments[str(instrument_id)]
        if instrument.get("status", "").lower() != "active":
            return json.dumps({"error": f"Instrument {instrument_id} is not active for trading"})
        
        # Execute the trade
        trade_id = generate_id(trades)
        timestamp = "2025-10-01T00:00:00"
        
        new_trade = {
            "trade_id": str(trade_id),
            "fund_id": fund_id,
            "instrument_id": instrument_id,
            "trade_date": trade_date,
            "quantity": quantity,
            "price": price,
            "side": side.lower(),
            "status": "executed",
            "created_at": timestamp
        }
        
        trades[str(trade_id)] = new_trade
        
        return json.dumps({
            "success": True,
            "trade_id": str(trade_id),
            "message": f"Trade {trade_id} executed successfully",
            "trade_data": {
                "trade_id": new_trade["trade_id"],
                "fund_id": new_trade["fund_id"],
                "instrument_id": new_trade["instrument_id"],
                "quantity": new_trade["quantity"],
                "price": new_trade["price"],
                "side": new_trade["side"],
                "status": new_trade["status"],
                "trade_date": new_trade["trade_date"],
                "created_at": new_trade["created_at"]
            }
        })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "process_trade",
                "description": "Execute a trade for a fund after fund manager approval has been verified",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "ID of the fund executing the trade"},
                        "instrument_id": {"type": "string", "description": "ID of the instrument to trade"},
                        "quantity": {"type": "number", "description": "Trade quantity: positive for buy, negative for sell"},
                        "side": {"type": "string", "description": "Trade direction: 'buy' or 'sell'"},
                        "trade_date": {"type": "string", "description": "Date of executing Trade (YYYY-MM-DD)"},
                        "price": {"type": "number", "description": "Price"}
                    },
                    "required": ["fund_id", "instrument_id", "quantity", "side", "trade_date", "price"]
                }
            }
        }