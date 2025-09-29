import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CompleteTrade(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str, instrument_id: str, 
               quantity: float, side: str, trade_date: str, price: float,
               fund_manager_approval: bool) -> str:
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
        
        # Validate required approval first
        if not fund_manager_approval:
            return json.dumps({
                "success": False,
                "error": "Fund Manager approval is required for trade execution"
            })
        
        # Validate required parameters
        if not fund_id:
            return json.dumps({
                "success": False,
                "error": "fund_id is required"
            })
        
        if not instrument_id:
            return json.dumps({
                "success": False,
                "error": "instrument_id is required"
            })
        
        if not side:
            return json.dumps({
                "success": False,
                "error": "side is required"
            })
        
        if not trade_date:
            return json.dumps({
                "success": False,
                "error": "trade_date is required"
            })
        
        # Validate fund exists
        if str(fund_id) not in funds:
            return json.dumps({
                "success": False,
                "error": f"Fund {fund_id} not found"
            })
        
        # Validate instrument exists
        if str(instrument_id) not in instruments:
            return json.dumps({
                "success": False,
                "error": f"Instrument {instrument_id} not found"
            })
        
        # Validate side
        valid_sides = ["buy", "sell"]
        if side.lower() not in valid_sides:
            return json.dumps({
                "success": False,
                "error": f"Invalid side. Must be one of {valid_sides}"
            })
        
        # Validate quantity
        try:
            quantity = float(quantity)
            if quantity <= 0:
                return json.dumps({
                    "success": False,
                    "error": "Quantity must be positive"
                })
        except (ValueError, TypeError):
            return json.dumps({
                "success": False,
                "error": "Invalid quantity format"
            })
        
        # Validate price
        try:
            price = float(price)
            if price <= 0:
                return json.dumps({
                    "success": False,
                    "error": "Price must be positive"
                })
        except (ValueError, TypeError):
            return json.dumps({
                "success": False,
                "error": "Invalid price format"
            })
        
        # Validate fund status is open
        fund = funds[str(fund_id)]
        if fund.get("status", "").lower() != "open":
            return json.dumps({
                "success": False,
                "error": f"Fund {fund_id} is not open for trading"
            })
        
        # Validate instrument status is active
        instrument = instruments[str(instrument_id)]
        if instrument.get("status", "").lower() != "active":
            return json.dumps({
                "success": False,
                "error": f"Instrument {instrument_id} is not active for trading"
            })
        
        # Execute the trade
        trade_id = generate_id(trades)
        timestamp = "2025-10-01T00:00:00"
        
        new_trade = {
            "trade_id": str(trade_id),
            "fund_id": str(fund_id),
            "instrument_id": str(instrument_id),
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
                "trade_id": str(new_trade["trade_id"]),
                "fund_id": str(new_trade["fund_id"]),
                "instrument_id": str(new_trade["instrument_id"]),
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
                "name": "complete_trade",
                "description": "Execute a trade for a fund in the fund management system. This tool processes trade orders with comprehensive validation and regulatory compliance checks. Validates fund and instrument existence, trading eligibility, quantity and price parameters, and ensures proper market side specification. Requires Fund Manager approval as mandated by trading authorization procedures. Creates executed trade records with complete audit trail for regulatory reporting and portfolio tracking. Essential for fund portfolio management, investment strategy execution, and maintaining accurate position records. Supports buy and sell operations with real-time validation of fund and instrument trading status.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {
                            "type": "string", 
                            "description": "Unique identifier of the fund executing the trade (required, must exist in system and have 'open' status)"
                        },
                        "instrument_id": {
                            "type": "string", 
                            "description": "Unique identifier of the financial instrument to trade (required, must exist in system and have 'active' status)"
                        },
                        "quantity": {
                            "type": "number", 
                            "description": "Number of units to trade (required, must be positive regardless of trade side)"
                        },
                        "side": {
                            "type": "string", 
                            "description": "Trade direction (required). Must be either 'buy' or 'sell'"
                        },
                        "trade_date": {
                            "type": "string", 
                            "description": "Date of trade execution in YYYY-MM-DD format (required)"
                        },
                        "price": {
                            "type": "number", 
                            "description": "Execution price per unit (required, must be positive)"
                        },
                        "fund_manager_approval": {
                            "type": "boolean",
                            "description": "Fund Manager approval presence (True/False) (required for trade execution as mandated by trading authorization procedures)"
                        }
                    },
                    "required": ["fund_id", "instrument_id", "quantity", "side", "trade_date", "price", "fund_manager_approval"]
                }
            }
        }