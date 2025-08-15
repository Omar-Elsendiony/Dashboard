import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CalculateLiabilities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], instrument_closing_price: float) -> str:
        
        # Validate closing price
        if instrument_closing_price <= 0:
            return json.dumps({"success": False, "message": "Instrument closing price must be positive", "halt": True})
        
        # Calculate liabilities as 1.5% of closing price
        liabilities = round(instrument_closing_price * 0.015, 4)
        
        return json.dumps({"liabilities": liabilities})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "calculate_liabilities",
                "description": "Calculate liabilities as 1.5% of instrument closing price",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "instrument_closing_price": {"type": "number", "description": "Closing price of the instrument"}
                    },
                    "required": ["instrument_closing_price"]
                }
            }
        }
