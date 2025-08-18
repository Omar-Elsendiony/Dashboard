import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class ObtainFundTradeDetails(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str, instrument_id: Optional[str] = None,
               status: Optional[str] = None, side: Optional[str] = None) -> str:
        trades = data.get("trades", {})
        funds = data.get("funds", {})
        results = []
        
        # Validate fund exists
        if str(fund_id) not in funds:
            raise ValueError(f"Fund {fund_id} not found")
        
        for trade in trades.values():
            if trade.get("fund_id") != fund_id:
                continue
            if instrument_id and trade.get("instrument_id") != instrument_id:
                continue
            if status and trade.get("status") != status:
                continue
            if side and trade.get("side") != side:
                continue
            
            # Calculate trade value for cost analysis
            trade_copy = trade.copy()
            trade_copy["trade_value"] = float(trade.get("quantity", 0)) * float(trade.get("price", 0))
            results.append(trade_copy)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "obtain_fund_trade_details",
                "description": "Obtain fund trade details for transaction cost analysis",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "ID of the fund"},
                        "instrument_id": {"type": "string", "description": "Filter by instrument ID (optional)"},
                        "status": {"type": "string", "description": "Filter by trade status (approved, executed, pending, failed)"},
                        "side": {"type": "string", "description": "Filter by trade side (buy, sell)"}
                    },
                    "required": ["fund_id"]
                }
            }
        }
