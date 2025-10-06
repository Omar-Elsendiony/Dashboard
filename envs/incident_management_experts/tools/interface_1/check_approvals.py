import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CheckApproval(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, requester_email: str) -> str:
        """
        Check approval for Incident Management actions.
        Uses OR logic with fallback:
        1. If requester has ANY authorized role → approved
        2. If requester lacks an authorized role but has an 'approved' record from someone with an authorized role → approved
        3. Otherwise → denied
        
        Args:
            data: Environment data containing users and approvals
            action: The incident management action being performed
            requester_email: Email of the user requesting the action  
        """
        # Single source of truth for all actions and their authorized roles
        ACTIONS = {
            "create_client": ["system_administrator", "incident_manager", "account_manager"],
            "update_client": ["system_administrator", "incident_manager", "account_manager"],
            "create_user": ["system_administrator", "incident_manager"],
            "update_user": ["system_administrator", "incident_manager"],
            "create_vendor": ["system_administrator", "incident_manager", "executive"],
            "update_vendor": ["system_administrator", "incident_manager", "executive"],
            "create_product": ["system_administrator", "incident_manager", "executive"],
            "update_product": ["system_administrator", "incident_manager", "executive"],
            "create_component": ["system_administrator", "technical_support", "incident_manager"],
            "update_component": ["system_administrator", "technical_support", "incident_manager"],
            "create_subscription": ["account_manager", "incident_manager", "executive"],
            "update_subscription": ["account_manager", "incident_manager", "executive"],
            "create_sla": ["account_manager", "system_administrator", "executive"],
            "update_sla": ["account_manager", "system_administrator", "executive"],
            "create_incident": ["incident_manager", "technical_support", "system_administrator", "executive"],
            "update_incident": ["incident_manager", "technical_support", "system_administrator", "executive"],
            "resolve_incident": ["incident_manager", "technical_support", "executive"],
            "close_incident": ["incident_manager", "executive"],
            "create_communication": ["incident_manager", "technical_support", "system_administrator", "account_manager"],
            "update_communication": ["incident_manager", "technical_support", "system_administrator", "account_manager"],
            "create_workaround": ["technical_support", "incident_manager", "system_administrator", "executive"],
            "update_workaround": ["technical_support", "incident_manager", "system_administrator", "executive"],
            "conduct_rca": ["technical_support", "incident_manager", "system_administrator", "executive"],
            "update_rca": ["technical_support", "incident_manager", "system_administrator", "executive"],
            "create_escalation": ["incident_manager", "technical_support", "system_administrator", "executive"],
            "update_escalation": ["incident_manager", "technical_support", "system_administrator", "executive"],
            "create_change_request": ["technical_support", "incident_manager", "system_administrator", "executive"],
            "update_change_request": ["technical_support", "incident_manager", "system_administrator", "executive"],
            "create_rollback_request": ["system_administrator", "executive"],
            "update_rollback_request": ["incident_manager", "system_administrator", "executive"],
            "record_metrics": ["incident_manager", "system_administrator"],
            "update_metrics": ["incident_manager", "system_administrator"],
            "generate_report": ["incident_manager", "executive"],
            "update_report": ["incident_manager", "executive"],
            "create_kb_article": ["technical_support", "incident_manager"],
            "update_kb_article": ["technical_support", "incident_manager"],
            "create_pir": ["incident_manager", "executive"],
            "update_pir": ["incident_manager", "executive"]
        }
        
        # Find the requester's role
        users = data.get("users", {})
        requester_role = None
        for user in users.values():
            if user.get("email") == requester_email:
                requester_role = user.get("role")
                break
        
        if not requester_role:
            return json.dumps({
                "approval_valid": False,
                # "error": f"No user found with email: {requester_email}"
            })
        
        # Check if the action is defined
        if action not in ACTIONS:
            return json.dumps({
                "approval_valid": False,
                # "error": f"Unknown action: {action}"
            })
        
        authorized_roles = ACTIONS[action]
        
        # TIER 1: Check if requester has direct authorization
        if requester_role in authorized_roles:
            return json.dumps({
                "approval_valid": True,
                # "message": f"User with role '{requester_role}' is directly authorized to perform action '{action}'"
            })
        
        # TIER 2: Requester not directly authorized, check for an explicit approval
        approvals = data.get("approvals", {})
        print(approvals.keys())
        for approval in approvals.values():
            print(action)
            print(approval.get("action_name"))
            # Check for a matching, approved record for the specific requester and action
            if (approval.get("requester_email") == requester_email and
                approval.get("action_name") == action and
                approval.get("status") == "approved"):
                
                # Check if the approver has an authorized role
                approver_role = approval.get("approver_role")
                if approver_role and approver_role in authorized_roles:
                    return json.dumps({
                        "approval_valid": True,
                        "message": f"User '{requester_email}' has a valid approval from '{approver_role}' (authorized role) for action '{action}'"
                    })

        # No direct authorization or valid approval found
        return json.dumps({
            "approval_valid": False,
            # "error": f"Role '{requester_role}' is not authorized for action '{action}', and no valid approval was found. Authorized roles: {', '.join(authorized_roles)}."
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "check_approval",
                "description": "Validates authorization for Incident Management actions. First, it checks if the requester's role is directly authorized. If not, it checks for a specific, 'approved' record from a user who has an authorized role.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "The incident management action being performed"
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