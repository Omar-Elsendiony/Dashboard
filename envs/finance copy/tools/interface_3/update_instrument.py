import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class update_instrument(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        instrument_id: str,
        ticker: Optional[str] = None,
        name: Optional[str] = None,
        instrument_type: Optional[str] = None
    ) -> str:
        instruments = data.get("instruments", {})

        # Validate instrument exists
        if str(instrument_id) not in instruments:
            raise ValueError(f"Instrument {instrument_id} not found")

        # Validate instrument type if provided
        if instrument_type is not None:
            valid_types = ["stock", "bond", "derivative", "cash", "other"]
            if instrument_type not in valid_types:
                raise ValueError(f"Invalid instrument type. Must be one of {valid_types}")

        # Validate ticker uniqueness if provided
        if ticker is not None:
            for iid, inst in instruments.items():
                if iid != str(instrument_id) and inst.get("ticker", "").upper() == ticker.upper():
                    raise ValueError(f"Ticker '{ticker}' already exists for instrument {iid}")

        instrument = instruments[str(instrument_id)]

        # Update fields if provided
        if ticker is not None:
            instrument["ticker"] = ticker
        if name is not None:
            instrument["name"] = name
        if instrument_type is not None:
            instrument["instrument_type"] = instrument_type

        return json.dumps(instrument)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_instrument",
                "description": "Update an instrument's information; ticker must remain unique across all instruments.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "instrument_id": {
                            "type": "string",
                            "description": "ID of the instrument"
                        },
                        "ticker": {
                            "type": "string",
                            "description": "New unique instrument ticker symbol"
                        },
                        "name": {
                            "type": "string",
                            "description": "New instrument name"
                        },
                        "instrument_type": {
                            "type": "string",
                            "description": "New instrument type (stock, bond, derivative, cash, other)"
                        }
                    },
                    "required": ["instrument_id"]
                }
            }
        }