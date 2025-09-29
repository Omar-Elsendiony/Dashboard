import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ManipulateInstrumentPrice(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, price_data: Dict[str, Any] = None, price_id: str = None) -> str:
        """
        Create or update instrument price records.
        
        Actions:
        - create: Create new price record (requires price_data with instrument_id, price_date, open_price, high_price, low_price, close_price, fund_manager_approval, compliance_officer_approval)
        - update: Update existing price record (requires price_id and price_data with changes, fund_manager_approval, compliance_officer_approval)
        """
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
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
            required_fields = ["instrument_id", "price_date", "open_price", "high_price", "low_price", "close_price", "fund_manager_approval", "compliance_officer_approval"]
            missing_fields = [field for field in required_fields if field not in price_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields for price creation: {', '.join(missing_fields)}. Both Fund Manager and Compliance Officer approvals are required."
                })
            if not (price_data.get("fund_manager_approval") and price_data.get("compliance_officer_approval")):
                return json.dumps({
                    "success": False,
                    "error": "Both Fund Manager and Compliance Officer approvals are required for price creation"
                })
            
            # Validate only allowed fields are present
            allowed_fields = ["instrument_id", "price_date", "open_price", "high_price", "low_price", "close_price", "fund_manager_approval", "compliance_officer_approval"]
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
                        "error": f"{field} must be positive - negative values are not allowed"
                    })
            
            # Validate price logic (high >= low)
            if price_data["high_price"] < price_data["low_price"]:
                return json.dumps({
                    "success": False,
                    "error": "Invalid price data: high price must be greater than or equal to low price"
                })
            
            # Check for existing price for the same instrument and date
            instrument_id = price_data["instrument_id"]
            price_date = price_data["price_date"]
            for existing_price in instrument_prices.values():
                if (existing_price.get("instrument_id") == instrument_id and 
                    existing_price.get("price_date") == price_date):
                    return json.dumps({
                        "success": False,
                        "error": f"Price already exists for instrument {instrument_id} on date {price_date}. Only one price per instrument per date is allowed."
                    })
            
            # Generate new price ID using the same pattern as RegisterFund
            new_price_id = generate_id(instrument_prices)
            
            # Create new price record
            new_price = {
                "price_id": str(new_price_id),
                "instrument_id": price_data["instrument_id"],
                "price_date": price_data["price_date"],
                "open_price": price_data["open_price"],
                "high_price": price_data["high_price"],
                "low_price": price_data["low_price"],
                "close_price": price_data["close_price"]
            }
            
            instrument_prices[str(new_price_id)] = new_price
            
            return json.dumps({
                "success": True,
                "action": "create",
                "price_id": str(new_price_id),
                "message": f"Instrument price {new_price_id} created successfully for instrument {instrument_id} on {price_date}",
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
                    "error": f"Instrument price record {price_id} not found"
                })
            
            if not price_data:
                return json.dumps({
                    "success": False,
                    "error": "price_data is required for update action"
                })
            
            # Validate required approvals for updates
            required_approvals = ["fund_manager_approval", "compliance_officer_approval"]
            missing_approvals = [field for field in required_approvals if field not in price_data]
            if missing_approvals:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required approvals for price update: {', '.join(missing_approvals)}. Both Fund Manager and Compliance Officer approvals are required."
                })
            
            if not (price_data.get("fund_manager_approval") and price_data.get("compliance_officer_approval")):
                return json.dumps({
                    "success": False,
                    "error": "Both Fund Manager and Compliance Officer approvals are required for price update"
                })
            
            # Validate only allowed fields are present for updates
            allowed_update_fields = ["open_price", "high_price", "low_price", "close_price", "fund_manager_approval", "compliance_officer_approval"]
            invalid_fields = [field for field in price_data.keys() if field not in allowed_update_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for price update: {', '.join(invalid_fields)}. Cannot update instrument_id or price_date."
                })
            
            # Get current price data for validation
            current_price = instrument_prices[price_id].copy()
            
            # Update current price with new values for validation
            for key, value in price_data.items():
                if key not in ["fund_manager_approval", "compliance_officer_approval"]:
                    current_price[key] = value
            
            # Validate all prices are positive if provided
            price_fields = ["open_price", "high_price", "low_price", "close_price"]
            for field in price_fields:
                if field in price_data and price_data[field] <= 0:
                    return json.dumps({
                        "success": False,
                        "error": f"{field} must be positive - negative values are not allowed"
                    })
            
            # Validate price logic after update
            if current_price["high_price"] < current_price["low_price"]:
                return json.dumps({
                    "success": False,
                    "error": "Invalid price data: high price must be greater than or equal to low price"
                })
            
            # Update price record
            updated_price = instrument_prices[price_id].copy()
            for key, value in price_data.items():
                if key not in ["fund_manager_approval", "compliance_officer_approval"]:
                    updated_price[key] = value
            
            instrument_prices[price_id] = updated_price
            
            return json.dumps({
                "success": True,
                "action": "update",
                "price_id": str(price_id),
                "message": f"Instrument price {price_id} updated successfully",
                "price_data": updated_price
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manipulate_instrument_price",
                "description": "Create or update instrument price records in the fund management system. This tool manages daily pricing data for financial instruments, including open, high, low, and close prices with high precision. For creation, establishes new price records with comprehensive validation to ensure data integrity and prevents duplicate entries for the same instrument and date. For updates, modifies existing price records while maintaining data integrity. Both operations require dual approval from Fund Manager and Compliance Officer as mandated by regulatory requirements. Validates price logic (high price >= low price), ensures positive values, and prevents future-dated entries. Essential for accurate NAV calculations, portfolio valuations, and regulatory reporting. Supports the complete instrument pricing lifecycle from initial price establishment to ongoing market data updates.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' to establish new instrument price record, 'update' to modify existing price record",
                            "enum": ["create", "update"]
                        },
                        "price_data": {
                            "type": "object",
                            "description": "Price data object. For create: requires instrument_id, price_date (cannot be future), open_price (positive), high_price (positive, >= low_price), low_price (positive, <= high_price), close_price (positive), fund_manager_approval (approval code), compliance_officer_approval (approval code). For update: includes price fields to change with both approval codes (instrument_id and price_date cannot be updated). SYNTAX: {\"key\": \"value\"}",
                            "properties": {
                                "instrument_id": {
                                    "type": "string",
                                    "description": "Unique identifier of the financial instrument (required for create only, cannot be updated)"
                                },
                                "price_date": {
                                    "type": "string",
                                    "description": "Date of the price record in YYYY-MM-DD format (required for create only, cannot be updated, cannot be future date, unique with instrument_id)"
                                },
                                "open_price": {
                                    "type": "number",
                                    "description": "Opening price of the instrument (high precision, must be positive)"
                                },
                                "high_price": {
                                    "type": "number",
                                    "description": "Highest price during trading period (high precision, must be >= low_price and positive)"
                                },
                                "low_price": {
                                    "type": "number",
                                    "description": "Lowest price during trading period (high precision, must be <= high_price and positive)"
                                },
                                "close_price": {
                                    "type": "number",
                                    "description": "Closing price of the instrument (high precision, must be positive)"
                                },
                                "fund_manager_approval": {
                                    "type": "boolean",
                                    "description": "Fund Manager approval presence (True/False) (required for both create and update operations)"
                                },
                                "compliance_officer_approval": {
                                    "type": "boolean",
                                    "description": "Compliance Officer approval presence (True/False) (required for both create and update operations)"
                                }
                            }
                        },
                        "price_id": {
                            "type": "string",
                            "description": "Unique identifier of the price record (required for update action only)"
                        }
                    },
                    "required": ["action"]
                }
            }
        }