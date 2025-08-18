
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class RetrieveFundInstruments(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str) -> str:
        funds = data.get("funds", {})
        instruments = data.get("instruments", {})
        trades = data.get("trades", {})
        
        # Validate fund exists
        if str(fund_id) not in funds:
            return json.dumps({"success": False, "message": "Fund not found", "halt": True})
        
        fund_instruments = []
        for trade_id, trade in trades.items():
            if trade.get("fund_id") == fund_id:
                instrument_id = trade.get("instrument_id")
                fund_instruments.append(instruments.get(str(instrument_id), {}))
        
        return json.dumps({"fund_instruments": fund_instruments})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "retrieve_fund_instruments",
                "description": "Retrieve all instruments associated with a specific fund",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "ID of the fund"}
                    },
                    "required": ["fund_id"]
                }
            }
        }