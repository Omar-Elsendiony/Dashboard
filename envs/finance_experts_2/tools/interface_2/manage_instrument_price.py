import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ManageInstrumentPrice(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, price_data: Dict[str, Any] = None, price_id: str = None) -> str:
        """
        Create or update instrument price records.
        
        Actions:
        - create: Create new price record (requires price_data with instrument_id, price_date, open_price, high_price, low_price, close_price, approval_code)
        - update: Update existing price record (requires price_id and price_data with changes, approval_code)
        """
        if action not in ["create", "update"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid action '{action}'. Must be 'create' or 'update'"
            })
        
        # Access instrument_prices data
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for instrument_prices"
            })
        
        instrument_prices = data.get("instrument_prices", {})
        
        if action == "create":
            if not price_data:
                return json.dumps({
                    "success": False,
                    "error": "price_data is required for create action"
                })
            
            # Validate required fields for creation
            required_fields = ["instrument_id", "price_date", "open_price", "high_price", "low_price", "close_price", "approval_code"]
            missing_fields = [field for field in required_fields if field not in price_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields for price creation: {', '.join(missing_fields)}"
                })
            
            # Validate only allowed fields are present
            allowed_fields = ["instrument_id", "price_date", "open_price", "high_price", "low_price", "close_price", "approval_code"]
            invalid_fields = [field for field in price_data.keys() if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for price creation: {', '.join(invalid_fields)}"
                })
            
            # Validate all prices are positive
            price_fields = ["open_price", "high_price", "low_price", "close_price"]
            for field in price_fields:
                if price_data[field] <= 0:
                    return json.dumps({
                        "success": False,
                        "error": f"{field} must be positive"
                    })
            
            # Validate price logic (high >= low, etc.)
            if price_data["high_price"] < price_data["low_price"]:
                return json.dumps({
                    "success": False,
                    "error": "High price must be greater than or equal to low price"
                })
            
            # Check for existing price for the same instrument and date
            instrument_id = price_data["instrument_id"]
            price_date = price_data["price_date"]
            for existing_price in instrument_prices.values():
                if (existing_price.get("instrument_id") == instrument_id and 
                    existing_price.get("price_date") == price_date):
                    return json.dumps({
                        "success": False,
                        "error": f"Price already exists for instrument {instrument_id} on date {price_date}"
                    })
            
            # Generate new price ID
            existing_ids = [int(pid) for pid in instrument_prices.keys() if pid.isdigit()]
            new_price_id = str(max(existing_ids, default=0) + 1)
            
            # Create new price record
            new_price = {
                "price_id": new_price_id,
                "instrument_id": price_data["instrument_id"],
                "price_date": price_data["price_date"],
                "open_price": price_data["open_price"],
                "high_price": price_data["high_price"],
                "low_price": price_data["low_price"],
                "close_price": price_data["close_price"]
            }
            
            instrument_prices[new_price_id] = new_price
            
            return json.dumps({
                "success": True,
                "action": "create",
                "price_id": new_price_id,
                "message": f"Instrument price {new_price_id} created successfully",
                "price_data": new_price
            })
        
        elif action == "update":
            if not price_id:
                return json.dumps({
                    "success": False,
                    "error": "price_id is required for update action"
                })
            
            if price_id not in instrument_prices:
                return json.dumps({
                    "success": False,
                    "error": f"Instrument price {price_id} not found"
                })
            
            if not price_data:
                return json.dumps({
                    "success": False,
                    "error": "price_data is required for update action"
                })
            
            # Validate only allowed fields are present for updates
            allowed_update_fields = ["open_price", "high_price", "low_price", "close_price", "approval_code"]
            invalid_fields = [field for field in price_data.keys() if field not in allowed_update_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for price update: {', '.join(invalid_fields)}"
                })
            
            # Get current price data for validation
            current_price = instrument_prices[price_id].copy()
            
            # Update current price with new values for validation
            for key, value in price_data.items():
                if key not in ["approval_code"]:
                    current_price[key] = value
            
            # Validate all prices are positive if provided
            price_fields = ["open_price", "high_price", "low_price", "close_price"]
            for field in price_fields:
                if field in price_data and price_data[field] <= 0:
                    return json.dumps({
                        "success": False,
                        "error": f"{field} must be positive"
                    })
            
            # Validate price logic after update
            if current_price["high_price"] < current_price["low_price"]:
                return json.dumps({
                    "success": False,
                    "error": "High price must be greater than or equal to low price"
                })
            
            # Update price record
            updated_price = instrument_prices[price_id].copy()
            for key, value in price_data.items():
                if key not in ["approval_code"]:  # Skip approval_code from being stored
                    updated_price[key] = value
            
            instrument_prices[price_id] = updated_price
            
            return json.dumps({
                "success": True,
                "action": "update",
                "price_id": price_id,
                "message": f"Instrument price {price_id} updated successfully",
                "price_data": updated_price
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manage_instrument_price",
                "description": "Create or update instrument price records in the fund management system. For creation, requires instrument_id, price_date, open_price, high_price, low_price, close_price, and approval_code. For updates, requires price_id and fields to change with approval_code. Ensures one price record per instrument per date and validates price logic.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' or 'update'"
                        },
                        "price_data": {
                            "type": "object",
                            "description": "Price data. For create: instrument_id, price_date, open_price, high_price, low_price, close_price, approval_code. For update: fields to change with approval_code",
                            "additionalProperties": True
                        },
                        "price_id": {
                            "type": "string",
                            "description": "Price ID (required for update action)"
                        }
                    },
                    "required": ["action"]
                }
            }
        }