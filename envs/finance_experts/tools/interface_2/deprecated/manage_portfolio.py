import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ManagePortfolio(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, portfolio_data: Dict[str, Any] = None, portfolio_id: str = None) -> str:
        """
        Create or update portfolio records.
        
        Actions:
        - create: Create new portfolio (requires portfolio_data with investor_id, approval_code, optional status)
        - update: Update existing portfolio (requires portfolio_id and portfolio_data with changes like status, approval_code)
        """
        if action not in ["create", "update"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid action '{action}'. Must be 'create' or 'update'"
            })
        
        # Access portfolios data
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for portfolios"
            })
        
        portfolios = data.get("portfolios", {})
        
        if action == "create":
            if not portfolio_data:
                return json.dumps({
                    "success": False,
                    "error": "portfolio_data is required for create action"
                })
            
            # Validate required fields for creation
            required_fields = ["investor_id", "approval_code"]
            missing_fields = [field for field in required_fields if field not in portfolio_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields for portfolio creation: {', '.join(missing_fields)}"
                })
            
            # Validate only allowed fields are present
            allowed_fields = ["investor_id", "status", "approval_code"]
            invalid_fields = [field for field in portfolio_data.keys() if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for portfolio creation: {', '.join(invalid_fields)}"
                })
            
            # Validate status enum if provided
            if "status" in portfolio_data:
                valid_statuses = ["active", "inactive", "archived"]
                if portfolio_data["status"] not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                    })
            
            # Check if investor already has an active portfolio
            investor_id = portfolio_data["investor_id"]
            for existing_portfolio in portfolios.values():
                if (existing_portfolio.get("investor_id") == investor_id and 
                    existing_portfolio.get("status") == "active"):
                    return json.dumps({
                        "success": False,
                        "error": f"Investor {investor_id} already has an active portfolio"
                    })
            
            # Generate new portfolio ID
            existing_ids = [int(pid) for pid in portfolios.keys() if pid.isdigit()]
            new_portfolio_id = str(max(existing_ids, default=0) + 1)
            
            # Create new portfolio record
            new_portfolio = {
                "portfolio_id": new_portfolio_id,
                "investor_id": portfolio_data["investor_id"],
                "status": portfolio_data.get("status", "active"),
                "created_at": "2025-10-01T12:00:00",
                "updated_at": "2025-10-01T12:00:00"
            }
            
            portfolios[new_portfolio_id] = new_portfolio
            
            return json.dumps({
                "success": True,
                "action": "create",
                "portfolio_id": new_portfolio_id,
                "message": f"Portfolio {new_portfolio_id} created successfully",
                "portfolio_data": new_portfolio
            })
        
        elif action == "update":
            if not portfolio_id:
                return json.dumps({
                    "success": False,
                    "error": "portfolio_id is required for update action"
                })
            
            if portfolio_id not in portfolios:
                return json.dumps({
                    "success": False,
                    "error": f"Portfolio {portfolio_id} not found"
                })
            
            if not portfolio_data:
                return json.dumps({
                    "success": False,
                    "error": "portfolio_data is required for update action"
                })
            
            # Validate only allowed fields are present for updates
            allowed_update_fields = ["status", "approval_code"]
            invalid_fields = [field for field in portfolio_data.keys() if field not in allowed_update_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for portfolio update: {', '.join(invalid_fields)}"
                })
            
            # Validate status enum if provided
            if "status" in portfolio_data:
                valid_statuses = ["active", "inactive", "archived"]
                if portfolio_data["status"] not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                    })
            
            # Update portfolio record
            updated_portfolio = portfolios[portfolio_id].copy()
            for key, value in portfolio_data.items():
                if key not in ["approval_code"]:  # Skip approval_code from being stored
                    updated_portfolio[key] = value
            
            updated_portfolio["updated_at"] = "2025-10-01T12:00:00"
            portfolios[portfolio_id] = updated_portfolio
            
            return json.dumps({
                "success": True,
                "action": "update", 
                "portfolio_id": portfolio_id,
                "message": f"Portfolio {portfolio_id} updated successfully",
                "portfolio_data": updated_portfolio
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manage_portfolio",
                "description": "Create or update portfolio records in the fund management system. For creation, requires investor_id and approval_code, with optional status (defaults to 'active'). For updates, requires portfolio_id and fields to change with approval_code. Ensures one investor can only have one active portfolio.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' or 'update'"
                        },
                        "portfolio_data": {
                            "type": "object",
                            "description": "Portfolio data. For create: investor_id, approval_code, optional status. For update: fields to change with approval_code"
                        },
                        "portfolio_id": {
                            "type": "string",
                            "description": "Portfolio ID (required for update action)"
                        }
                    },
                    "required": ["action"]
                }
            }
        }
