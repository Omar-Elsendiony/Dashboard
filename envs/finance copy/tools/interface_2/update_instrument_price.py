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
        instrument_prices = data.get("instrument_prices", {})

        # Validate price record exists
        if price_id not in instrument_prices:
            raise ValueError(f"Price record {price_id} not found")
        record = instrument_prices[price_id]

        inst_id = record.get("instrument_id")
        date = record.get("price_date")

        # Ensure uniqueness: no other record for this instrument/date
        for pid, rec in instrument_prices.items():
            if pid == price_id:
                continue
            if rec.get("instrument_id") == inst_id and rec.get("price_date") == date:
                raise ValueError(
                    f"Duplicate price for instrument {inst_id} on {date} (conflicts with record {pid})"
                )

        # Update provided fields
        if open_price is not None:
            record["open_price"] = open_price
        if high_price is not None:
            record["high_price"] = high_price
        if low_price is not None:
            record["low_price"] = low_price
        if close_price is not None:
            record["close_price"] = close_price

        return json.dumps(record)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_instrument_price",
                "description": (
                    "Update an existing instrument price record. "
                    "Provide price_id and any subset of open_price, high_price, low_price, close_price."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "price_id": {
                            "type": "string",
                            "description": "ID of the price record to update"
                        },
                        "open_price": {
                            "type": "number",
                            "description": "New opening price"
                        },
                        "high_price": {
                            "type": "number",
                            "description": "New high price"
                        },
                        "low_price": {
                            "type": "number",
                            "description": "New low price"
                        },
                        "close_price": {
                            "type": "number",
                            "description": "New closing price"
                        }
                    },
                    "required": ["price_id"]
                }
            }
        }