import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class CalculateDailyProfitLossByFund(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str, trade_date: Optional[str] = None) -> str:
        trades = data.get("trades", {})
        funds = data.get("funds", {})
        results = []
        
        # Validate fund exists
        if str(fund_id) not in funds:
            raise ValueError(f"Fund {fund_id} not found")
        
        daily_pnl = {}
        
        for trade in trades.values():
            if trade.get("fund_id") != fund_id:
                continue
            
            # Extract date from timestamp
            trade_timestamp = trade.get("trade_date", "")
            trade_day = trade_timestamp.split("T")[0] if "T" in trade_timestamp else trade_timestamp
            
            if trade_date and trade_day != trade_date:
                continue
            
            if trade_day not in daily_pnl:
                daily_pnl[trade_day] = {
                    "date": trade_day,
                    "fund_id": fund_id,
                    "total_buy_value": 0,
                    "total_sell_value": 0,
                    "net_pnl": 0,
                    "trade_count": 0
                }
            
            quantity = float(trade.get("quantity", 0))
            price = float(trade.get("price", 0))
            value = quantity * price
            
            if trade.get("side") == "buy":
                daily_pnl[trade_day]["total_buy_value"] += value
            elif trade.get("side") == "sell":
                daily_pnl[trade_day]["total_sell_value"] += value
            
            daily_pnl[trade_day]["trade_count"] += 1
        
        # Calculate net P&L
        for day_data in daily_pnl.values():
            day_data["net_pnl"] = day_data["total_sell_value"] - day_data["total_buy_value"]
            results.append(day_data)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "calculate_daily_profit_loss_by_fund",
                                "description": "Calculate the daily profit/loss for a specific fund based on trade activities",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "ID of the fund"},
                        "trade_date": {"type": "string", "description": "Filter by specific trade date (optional)"}
                    },
                    "required": ["fund_id"]
                }
            }
        }
