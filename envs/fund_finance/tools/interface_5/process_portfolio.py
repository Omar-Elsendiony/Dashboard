import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ProcessPortfolio(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, portfolio_data: Dict[str, Any] = None, portfolio_id: str = None) -> str:
        """
        Create or update portfolio records.
        
        Actions:
        - create: Create new portfolio (requires portfolio_data with investor_id, fund_manager_approval OR finance_officer_approval, optional status)
        - update: Update existing portfolio (requires portfolio_id and portfolio_data with changes like status, fund_manager_approval)
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
        
        # Access portfolios data
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for portfolios"
            })
        
        portfolios = data.get("portfolios", {})
        portfolio_holdings = data.get("portfolio_holdings", {})
        
        if action == "create":
            if not portfolio_data:
                return json.dumps({
                    "success": False,
                    "error": "portfolio_data is required for create action"
                })
            
            # Validate required fields for creation
            required_fields = ["investor_id"]
            missing_fields = [field for field in required_fields if field not in portfolio_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields for portfolio creation: {', '.join(missing_fields)}"
                })
            
            # Validate approval - Fund Manager OR Finance Officer approval required
            has_fund_manager_approval = portfolio_data.get("fund_manager_approval", False)
            has_finance_officer_approval = portfolio_data.get("finance_officer_approval", False)
            
            if not (has_fund_manager_approval or has_finance_officer_approval):
                return json.dumps({
                    "success": False,
                    "error": "Either Fund Manager approval or Finance Officer approval is required for portfolio creation"
                })
            
            # Validate only allowed fields are present
            allowed_fields = ["investor_id", "status", "fund_manager_approval", "finance_officer_approval"]
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
            
            # Check if investor already has an active portfolio (policy constraint)
            investor_id = portfolio_data["investor_id"]
            for existing_portfolio in portfolios.values():
                if (existing_portfolio.get("investor_id") == investor_id and 
                    existing_portfolio.get("status") == "active"):
                    return json.dumps({
                        "success": False,
                        "error": f"Investor {investor_id} already has an active portfolio. One investor is only allowed to have one portfolio."
                    })
            
            # Generate new portfolio ID using consistent pattern
            new_portfolio_id = generate_id(portfolios)
            
            # Create new portfolio record
            new_portfolio = {
                "portfolio_id": str(new_portfolio_id) if new_portfolio_id else None ,
                "investor_id": str(portfolio_data["investor_id"]) if portfolio_data["investor_id"] else None,
                "status": portfolio_data.get("status", "active"),
                "created_at": "2025-10-01T12:00:00",
                "updated_at": "2025-10-01T12:00:00"
            }
            
            portfolios[str(new_portfolio_id)] = new_portfolio
            
            return json.dumps({
                "success": True,
                "action": "create",
                "portfolio_id": str(new_portfolio_id) if new_portfolio_id else None ,
                "message": f"Portfolio {new_portfolio_id} created successfully for investor {investor_id}",
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
                    "error": f"Portfolio record {portfolio_id} not found"
                })
            
            if not portfolio_data:
                return json.dumps({
                    "success": False,
                    "error": "portfolio_data is required for update action"
                })
            
            # Validate required approvals for updates - Fund Manager approval required
            if not portfolio_data.get("fund_manager_approval", False):
                return json.dumps({
                    "success": False,
                    "error": "Fund Manager approval is required for portfolio update"
                })
            
            # Validate only allowed fields are present for updates
            allowed_update_fields = ["status", "fund_manager_approval"]
            invalid_fields = [field for field in portfolio_data.keys() if field not in allowed_update_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for portfolio update: {', '.join(invalid_fields)}. Cannot update investor_id."
                })
            
            # Validate status enum if provided
            if "status" in portfolio_data:
                valid_statuses = ["active", "inactive", "archived"]
                if portfolio_data["status"] not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                    })
                
                # Check if closing a portfolio with active holdings (policy constraint)
                current_portfolio = portfolios[portfolio_id]
                if (current_portfolio.get("status") == "active" and 
                    portfolio_data["status"] in ["inactive", "archived"]):
                    
                    # Check for active holdings in this portfolio
                    has_active_holdings = any(
                        holding.get("portfolio_id") == portfolio_id 
                        for holding in portfolio_holdings.values()
                    )
                    
                    if has_active_holdings:
                        return json.dumps({
                            "success": False,
                            "error": f"Cannot close portfolio {portfolio_id} because it has active holdings. Please remove all holdings before closing the portfolio."
                        })
            
            # Update portfolio record
            updated_portfolio = portfolios[portfolio_id].copy()
            for key, value in portfolio_data.items():
                if key not in ["fund_manager_approval"]:
                    updated_portfolio[key] = value
            
            updated_portfolio["updated_at"] = "2025-10-01T12:00:00"
            portfolios[portfolio_id] = updated_portfolio
            
            return json.dumps({
                "success": True,
                "action": "update",
                "portfolio_id": str(portfolio_id),
                "message": f"Portfolio {portfolio_id} updated successfully",
                "portfolio_data": updated_portfolio
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "process_portfolio",
                "description": "Create or update portfolio records in the fund management system. This tool manages investor portfolio lifecycle, ensuring compliance with investment policies and regulatory requirements. For creation, establishes new portfolio records with validation to enforce the one-investor-one-portfolio constraint and requires either Fund Manager or Finance Officer approval. For updates, modifies existing portfolio records while preventing closure when active holdings exist and requires Fund Manager approval. Validates portfolio status transitions and maintains audit trails. Essential for proper investor account management, portfolio tracking, and regulatory compliance. Supports the complete portfolio lifecycle from initial creation through status changes to archival.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' to establish new portfolio record, 'update' to modify existing portfolio record",
                            "enum": ["create", "update"]
                        },
                        "portfolio_data": {
                            "type": "object",
                            "description": "Portfolio data object. For create: requires investor_id, status (optional, defaults to 'active'), and either fund_manager_approval OR finance_officer_approval. For update: includes status changes with fund_manager_approval (investor_id cannot be updated). SYNTAX: {\"key\": \"value\"}",
                            "properties": {
                                "investor_id": {
                                    "type": "string",
                                    "description": "Unique identifier of the investor (required for create only, cannot be updated)"
                                },
                                "status": {
                                    "type": "string",
                                    "description": "Portfolio status: 'active', 'inactive', or 'archived' (optional for create, defaults to 'active')",
                                    "enum": ["active", "inactive", "archived"]
                                },
                                "fund_manager_approval": {
                                    "type": "boolean",
                                    "description": "Fund Manager approval presence (True/False) (for create: either this OR finance_officer_approval required; for update: this is required)"
                                },
                                "finance_officer_approval": {
                                    "type": "boolean",
                                    "description": "Finance Officer approval presence (True/False) (for create only: either this OR fund_manager_approval required)"
                                }
                            }
                        },
                        "portfolio_id": {
                            "type": "string",
                            "description": "Unique identifier of the portfolio record (required for update action only)"
                        }
                    },
                    "required": ["action"]
                }
            }
        }