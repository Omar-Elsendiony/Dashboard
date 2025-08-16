import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdateInstrumentPrice(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], instrument_id: str, price_date: str,
               open_price: float, high_price: float, low_price: float, 
               close_price: float) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        instruments = data.get("instruments", {})
        instrument_prices = data.get("instrument_prices", {})
        
        # Validate instrument exists
        if str(instrument_id) not in instruments:
            raise ValueError(f"Instrument {instrument_id} not found")
        
        # Check if price record already exists for this instrument and date
        existing_price_id = None
        for price_id, price_record in instrument_prices.items():
            if (price_record.get("instrument_id") == instrument_id and 
                price_record.get("price_date") == price_date):
                existing_price_id = price_id
                break
        
        price_record = {
            "instrument_id": instrument_id,
            "price_date": price_date,
            "open_price": open_price,
            "high_price": high_price,
            "low_price": low_price,
            "close_price": close_price
        }
        
        if existing_price_id:
            # Update existing record
            price_record["price_id"] = int(existing_price_id)
            instrument_prices[existing_price_id] = price_record
            return json.dumps({"status": "updated", "price_id": int(existing_price_id)})
        else:
            # Create new record
            price_id = generate_id(instrument_prices)
            price_record["price_id"] = price_id
            instrument_prices[str(price_id)] = price_record
            return json.dumps({"status": "created", "price_id": price_id})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_instrument_price",
                "description": "Update daily price data for instruments",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "instrument_id": {"type": "string", "description": "ID of the instrument"},
                        "price_date": {"type": "string", "description": "Date of the price data"},
                        "open_price": {"type": "number", "description": "Opening price"},
                        "high_price": {"type": "number", "description": "Highest price"},
                        "low_price": {"type": "number", "description": "Lowest price"},
                        "close_price": {"type": "number", "description": "Closing price"}
                    },
                    "required": ["instrument_id", "price_date", "open_price", "high_price", "low_price", "close_price"]
                }
            }
        }
