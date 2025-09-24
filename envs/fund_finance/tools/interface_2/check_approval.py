import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CheckApproval(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, requester_email: str) -> str:
        # Define role authorization mapping
        role_authorizations = {
            "compliance_officer": [
                "investor_onboarding", "investor_offboarding", "subscription_management", 
                "commitments_create", "commitments_fulfill", "redemption_processing"
            ],
            "fund_manager": [
                "fund_management_setup", "fund_management_maintenance", "trade_execution", 
                "portfolio_creation", "portfolio_update", "portfolio_holding_management", 
                "instrument_creation", "nav_record_updates", "instrument_price_updates",
                "reporting_performance", "reporting_financial", "subscription_management"
            ],
            "finance_officer": [
                "nav_valuation", "redemption_processing", 
                "portfolio_creation", "invoice_management", "payment_processing", 
                "nav_record_creation", "nav_record_updates", "reporting_holding"
            ],
            "trader": [
                "trade_execution"
            ],
            "system_administrator": [
                "user_account_management", "system_monitoring"
            ]
        }
        
        # Define actions requiring multiple approvers (AND logic)
        and_approval_actions = {
            "fund_management_setup": ["fund_manager", "compliance_officer"],
            "fund_management_maintenance": ["fund_manager", "compliance_officer"],
            "redemption_processing": ["compliance_officer", "finance_officer"],
            "instrument_creation": ["fund_manager", "compliance_officer"],
            "nav_record_updates": ["finance_officer", "fund_manager"],
            "instrument_price_updates": ["fund_manager", "compliance_officer"],
            "subscription_management": ["compliance_officer", "fund_manager"]
        }
        
        # Define actions allowing alternative approvers (OR logic)
        or_approval_actions = {
            "portfolio_creation": ["fund_manager", "finance_officer"]
        }
        
        users = data.get("users", {})
        for user in users.values():
            if user.get("email") == requester_email:
                role_conducting_action = user.get("role")
                requester_id = user.get("user_id")
                break
        else:
            return json.dumps({
                "approval_valid": False,
                "error": f"No user found with email: {requester_email}"
            })
        # Check if role is directly authorized for the action
        authorized_roles = role_authorizations.get(role_conducting_action, [])
        if action in authorized_roles:
            return json.dumps({
                "approval_valid": True, 
                # "authorized_by_role": True,
                "message": f"Role '{role_conducting_action}' is directly authorized for action '{action}'",
            })
        
        # If not directly authorized, calculate and check approval code
        # Generate calculated approval code: action + requester_id (hashed)
        # import hashlib
        # calculated_approval_code = hashlib.sha256(f"{action}_{requester_id}".encode()).hexdigest()
        calculated_approval_code = f"{action}_{requester_id}"
        
        approvals = data.get("approvals", {})
        
        # Check if calculated approval code exists
        approvals_found_for_code = []
        for approval in approvals.values():
            if approval.get("code") == calculated_approval_code:
                approvals_found_for_code.append(approval)
                # break
        # print(f"Approvals found for code '{calculated_approval_code}': {approvals_found_for_code}")
        if not approvals_found_for_code:
            return json.dumps({
                "approval_valid": False,
                "error": f"No approval found"
            })

        approvals_approved_by = [ approvals_found.get("approved_by") for approvals_found in approvals_found_for_code if "approved_by" in approvals_found ]
        # Check AND logic actions
        if action in and_approval_actions:
            required_roles = and_approval_actions[action]
            for approved_by in approvals_approved_by:
                if required_roles and approved_by in required_roles:
                    required_roles.remove(approved_by)
                    # return json.dumps({
                    #     "approval_valid": True,
                    #     "approved_by": approved_by,
                    #     "approval_type": "and_logic",
                    #     "note": f"Requires all roles: {', '.join(required_roles)}"
                    # })
            if not required_roles:
                return json.dumps({
                    "approval_valid": True,
                    "approved_by": approvals_approved_by,
                })
            else:
                return json.dumps({
                    "approval_valid": False,
                    "error": f"Requires additional approvals from roles: {', '.join(required_roles)}"
                })
        
        # Check OR logic actions
        elif action in or_approval_actions:
            allowed_roles = or_approval_actions[action]
            for approved_by in approvals_approved_by:
                if approved_by in allowed_roles:
                    return json.dumps({
                        "approval_valid": True,
                        "approved_by": approved_by,
                    })
        
        # Check single approver actions
        else:
            for role, actions in role_authorizations.items():
                approved_by = approvals_found_for_code[0].get("approved_by")
                if action in actions and approved_by == role:
                    # print("single approver match found")
                    return json.dumps({
                        "approval_valid": True,
                        "approved_by": approved_by,
                    })
        
        return json.dumps({
            "approval_valid": False,
            "error": f"No valid approval found"
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "check_approval",
                "description": "Validates role authorization and approval for fund management actions using requester email. Actions include: investor_onboarding (new investor registration), investor_offboarding (investor removal), fund_management_setup (new fund creation), fund_management_maintenance (fund updates), subscription_management (investor fund subscriptions), commitments_create (creating investor commitments), commitments_fulfill (fulfilling commitments), trade_execution (executing trades), nav_valuation (NAV calculations), redemption_processing (processing redemptions), portfolio_creation (creating investor portfolios), portfolio_update (updating portfolios), portfolio_holding_management (managing portfolio holdings), instrument_creation (creating new instruments), invoice_management (managing invoices), payment_processing (processing payments), nav_record_creation (creating NAV records), nav_record_updates (updating NAV records), instrument_price_updates (updating instrument prices), reporting_performance (performance reports), reporting_financial (financial reports), reporting_holding (holding reports), user_account_management (system user management), system_monitoring (system activity monitoring). Roles include: compliance_officer (handles regulatory compliance and investor verification), fund_manager (manages funds and approves investments), finance_officer (handles financial calculations and payments), trader (executes market trades), system_administrator (manages system users and monitoring). If the requester's role is directly authorized for the action, returns approval immediately. Otherwise, validates against existing approvals.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "The action being performed: investor_onboarding, investor_offboarding, fund_management_setup, fund_management_maintenance, subscription_management, commitments_create, commitments_fulfill, trade_execution, nav_valuation, redemption_processing, portfolio_creation, portfolio_update, portfolio_holding_management, instrument_creation, invoice_management, payment_processing, nav_record_creation, nav_record_updates, instrument_price_updates, reporting_performance, reporting_financial, reporting_holding, user_account_management, system_monitoring"
                        },
                        "requester_email": {
                            "type": "string",
                            "description": "Email of the user requesting the action"
                        }
                    },
                    "required": ["action", "requester_email"]
                }
            }
        }