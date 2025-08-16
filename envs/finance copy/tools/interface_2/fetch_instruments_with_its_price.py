import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class fetch_instruments_with_its_price(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        ticker: Optional[str] = None,
        name: Optional[str] = None,
        instrument_type: Optional[str] = None
    ) -> str:
        instruments = data.get("instruments", {})
        prices = data.get("instrument_prices", {})
        results = []

        for instr in instruments.values():
            if ticker and instr.get("ticker") != ticker:
                continue
            if name and name.lower() not in instr.get("name", "").lower():
                continue
            if instrument_type and instr.get("instrument_type") != instrument_type:
                continue

            # Collect all prices for this instrument
            instr_prices = [
                p for p in prices.values()
                if p.get("instrument_id") == instr.get("instrument_id")
            ]

            instr_copy = instr.copy()
            instr_copy["prices"] = instr_prices
            results.append(instr_copy)

        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "fetch_instruments_with_its_price",
                "description": "Fetch instruments filtered by ticker, name, or type, with all their price entries.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ticker": {"type": "string", "description": "Instrument ticker"},
                        "name": {"type": "string", "description": "Partial match on instrument name"},
                        "instrument_type": {
                            "type": "string",
                            "description": "Instrument type (stock, bond, derivative, cash, other)"
                        }
                    },
                    "required": []
                }
            }
        }