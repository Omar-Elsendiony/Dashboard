import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ProcessFund(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, fund_data: Dict[str, Any] = None, fund_id: str = None) -> str:
        """
        Create or update fund records.
        
        Actions:
        - create: Create new fund (requires fund_data with fund_name, fund_type, manager_id, approval_code, 
                 optional , size)
        - update: Update existing fund (requires fund_id and fund_data with change_set, fund_manager_approval, 
                 compliance_officer_approval)
        """
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
            required_fields = ["name", "fund_type", "manager_id", "approval_code"]
            missing_fields = [field for field in required_fields if field not in fund_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields for fund creation: {', '.join(missing_fields)}"
                })
            
            # Validate only allowed fields are present
            allowed_fields = ["name", "fund_type", "size", "manager_id", "approval_code", "status"]
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
                valid_statuses = ["active", "inactive", "closed", "liquidating"]
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
            
            # Generate new fund ID
            existing_ids = [int(fid) for fid in funds.keys() if fid.isdigit()]
            new_fund_id = str(max(existing_ids, default=0) + 1)
            
            # Create new fund record
            new_fund = {
                "fund_id": new_fund_id,
                "name": fund_data["name"],
                "fund_type": fund_data["fund_type"],
                "size": fund_data.get("size"),
                "manager_id": fund_data["manager_id"],
                "status": fund_data.get("status", "active"),
                "created_at": "2025-10-01T12:00:00",
                "updated_at": "2025-10-01T12:00:00"
            }
            
            funds[new_fund_id] = new_fund
            
            return json.dumps({
                "success": True,
                "action": "create",
                "fund_id": new_fund_id,
                "message": f"Fund {new_fund_id} created successfully",
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
            
            # Validate required approvals for update
            required_approvals = ["fund_manager_approval", "compliance_officer_approval"]
            missing_approvals = [field for field in required_approvals if field not in fund_data]
            if missing_approvals:
                return json.dumps({
                    "success": False,
                    "error": f"Required approvals not provided: {', '.join(missing_approvals)}"
                })
            
            # Validate only allowed fields are present for updates
            allowed_update_fields = ["name", "fund_type", "size", "manager_id", "status", 
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
            current_status = current_fund.get("status", "active")
            if "status" in fund_data:
                new_status = fund_data["status"]
                valid_statuses = ["active", "inactive", "closed", "liquidating"]
                
                if new_status not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                    })
                
                # Define invalid status transitions
                invalid_transitions = {
                    "closed": ["active", "inactive"],  # Cannot reactivate closed fund
                    "liquidating": ["active", "inactive"]  # Cannot reactivate liquidating fund
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
                "fund_id": fund_id,
                "message": f"Fund {fund_id} updated successfully",
                "fund_data": updated_fund
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "process_fund",
                "description": "Create or update fund records in the fund management system. For creation, requires fund_name, fund_type, manager_id, and approval_code with optional size. For updates, requires fund_id, change_set, and both Fund Manager and Compliance Officer approvals. Validates business rules and status transitions.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' or 'update'"
                        },
                        "fund_data": {
                            "type": "object",
                            "description": "Fund data. For create: fund_name, fund_type, manager_id, approval_code, optional  size, status. For update: change_set with fund_manager_approval and compliance_officer_approval"
                        },
                        "fund_id": {
                            "type": "string",
                            "description": "Fund ID (required for update action)"
                        }
                    },
                    "required": ["action"]
                }
            }
        }