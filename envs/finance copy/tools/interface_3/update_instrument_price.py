import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class update_instrument_price(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        price_id: str,
        open_price: Optional[float] = None,
        high_price: Optional[float] = None,
        low_price: Optional[float] = None,
        close_price: Optional[float] = None
    ) -> str:
        prices = data.get("instrument_prices", {})

        # Validate price record exists
        if price_id not in prices:
            raise ValueError(f"Price record {price_id} not found")
        record = prices[price_id]

        # Determine the candidate values (fallback to existing if not provided)
        vals = {
            "open_price": open_price if open_price is not None else record["open_price"],
            "high_price": high_price if high_price is not None else record["high_price"],
            "low_price": low_price if low_price is not None else record["low_price"],
            "close_price": close_price if close_price is not None else record["close_price"],
        }

        # Ensure low_price is the minimum and high_price is the maximum
        all_vals = [vals["open_price"], vals["high_price"], vals["low_price"], vals["close_price"]]
        if vals["low_price"] != min(all_vals):
            raise ValueError(f"low_price ({vals['low_price']}) must be the lowest of {all_vals}")
        if vals["high_price"] != max(all_vals):
            raise ValueError(f"high_price ({vals['high_price']}) must be the highest of {all_vals}")

        # Apply the updates
        for key, candidate in vals.items():
            if locals()[key] is not None:  # only set if argument was provided
                record[key] = candidate

        return json.dumps(record)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_instrument_price",
                "description": (
                    "Update an existing price record. Provide price_id and any subset "
                    "of open_price, high_price, low_price, close_price. "
                    "Validates that high_price is the maximum and low_price is the minimum of all four."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "price_id": {"type": "string", "description": "ID of the price record to update"},
                        "open_price": {"type": "number", "description": "Optional new opening price"},
                        "high_price": {"type": "number", "description": "Optional new high price"},
                        "low_price": {"type": "number", "description": "Optional new low price"},
                        "close_price": {"type": "number", "description": "Optional new closing price"}
                    },
                    "required": ["price_id"]
                }
            }
        }