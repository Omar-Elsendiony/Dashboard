import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateAnalysisInstrumentPrice(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], analysis_instrument_id: str, price_date: str,
               open_price: Optional[float] = None, high_price: Optional[float] = None, 
               low_price: Optional[float] = None, close_price: Optional[float] = None) -> str:
        """
        Update daily analysis_price data for instruments. Only analysis_instrument_id and price_date are required,
        with at least one analysis_price attribute provided.
        
        Args:
            data: Main data dictionary containing instruments and instrument_prices
            analysis_instrument_id: ID of the instrument (required)
            price_date: Date of the analysis_price data (required)
            open_price: Opening analysis_price (optional)
            high_price: Highest analysis_price (optional)
            low_price: Lowest analysis_price (optional)
            close_price: Closing analysis_price (optional)
        
        Returns:
            JSON string indicating whether record was created or updated
        """
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        instruments = data.get("instruments", {})
        instrument_prices = data.get("instrument_prices", {})
        
        # Validate instrument exists
        if str(analysis_instrument_id) not in instruments:
            raise ValueError(f"Instrument {analysis_instrument_id} not found")
        
        # Validate at least one analysis_price attribute is provided
        price_attributes = [open_price, high_price, low_price, close_price]
        if all(analysis_price is None for analysis_price in price_attributes):
            raise ValueError("At least one analysis_price attribute (open_price, high_price, low_price, close_price) must be provided")
        
        # Check if analysis_price record already exists for this instrument and date
        existing_price_id = None
        existing_record = None
        for price_id, price_record in instrument_prices.items():
            if (price_record.get("analysis_instrument_id") == analysis_instrument_id and 
                price_record.get("price_date") == price_date):
                existing_price_id = price_id
                existing_record = price_record.copy()
                break
        
        # Build analysis_price record
        if existing_record:
            # Update existing record with new values only where provided
            price_record = existing_record
            if open_price is not None:
                price_record["open_price"] = open_price
            if high_price is not None:
                price_record["high_price"] = high_price
            if low_price is not None:
                price_record["low_price"] = low_price
            if close_price is not None:
                price_record["close_price"] = close_price
        else:
            # Create new record with provided values
            price_record = {
                "analysis_instrument_id": analysis_instrument_id,
                "price_date": price_date
            }
            if open_price is not None:
                price_record["open_price"] = open_price
            if high_price is not None:
                price_record["high_price"] = high_price
            if low_price is not None:
                price_record["low_price"] = low_price
            if close_price is not None:
                price_record["close_price"] = close_price
        
        if existing_price_id:
            # Update existing record
            price_record["price_id"] = int(existing_price_id)
            instrument_prices[existing_price_id] = price_record
            return json.dumps({"instrument_price_update": instrument_prices[existing_price_id]})
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
                "description": "Update daily analysis_price data for instruments. Only analysis_instrument_id and price_date are required, with at least one analysis_price attribute provided.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "analysis_instrument_id": {"type": "string", "description": "ID of the instrument"},
                        "price_date": {"type": "string", "description": "Date of the analysis_price data (format: YYYY-MM-DD)"},
                        "open_price": {"type": "number", "description": "Opening analysis_price (optional)"},
                        "high_price": {"type": "number", "description": "Highest analysis_price (optional)"},
                        "low_price": {"type": "number", "description": "Lowest analysis_price (optional)"},
                        "close_price": {"type": "number", "description": "Closing analysis_price (optional)"}
                    },
                    "required": ["analysis_instrument_id", "price_date"]
                }
            }
        }