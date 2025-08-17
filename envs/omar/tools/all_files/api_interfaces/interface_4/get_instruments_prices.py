import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetInstrumentsPrices(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], instrument_id: Optional[str] = None,
               price_date: Optional[str] = None) -> str:
        instrument_prices = data.get("instrument_prices", {})
        instruments = data.get("instruments", {})
        results = []
        
        # Validate instrument if provided
        if instrument_id and str(instrument_id) not in instruments:
            raise ValueError(f"Instrument {instrument_id} not found")
        
        for price in instrument_prices.values():
            if instrument_id and price.get("instrument_id") != instrument_id:
                continue
            if price_date and price.get("price_date") != price_date:
                continue
            results.append(price)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_instruments_prices",
                "description": "Get instrument prices for pricing and valuation",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "instrument_id": {"type": "string", "description": "Filter by instrument ID (optional)"},
                        "price_date": {"type": "string", "description": "Filter by price date (optional)"}
                    },
                    "required": []
                }
            }
        }
