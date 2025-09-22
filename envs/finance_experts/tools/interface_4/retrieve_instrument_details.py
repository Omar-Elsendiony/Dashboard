import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class RetrieveIntrumentDetails(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, 
               instrument_type: Optional[str] = None,
               status: Optional[str] = None, 
               ticker: Optional[str] = None,
               instrument_id: Optional[str] = None,
               price_date: Optional[str] = None) -> str:
        
        if action == "instruments":
            # Handle instrument retrieval
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
            
        elif action == "instrument_prices":
            # Handle instrument prices retrieval
            instrument_prices = data.get("instrument_prices", {})
            instruments = data.get("instruments", {})
            results = []
            
            # Validate instrument if provided
            if instrument_id and str(instrument_id) not in instruments:
                raise ValueError(f"Instrument {instrument_id} not found")
            
            for price in instrument_prices.values():
                if instrument_id and price.get("instrument_id") != instrument_id:
                    continue
                if price_date and price.get("price_date") != price_date:
                    continue
                results.append(price)
            
            return json.dumps(results)
        
        else:
            raise ValueError(f"Invalid action: {action}. Must be 'instruments' or 'instrument_prices'")

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "retrieve_instrument_details",
                "description": """Retrieve financial instruments or their prices from the investment universe.
                
                ACTIONS:
                1. 'instruments' - Retrieve instrument data with optional filters:
                   - instrument_type: Filter by type (equities, bonds, etc.)
                   - status: Filter by status (active, inactive)
                   - ticker: Filter by ticker symbol
                   
                2. 'instrument_prices' - Retrieve pricing data with optional filters:
                   - instrument_id: Filter by specific instrument ID
                   - price_date: Filter by specific date
                
                USAGE EXAMPLES:
                - Get all equity instruments: action='instruments', instrument_type='equities'
                - Get active bonds: action='instruments', instrument_type='bonds', status='active'
                - Get specific instrument by ticker: action='instruments', ticker='AAPL'
                - Get prices for specific instrument: action='instrument_prices', instrument_id='12345'
                - Get all prices for a date: action='instrument_prices', price_date='2024-01-15'
                - Get price for instrument on date: action='instrument_prices', instrument_id='12345', price_date='2024-01-15'
                """,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Required: Specify 'instruments' to get instrument data or 'instrument_prices' to get pricing data",
                            "enum": ["instruments", "instrument_prices"]
                        },
                        "instrument_type": {
                            "type": "string",
                            "description": "Optional: Filter instruments by type (only used with action='instruments')",
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
                        "status": {
                            "type": "string", 
                            "description": "Optional: Filter instruments by status - 'active' or 'inactive' (only used with action='instruments')"
                        },
                        "ticker": {
                            "type": "string", 
                            "description": "Optional: Filter instruments by ticker symbol (only used with action='instruments')"
                        },
                        "instrument_id": {
                            "type": "string", 
                            "description": "Optional: Filter prices by instrument ID (only used with action='instrument_prices')"
                        },
                        "price_date": {
                            "type": "string", 
                            "description": "Optional: Filter prices by date in YYYY-MM-DD format (only used with action='instrument_prices')"
                        }
                    },
                    "required": ["action"]
                }
            }
        }