import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ManipulateFund(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, fund_data: Dict[str, Any] = None, fund_id: str = None) -> str:
        """
        Create or update fund records.
        
        Actions:
        - create: Create new fund (requires fund_data with name, fund_type, manager_id, fund_manager_approval, compliance_officer_approval, 
                 optional size, base_currency, status)
        - update: Update existing fund (requires fund_id and fund_data with changes, fund_manager_approval, 
                 compliance_officer_approval)
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
        
        # Access funds data
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for funds"
            })
        
        funds = data.get("funds", {})
        
        if action == "create":
            if not fund_data:
                return json.dumps({
                    "success": False,
                    "error": "fund_data is required for create action"
                })
            
            # Validate required fields for creation
            required_fields = ["name", "fund_type", "manager_id", "fund_manager_approval", "compliance_officer_approval"]
            missing_fields = [field for field in required_fields if field not in fund_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields for fund creation: {', '.join(missing_fields)}. Both Fund Manager and Compliance Officer approvals are required."
                })
            
            # Validate both approvals are present and true
            if not (fund_data.get("fund_manager_approval") and fund_data.get("compliance_officer_approval")):
                return json.dumps({
                    "success": False,
                    "error": "Both Fund Manager and Compliance Officer approvals are required for fund creation"
                })
            
            # Validate only allowed fields are present
            allowed_fields = ["name", "fund_type", "size", "base_currency", "manager_id", "status", "fund_manager_approval", "compliance_officer_approval"]
            invalid_fields = [field for field in fund_data.keys() if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for fund creation: {', '.join(invalid_fields)}"
                })
            
            # Validate fund_type enum
            valid_fund_types = ["equity_funds", "bond_funds", "multi_asset_funds", "money_market_funds", "hedge_funds", "private_equity_funds", "real_estate_funds"]
            if fund_data["fund_type"] not in valid_fund_types:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fund_type. Must be one of: {', '.join(valid_fund_types)}"
                })
            
            # Validate size if provided (must be positive number)
            if "size" in fund_data:
                try:
                    size_value = float(fund_data["size"])
                    if size_value <= 0:
                        return json.dumps({
                            "success": False,
                            "error": "Fund size must be a positive number"
                        })
                except (ValueError, TypeError):
                    return json.dumps({
                        "success": False,
                        "error": "Fund size must be a valid number"
                    })
            
            # Validate status if provided
            if "status" in fund_data:
                valid_statuses = ["open", "closed"]
                if fund_data["status"] not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                    })
            
            # Check for duplicate fund name
            fund_name = fund_data["name"].strip()
            for existing_fund in funds.values():
                if existing_fund.get("name", "").strip().lower() == fund_name.lower():
                    return json.dumps({
                        "success": False,
                        "error": f"Fund with name '{fund_name}' already exists"
                    })
            
            # Generate new fund ID using the same pattern as manage_instrument_price
            new_fund_id = generate_id(funds)
            
            # Create new fund record
            new_fund = {
                "fund_id": str(new_fund_id),
                "name": fund_data["name"],
                "fund_type": fund_data["fund_type"],
                "size": fund_data.get("size"),
                "base_currency": fund_data.get("base_currency", "USD"),
                "manager_id": str(fund_data["manager_id"]),
                "status": fund_data.get("status", "open"),
                "created_at": "2025-10-01T12:00:00",
                "updated_at": "2025-10-01T12:00:00"
            }
            
            funds[str(new_fund_id)] = new_fund
            
            return json.dumps({
                "success": True,
                "action": "create",
                "fund_id": str(new_fund_id),
                "message": f"Fund {new_fund_id} created successfully with name '{fund_data['name']}'",
                "fund_data": new_fund
            })
        
        elif action == "update":
            if not fund_id:
                return json.dumps({
                    "success": False,
                    "error": "fund_id is required for update action"
                })
            
            if fund_id not in funds:
                return json.dumps({
                    "success": False,
                    "error": f"Fund {fund_id} not found"
                })
            
            if not fund_data:
                return json.dumps({
                    "success": False,
                    "error": "fund_data is required for update action"
                })
            
            # Validate required approvals for updates
            required_approvals = ["fund_manager_approval", "compliance_officer_approval"]
            missing_approvals = [field for field in required_approvals if field not in fund_data]
            if missing_approvals:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required approvals for fund update: {', '.join(missing_approvals)}. Both Fund Manager and Compliance Officer approvals are required."
                })
            
            # Validate both approvals are present and true
            if not (fund_data.get("fund_manager_approval") and fund_data.get("compliance_officer_approval")):
                return json.dumps({
                    "success": False,
                    "error": "Both Fund Manager and Compliance Officer approvals are required for fund update"
                })
            
            # Validate only allowed fields are present for updates
            allowed_update_fields = ["name", "fund_type", "size", "base_currency", "manager_id", "status", 
                                   "fund_manager_approval", "compliance_officer_approval"]
            invalid_fields = [field for field in fund_data.keys() if field not in allowed_update_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for fund update: {', '.join(invalid_fields)}"
                })
            
            # Validate fund_type enum if provided
            if "fund_type" in fund_data:
                valid_fund_types = ["equity_funds", "bond_funds", "multi_asset_funds", "money_market_funds", "hedge_funds", "private_equity_funds", "real_estate_funds"]
                if fund_data["fund_type"] not in valid_fund_types:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid fund_type. Must be one of: {', '.join(valid_fund_types)}"
                    })
            
            # Validate size if provided
            if "size" in fund_data:
                try:
                    size_value = float(fund_data["size"])
                    if size_value <= 0:
                        return json.dumps({
                            "success": False,
                            "error": "Fund size must be a positive number"
                        })
                except (ValueError, TypeError):
                    return json.dumps({
                        "success": False,
                        "error": "Fund size must be a valid number"
                    })
            
            # Validate status transitions
            current_fund = funds[fund_id]
            current_status = current_fund.get("status", "open")
            if "status" in fund_data:
                new_status = fund_data["status"]
                valid_statuses = ["open", "closed"]
                
                if new_status not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                    })
                
                # Define invalid status transitions
                invalid_transitions = {
                    "closed": ["open"]  # Cannot reopen closed fund
                }
                
                if current_status in invalid_transitions and new_status in invalid_transitions[current_status]:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid transition from {current_status} to {new_status}"
                    })
            
            # Check for duplicate fund name if updating name
            if "name" in fund_data:
                new_fund_name = fund_data["name"].strip()
                for existing_fund_id, existing_fund in funds.items():
                    if (existing_fund_id != fund_id and 
                        existing_fund.get("name", "").strip().lower() == new_fund_name.lower()):
                        return json.dumps({
                            "success": False,
                            "error": f"Fund with name '{new_fund_name}' already exists"
                        })
            
            # Update fund record
            updated_fund = current_fund.copy()
            for key, value in fund_data.items():
                if key not in ["fund_manager_approval", "compliance_officer_approval"]:  # Skip approval codes
                    updated_fund[key] = value
            
            updated_fund["updated_at"] = "2025-10-01T12:00:00"
            funds[fund_id] = updated_fund
            
            return json.dumps({
                "success": True,
                "action": "update",
                "fund_id": str(fund_id),
                "message": f"Fund {fund_id} updated successfully",
                "fund_data": updated_fund
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manipulate_fund",
                "description": "Create or update fund records in the fund management system. This tool manages the complete fund lifecycle including creation of new investment funds and updates to existing fund configurations. For creation, establishes new fund records with comprehensive validation to ensure regulatory compliance and business rule adherence. For updates, modifies existing fund records while maintaining data integrity and enforcing valid status transitions. Both operations require dual approval from Fund Manager and Compliance Officer as mandated by regulatory requirements and internal governance policies. Validates fund types, enforces positive sizing constraints, prevents duplicate fund names, and manages fund status transitions according to business rules. Essential for fund administration, regulatory compliance, and investment management operations. Supports the complete fund management lifecycle from initial fund establishment to ongoing fund administration and eventual fund closure.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' to establish new fund record, 'update' to modify existing fund record",
                            "enum": ["create", "update"]
                        },
                        "fund_data": {
                            "type": "object",
                            "description": "Fund data object. For create: requires name (unique fund name), fund_type (from valid enum), manager_id (fund manager identifier), fund_manager_approval (approval code), compliance_officer_approval (approval code), optional size (positive number), base_currency (defaults to USD), status (defaults to active). For update: includes fund fields to change with both approval codes. SYNTAX: {\"key\": \"value\"}",
                            "properties": {
                                "name": {
                                    "type": "string",
                                    "description": "Fund name (must be unique across all funds, required for create)"
                                },
                                "fund_type": {
                                    "type": "string",
                                    "description": "Type of fund from valid enum (required for create)",
                                    "enum": ["equity_funds", "bond_funds", "multi_asset_funds", "money_market_funds", "hedge_funds", "private_equity_funds", "real_estate_funds"]
                                },
                                "size": {
                                    "type": "number",
                                    "description": "Initial fund size in base currency (must be positive number, optional)"
                                },
                                "base_currency": {
                                    "type": "string",
                                    "description": "Base currency for fund operations (optional, defaults to USD)"
                                },
                                "manager_id": {
                                    "type": "string",
                                    "description": "Unique identifier of the fund manager (required for create)"
                                },
                                "status": {
                                    "type": "string",
                                    "description": "Fund operational status (optional, defaults to open)",
                                    "enum": ["open", "closed"]
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
                        "fund_id": {
                            "type": "string",
                            "description": "Unique identifier of the fund (required for update action only)"
                        }
                    },
                    "required": ["action"]
                }
            }
        }