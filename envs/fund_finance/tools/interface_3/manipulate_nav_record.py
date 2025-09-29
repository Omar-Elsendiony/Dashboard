import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ManipulateNavRecord(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, nav_data: Dict[str, Any] = None, nav_id: str = None) -> str:
        """
        Create or update NAV records.
        
        Actions:
        - create: Create new NAV record (requires nav_data with fund_id, nav_date, nav_value, finance_officer_approval)
        - update: Update existing NAV record (requires nav_id and nav_data with changes, finance_officer_approval, fund_manager_approval)
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
        
        # Access nav_records data
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for nav_records"
            })
        
        nav_records = data.get("nav_records", {})
        
        if action == "create":
            if not nav_data:
                return json.dumps({
                    "success": False,
                    "error": "nav_data is required for create action"
                })
            
            # Validate required fields for creation
            required_fields = ["fund_id", "nav_date", "nav_value", "finance_officer_approval"]
            missing_fields = [field for field in required_fields if field not in nav_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields for NAV creation: {', '.join(missing_fields)}. Finance Officer approval is required."
                })
            
            # Validate that finance_officer_approval is True
            if not nav_data.get("finance_officer_approval"):
                return json.dumps({
                    "success": False,
                    "error": "Finance Officer approval must be True for NAV creation"
                })
            
            # Validate only allowed fields are present
            allowed_fields = ["fund_id", "nav_date", "nav_value", "finance_officer_approval"]
            invalid_fields = [field for field in nav_data.keys() if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for NAV creation: {', '.join(invalid_fields)}"
                })
            
            # Validate NAV value is positive
            if nav_data["nav_value"] <= 0:
                return json.dumps({
                    "success": False,
                    "error": "NAV value must be positive - negative or zero values are not allowed"
                })
            
            # Validate that nav_date is not in the future (using current system date)
            current_date = "2025-10-01"  # Based on policy current date
            if nav_data["nav_date"] > current_date:
                return json.dumps({
                    "success": False,
                    "error": "Invalid NAV date: cannot create NAV record with future date"
                })
            
            # Check for existing NAV for the same fund and date
            fund_id = nav_data["fund_id"]
            nav_date = nav_data["nav_date"]
            for existing_nav in nav_records.values():
                if (existing_nav.get("fund_id") == fund_id and 
                    existing_nav.get("nav_date") == nav_date):
                    return json.dumps({
                        "success": False,
                        "error": f"NAV already exists for fund {fund_id} on date {nav_date}. Only one NAV per fund per date is allowed."
                    })
            
            # Generate new NAV ID using the same pattern as other tools
            new_nav_id = generate_id(nav_records)
            
            # Create new NAV record
            new_nav = {
                "nav_id": str(new_nav_id),
                "fund_id": str(nav_data["fund_id"]),
                "nav_date": nav_data["nav_date"],
                "nav_value": nav_data["nav_value"],
                "updated_at": "2025-10-01T12:00:00"
            }
            
            nav_records[str(new_nav_id)] = new_nav
            
            return json.dumps({
                "success": True,
                "action": "create",
                "nav_id": str(new_nav_id),
                "message": f"NAV record {new_nav_id} created successfully for fund {fund_id} on {nav_date}",
                "nav_data": new_nav
            })
        
        elif action == "update":
            if not nav_id:
                return json.dumps({
                    "success": False,
                    "error": "nav_id is required for update action"
                })
            
            if nav_id not in nav_records:
                return json.dumps({
                    "success": False,
                    "error": f"NAV record {nav_id} not found"
                })
            
            if not nav_data:
                return json.dumps({
                    "success": False,
                    "error": "nav_data is required for update action"
                })
            
            # Validate required approvals for updates (both Finance Officer and Fund Manager required)
            required_approvals = ["finance_officer_approval", "fund_manager_approval"]
            missing_approvals = [field for field in required_approvals if field not in nav_data]
            if missing_approvals:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required approvals for NAV update: {', '.join(missing_approvals)}. Both Finance Officer and Fund Manager approvals are required."
                })
            
            # Validate that both approvals are True
            if not (nav_data.get("finance_officer_approval") and nav_data.get("fund_manager_approval")):
                return json.dumps({
                    "success": False,
                    "error": "Both Finance Officer and Fund Manager approvals must be True for NAV update"
                })
            
            # Validate only allowed fields are present for updates (cannot update fund_id or nav_date)
            allowed_update_fields = ["nav_value", "finance_officer_approval", "fund_manager_approval"]
            invalid_fields = [field for field in nav_data.keys() if field not in allowed_update_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for NAV update: {', '.join(invalid_fields)}. Cannot update fund_id or nav_date."
                })
            
            # Validate NAV value is positive if provided
            if "nav_value" in nav_data and nav_data["nav_value"] <= 0:
                return json.dumps({
                    "success": False,
                    "error": "NAV value must be positive - negative or zero values are not allowed"
                })
            
            # Update NAV record
            updated_nav = nav_records[nav_id].copy()
            for key, value in nav_data.items():
                if key not in ["finance_officer_approval", "fund_manager_approval"]:  # Skip approval codes from being stored
                    updated_nav[key] = value
            
            updated_nav["updated_at"] = "2025-10-01T12:00:00"
            nav_records[nav_id] = updated_nav
            
            return json.dumps({
                "success": True,
                "action": "update",
                "nav_id": str(nav_id) if nav_id is not None else None,
                "message": f"NAV record {nav_id} updated successfully",
                "nav_data": updated_nav
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manipulate_nav_record",
                "description": "Create or update NAV (Net Asset Value) records in the fund management system. This tool manages daily NAV calculations and updates for financial funds with comprehensive validation to ensure data integrity and regulatory compliance. For creation, establishes new NAV records with validation to prevent duplicate entries for the same fund and date combination, requiring Finance Officer approval. For updates, modifies existing NAV records while maintaining data integrity and requires both Finance Officer and Fund Manager approvals as mandated by regulatory requirements for material changes. Validates positive NAV values, prevents future-dated entries, and enforces proper business rules. Essential for accurate fund valuations, investor reporting, and regulatory compliance. Supports the complete NAV lifecycle from initial calculation to ongoing market-based adjustments.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' to establish new NAV record, 'update' to modify existing NAV record",
                            "enum": ["create", "update"]
                        },
                        "nav_data": {
                            "type": "object",
                            "description": "NAV data object. For create: requires fund_id, nav_date (cannot be future), nav_value (positive), finance_officer_approval (approval code). For update: includes nav_value to change with both finance_officer_approval and fund_manager_approval (fund_id and nav_date cannot be updated). SYNTAX: {\"key\": \"value\"}",
                            "properties": {
                                "fund_id": {
                                    "type": "string",
                                    "description": "Unique identifier of the fund (required for create only, cannot be updated, unique with nav_date)"
                                },
                                "nav_date": {
                                    "type": "string",
                                    "description": "Date of the NAV record in YYYY-MM-DD format (required for create only, cannot be updated, cannot be future date, unique with fund_id)"
                                },
                                "nav_value": {
                                    "type": "number",
                                    "description": "Net Asset Value with high precision (must be positive)"
                                },
                                "finance_officer_approval": {
                                    "type": "boolean",
                                    "description": "Finance Officer approval presence (True/False) (required for both create and update operations)"
                                },
                                "fund_manager_approval": {
                                    "type": "boolean",
                                    "description": "Fund Manager approval presence (True/False) (required for update operations only, for material changes)"
                                }
                            }
                        },
                        "nav_id": {
                            "type": "string",
                            "description": "Unique identifier of the NAV record (required for update action only)"
                        }
                    },
                    "required": ["action"]
                }
            }
        }