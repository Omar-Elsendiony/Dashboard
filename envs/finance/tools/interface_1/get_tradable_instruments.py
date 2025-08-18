import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetTradableInstruments(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_instrument_type: Optional[str] = None,
               fund_status: Optional[str] = None, fund_ticker: Optional[str] = None) -> str:
        instruments = data.get("instruments", {})
        results = []
        
        for instrument in instruments.values():
            if fund_instrument_type and instrument.get("instrument_type") != fund_instrument_type:
                continue
            if fund_status and instrument.get("status") != fund_status:
                continue
            if fund_ticker and instrument.get("ticker") != fund_ticker:
                continue
            results.append(instrument)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_tradable_instruments",
                "description": "Get instruments for investment universe management",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_instrument_type": {
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
                        "fund_status": {"type": "string", "description": "Filter by status (active, inactive)"},
                        "fund_ticker": {"type": "string", "description": "Filter by ticker symbol"}
                    },
                    "required": []
                }
            }
        }
