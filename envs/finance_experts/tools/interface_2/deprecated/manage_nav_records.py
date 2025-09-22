import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool



class ManageNavRecords(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, nav_data: Dict[str, Any] = None, nav_id: str = None) -> str:
        """
        Create or update NAV records.
        
        Actions:
        - create: Create new NAV record (requires nav_data with fund_id, nav_date, nav_value, approval_code)
        - update: Update existing NAV record (requires nav_id and nav_data with changes like nav_value, approval_code)
        """
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
            required_fields = ["fund_id", "nav_date", "nav_value", "approval_code"]
            missing_fields = [field for field in required_fields if field not in nav_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields for NAV creation: {', '.join(missing_fields)}"
                })
            
            # Validate only allowed fields are present
            allowed_fields = ["fund_id", "nav_date", "nav_value", "approval_code"]
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
                    "error": "NAV value must be positive"
                })
            
            # Check for existing NAV for the same fund and date
            fund_id = nav_data["fund_id"]
            nav_date = nav_data["nav_date"]
            for existing_nav in nav_records.values():
                if (existing_nav.get("fund_id") == fund_id and 
                    existing_nav.get("nav_date") == nav_date):
                    return json.dumps({
                        "success": False,
                        "error": f"NAV already exists for fund {fund_id} on date {nav_date}"
                    })
            
            # Generate new NAV ID
            existing_ids = [int(nid) for nid in nav_records.keys() if nid.isdigit()]
            new_nav_id = str(max(existing_ids, default=0) + 1)
            
            # Create new NAV record
            new_nav = {
                "nav_id": new_nav_id,
                "fund_id": nav_data["fund_id"],
                "nav_date": nav_data["nav_date"],
                "nav_value": nav_data["nav_value"],
                "updated_at": "2025-10-01T12:00:00"
            }
            
            nav_records[new_nav_id] = new_nav
            
            return json.dumps({
                "success": True,
                "action": "create",
                "nav_id": new_nav_id,
                "message": f"NAV record {new_nav_id} created successfully",
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
            
            # Validate only allowed fields are present for updates
            allowed_update_fields = ["nav_value", "approval_code"]
            invalid_fields = [field for field in nav_data.keys() if field not in allowed_update_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for NAV update: {', '.join(invalid_fields)}"
                })
            
            # Validate NAV value is positive if provided
            if "nav_value" in nav_data and nav_data["nav_value"] <= 0:
                return json.dumps({
                    "success": False,
                    "error": "NAV value must be positive"
                })
            
            # Update NAV record
            updated_nav = nav_records[nav_id].copy()
            for key, value in nav_data.items():
                if key not in ["approval_code"]:  # Skip approval_code from being stored
                    updated_nav[key] = value
            
            updated_nav["updated_at"] = "2025-10-01T12:00:00"
            nav_records[nav_id] = updated_nav
            
            return json.dumps({
                "success": True,
                "action": "update",
                "nav_id": nav_id,
                "message": f"NAV record {nav_id} updated successfully",
                "nav_data": updated_nav
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manage_nav_records",
                "description": "Create or update NAV records in the fund management system. For creation, requires fund_id, nav_date, nav_value, and approval_code. For updates, requires nav_id and fields to change with approval_code. Ensures one NAV record per fund per date and validates positive NAV values.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' or 'update'"
                        },
                        "nav_data": {
                            "type": "object",
                            "description": "NAV data. For create: fund_id, nav_date, nav_value, approval_code. For update: fields to change with approval_code"
                        },
                        "nav_id": {
                            "type": "string",
                            "description": "NAV ID (required for update action)"
                        }
                    },
                    "required": ["action"]
                }
            }
        }