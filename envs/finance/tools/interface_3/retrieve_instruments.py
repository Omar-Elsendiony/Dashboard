import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class retrieve_instruments(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        instrument_id: Optional[str] = None,
        ticker: Optional[str] = None,
        name: Optional[str] = None,
        instrument_type: Optional[str] = None
    ) -> str:
        instruments = data.get("instruments", {})
        results = []

        for instr in instruments.values():
            if instrument_id is not None and str(instr.get("instrument_id")) != str(instrument_id):
                continue
            if ticker is not None and instr.get("ticker", "").upper() != ticker.upper():
                continue
            if name is not None and name.lower() not in instr.get("name", "").lower():
                continue
            if instrument_type is not None and instr.get("instrument_type") != instrument_type:
                continue
            results.append(instr)

        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "retrieve_instruments",
                "description": "Fetch instruments by optional filters: instrument_id, ticker, name, or instrument_type.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "instrument_id": {
                            "type": "string",
                            "description": "Filter by instrument ID"
                        },
                        "ticker": {
                            "type": "string",
                            "description": "Filter by ticker symbol"
                        },
                        "name": {
                            "type": "string",
                            "description": "Partial match on instrument name"
                        },
                        "instrument_type": {
                            "type": "string",
                            "description": "Filter by instrument type (stock, bond, derivative, cash, other)"
                        }
                    },
                    "required": []
                }
            }
        }