import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ManagePortfolioHoldings(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, holding_data: Dict[str, Any] = None, holding_id: str = None) -> str:
        """
        Create or update portfolio holdings records.
        
        Actions:
        - create: Create new holding (requires holding_data with portfolio_id, fund_id, quantity, cost_basis, fund_manager_approval)
        - update: Update existing holding (requires holding_id and holding_data with changes like quantity, cost_basis, fund_manager_approval)
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
            
            required_fields = ["portfolio_id", "fund_id", "quantity", "cost_basis", "fund_manager_approval"]
            missing_fields = [field for field in required_fields if field not in holding_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields for holding creation: {', '.join(missing_fields)}. Fund Manager approval is required."
                })
            
            if not holding_data.get("fund_manager_approval"):
                return json.dumps({
                    "success": False,
                    "error": "Fund Manager approval is required for holding creation"
                })
            
            allowed_fields = ["portfolio_id", "fund_id", "quantity", "cost_basis", "fund_manager_approval"]
            invalid_fields = [field for field in holding_data.keys() if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for holding creation: {', '.join(invalid_fields)}"
                })
            
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
            
            portfolio_id = holding_data["portfolio_id"]
            fund_id = holding_data["fund_id"]
            for existing_holding in portfolio_holdings.values():
                if (existing_holding.get("portfolio_id") == portfolio_id and 
                    existing_holding.get("fund_id") == fund_id):
                    return json.dumps({
                        "success": False,
                        "error": f"Fund {fund_id} already exists in portfolio {portfolio_id}. Only one holding per fund per portfolio is allowed."
                    })
            
            new_holding_id = generate_id(portfolio_holdings)
            
            new_holding = {
                "holding_id": str(new_holding_id),
                "portfolio_id": str(holding_data["portfolio_id"]),
                "fund_id": str(holding_data["fund_id"]),
                "quantity": holding_data["quantity"],
                "cost_basis": holding_data["cost_basis"],
                "created_at": "2025-10-01T12:00:00"
            }
            
            portfolio_holdings[str(new_holding_id)] = new_holding
            
            return json.dumps({
                "success": True,
                "action": "create",
                "holding_id": str(new_holding_id),
                "message": f"Portfolio holding {new_holding_id} created successfully for portfolio {portfolio_id} with fund {fund_id}",
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
                    "error": f"Portfolio holding record {holding_id} not found"
                })
            
            if not holding_data:
                return json.dumps({
                    "success": False,
                    "error": "holding_data is required for update action"
                })
            
            if "fund_manager_approval" not in holding_data:
                return json.dumps({
                    "success": False,
                    "error": "Fund Manager approval is required for holding update"
                })
            
            if not holding_data.get("fund_manager_approval"):
                return json.dumps({
                    "success": False,
                    "error": "Fund Manager approval must be True for holding update"
                })
            
            allowed_update_fields = ["quantity", "cost_basis", "fund_manager_approval"]
            invalid_fields = [field for field in holding_data.keys() if field not in allowed_update_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for holding update: {', '.join(invalid_fields)}. Cannot update portfolio_id or fund_id."
                })
            
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
            
            updated_holding = portfolio_holdings[holding_id].copy()
            for key, value in holding_data.items():
                if key != "fund_manager_approval":
                    updated_holding[key] = value
            
            portfolio_holdings[holding_id] = updated_holding
            
            return json.dumps({
                "success": True,
                "action": "update",
                "holding_id": str(holding_id),
                "message": f"Portfolio holding {holding_id} updated successfully",
                "holding_data": updated_holding
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manage_portfolio_holdings",
                "description": "Create or update portfolio holdings records in the fund management system. This tool manages the relationship between investor portfolios and funds, ensuring proper allocation tracking and compliance with investment policies. For creation, establishes new holding records with validation to maintain data integrity and prevents duplicate fund entries within the same portfolio. For updates, modifies existing holding records while preserving the portfolio-fund relationship. Operations require approval from Fund Manager as mandated by regulatory requirements. Validates positive quantity and cost basis values, enforces one-fund-per-portfolio constraint, and maintains audit trails. Essential for accurate portfolio valuation, investor reporting, and regulatory compliance. Supports the complete portfolio holding lifecycle from initial investment allocation to ongoing position management.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' to establish new portfolio holding record, 'update' to modify existing holding record",
                            "enum": ["create", "update"]
                        },
                        "holding_data": {
                            "type": "object",
                            "description": "Holding data object. For create: requires portfolio_id, fund_id, quantity (positive), cost_basis (positive), fund_manager_approval (True). For update: includes holding fields to change with fund_manager_approval. SYNTAX: {\"key\": \"value\"}",
                            "properties": {
                                "portfolio_id": {
                                    "type": "string",
                                    "description": "Unique identifier of the portfolio (required for create only, cannot be updated)"
                                },
                                "fund_id": {
                                    "type": "string",
                                    "description": "Unique identifier of the fund (required for create only, cannot be updated)"
                                },
                                "quantity": {
                                    "type": "number",
                                    "description": "Number of units/shares held (must be positive)"
                                },
                                "cost_basis": {
                                    "type": "number",
                                    "description": "Original acquisition cost per unit (must be positive)"
                                },
                                "fund_manager_approval": {
                                    "type": "boolean",
                                    "description": "Fund Manager approval presence (True/False) (required for both create and update operations)"
                                }
                            }
                        },
                        "holding_id": {
                            "type": "string",
                            "description": "Unique identifier of the holding record (required for update action only)"
                        }
                    },
                    "required": ["action"]
                }
            }
        }
