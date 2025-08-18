import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetFundTradeAnalysis(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], analysis_fund_id: str, analysis_instrument_id: Optional[str] = None,
               status: Optional[str] = None, side: Optional[str] = None) -> str:
        trades = data.get("trades", {})
        funds = data.get("funds", {})
        results = []
        
        # Validate fund exists
        if str(analysis_fund_id) not in funds:
            raise ValueError(f"Fund {analysis_fund_id} not found")
        
        for trade in trades.values():
            if trade.get("analysis_fund_id") != analysis_fund_id:
                continue
            if analysis_instrument_id and trade.get("analysis_instrument_id") != analysis_instrument_id:
                continue
            if status and trade.get("status") != status:
                continue
            if side and trade.get("side") != side:
                continue
            
            # Calculate trade analysis_value for cost analysis
            trade_copy = trade.copy()
            trade_copy["trade_value"] = float(trade.get("quantity", 0)) * float(trade.get("analysis_price", 0))
            results.append(trade_copy)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_fund_trade_details",
                "description": "Get fund trade details for transaction cost analysis",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "analysis_fund_id": {"type": "string", "description": "ID of the fund"},
                        "analysis_instrument_id": {"type": "string", "description": "Filter by instrument ID (optional)"},
                        "status": {"type": "string", "description": "Filter by trade status (approved, executed, pending, failed)"},
                        "side": {"type": "string", "description": "Filter by trade side (buy, sell)"}
                    },
                    "required": ["analysis_fund_id"]
                }
            }
        }
