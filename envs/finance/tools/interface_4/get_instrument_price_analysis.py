import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetInstrumentPriceAnalysis(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], analysis_instrument_id: Optional[str] = None,
               price_date: Optional[str] = None) -> str:
        instrument_prices = data.get("instrument_prices", {})
        instruments = data.get("instruments", {})
        results = []
        
        # Validate instrument if provided
        if analysis_instrument_id and str(analysis_instrument_id) not in instruments:
            raise ValueError(f"Instrument {analysis_instrument_id} not found")
        
        for analysis_price in instrument_prices.values():
            if analysis_instrument_id and analysis_price.get("analysis_instrument_id") != analysis_instrument_id:
                continue
            if price_date and analysis_price.get("price_date") != price_date:
                continue
            results.append(analysis_price)
        
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
                        "analysis_instrument_id": {"type": "string", "description": "Filter by instrument ID (optional)"},
                        "price_date": {"type": "string", "description": "Filter by analysis_price date (optional)"}
                    },
                    "required": []
                }
            }
        }
