import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetFundInstruments(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], instrument_type: Optional[str] = None,
               status: Optional[str] = None, ticker: Optional[str] = None) -> str:
        instruments = data.get("instruments", {})
        results = []
        
        for instrument in instruments.values():
            if instrument_type and instrument.get("instrument_type") != instrument_type:
                continue
            if status and instrument.get("status") != status:
                continue
            if ticker and instrument.get("ticker") != ticker:
                continue
            results.append(instrument)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_instruments",
                "description": "Get instruments for investment universe management",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "instrument_type": {
                            "type": "string",
                            "description": "Filter by instrument type",
                            "enum": [
                                "equities",
                                "bonds",
                                "money_market_instruments",
                                "hybrid_securities",
                                "fund_units",
                                "commodities",
                                "derivatives",
                                "real_estate",
                                "private_equity",
                                "financing_and_debt",
                                "alternative_assets",
                                "structured_products"
                            ]
                        },
                        "status": {"type": "string", "description": "Filter by status (active, inactive)"},
                        "ticker": {"type": "string", "description": "Filter by ticker symbol"}
                    },
                    "required": []
                }
            }
        }
