import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ManagePortfolioHoldings(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, holding_data: Dict[str, Any] = None, holding_id: str = None) -> str:
        """
        Create or update portfolio holdings records.
        
        Actions:
        - create: Create new holding (requires holding_data with portfolio_id, fund_id, quantity, cost_basis, approval_code)
        - update: Update existing holding (requires holding_id and holding_data with changes like quantity, cost_basis, approval_code)
        """
        if action not in ["create", "update"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid action '{action}'. Must be 'create' or 'update'"
            })
        
        # Access portfolio_holdings data
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for portfolio_holdings"
            })
        
        portfolio_holdings = data.get("portfolio_holdings", {})
        
        if action == "create":
            if not holding_data:
                return json.dumps({
                    "success": False,
                    "error": "holding_data is required for create action"
                })
            
            # Validate required fields for creation
            required_fields = ["portfolio_id", "fund_id", "quantity", "cost_basis", "approval_code"]
            missing_fields = [field for field in required_fields if field not in holding_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields for holding creation: {', '.join(missing_fields)}"
                })
            
            # Validate only allowed fields are present
            allowed_fields = ["portfolio_id", "fund_id", "quantity", "cost_basis", "approval_code"]
            invalid_fields = [field for field in holding_data.keys() if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for holding creation: {', '.join(invalid_fields)}"
                })
            
            # Validate quantity and cost_basis are positive
            if holding_data["quantity"] <= 0:
                return json.dumps({
                    "success": False,
                    "error": "Quantity must be positive"
                })
            
            if holding_data["cost_basis"] <= 0:
                return json.dumps({
                    "success": False,
                    "error": "Cost basis must be positive"
                })
            
            # Check if fund already exists in portfolio (one fund per portfolio constraint)
            portfolio_id = holding_data["portfolio_id"]
            fund_id = holding_data["fund_id"]
            for existing_holding in portfolio_holdings.values():
                if (existing_holding.get("portfolio_id") == portfolio_id and 
                    existing_holding.get("fund_id") == fund_id):
                    return json.dumps({
                        "success": False,
                        "error": f"Fund {fund_id} already exists in portfolio {portfolio_id}"
                    })
            
            # Generate new holding ID
            existing_ids = [int(hid) for hid in portfolio_holdings.keys() if hid.isdigit()]
            new_holding_id = str(max(existing_ids, default=0) + 1)
            
            # Create new holding record
            new_holding = {
                "holding_id": new_holding_id,
                "portfolio_id": holding_data["portfolio_id"],
                "fund_id": holding_data["fund_id"],
                "quantity": holding_data["quantity"],
                "cost_basis": holding_data["cost_basis"],
                "created_at": "2025-10-01T12:00:00"
            }
            
            portfolio_holdings[new_holding_id] = new_holding
            
            return json.dumps({
                "success": True,
                "action": "create",
                "holding_id": new_holding_id,
                "message": f"Portfolio holding {new_holding_id} created successfully",
                "holding_data": new_holding
            })
        
        elif action == "update":
            if not holding_id:
                return json.dumps({
                    "success": False,
                    "error": "holding_id is required for update action"
                })
            
            if holding_id not in portfolio_holdings:
                return json.dumps({
                    "success": False,
                    "error": f"Portfolio holding {holding_id} not found"
                })
            
            if not holding_data:
                return json.dumps({
                    "success": False,
                    "error": "holding_data is required for update action"
                })
            
            # Validate only allowed fields are present for updates
            allowed_update_fields = ["quantity", "cost_basis", "approval_code"]
            invalid_fields = [field for field in holding_data.keys() if field not in allowed_update_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for holding update: {', '.join(invalid_fields)}"
                })
            
            # Validate quantity and cost_basis are positive if provided
            if "quantity" in holding_data and holding_data["quantity"] <= 0:
                return json.dumps({
                    "success": False,
                    "error": "Quantity must be positive"
                })
            
            if "cost_basis" in holding_data and holding_data["cost_basis"] <= 0:
                return json.dumps({
                    "success": False,
                    "error": "Cost basis must be positive"
                })
            
            # Update holding record
            updated_holding = portfolio_holdings[holding_id].copy()
            for key, value in holding_data.items():
                if key not in ["approval_code"]:  # Skip approval_code from being stored
                    updated_holding[key] = value
            
            portfolio_holdings[holding_id] = updated_holding
            
            return json.dumps({
                "success": True,
                "action": "update",
                "holding_id": holding_id,
                "message": f"Portfolio holding {holding_id} updated successfully",
                "holding_data": updated_holding
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manage_portfolio_holdings",
                "description": "Create or update portfolio holdings records in the fund management system. For creation, requires portfolio_id, fund_id, quantity, cost_basis, and approval_code. For updates, requires holding_id and fields to change with approval_code. Ensures one fund per portfolio constraint and validates positive values.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' or 'update'"
                        },
                        "holding_data": {
                            "type": "object",
                            "description": "Holding data. For create: portfolio_id, fund_id, quantity, cost_basis, approval_code. For update: fields to change with approval_code",
                            "additionalProperties": True
                        },
                        "holding_id": {
                            "type": "string",
                            "description": "Holding ID (required for update action)"
                        }
                    },
                    "required": ["action"]
                }
            }
        }