import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class CheckAuthorization(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, requester_email: str) -> str:
        """
        Check authorization for Incident Management actions.
        Uses two-tier logic with fallback:
        1. If requester has an authorized role → authorized
        2. If requester lacks an authorized role but has an 'approved' approval record from someone with an authorized role → authorized
        3. Otherwise → not authorized
        
        Args:
            data: Environment data containing users and approvals
            action: The incident management action being performed
            requester_email: Email of the user requesting the action
            
        Returns:
            JSON string with authorization result
        """
        # Single source of truth for all actions and their authorized roles
        ACTIONS = {
            "create_client": ["system_administrator", "incident_manager", "account_manager"],
            "update_client": ["system_administrator", "incident_manager", "account_manager"],
            "create_user": ["system_administrator", "incident_manager"],
            "update_user": ["system_administrator", "incident_manager"],
            "deactivate_user": ["system_administrator", "incident_manager"],
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
            "close_incident": ["incident_manager", "technical_support"],
            "create_communication": ["incident_manager", "technical_support", "system_administrator", "account_manager"],
            "update_communication": ["incident_manager", "technical_support", "system_administrator", "account_manager"],
            "create_workaround": ["technical_support", "incident_manager", "system_administrator", "executive"],
            "update_workaround": ["technical_support", "incident_manager", "system_administrator", "executive"],
            "conduct_rca": ["technical_support", "incident_manager"],
            "update_rca": ["technical_support", "incident_manager", "system_administrator", "executive"],
            "create_escalation": ["incident_manager", "technical_support", "system_administrator", "executive", "account_manager"],
            "update_escalation": ["incident_manager", "technical_support", "system_administrator", "executive"],
            "create_change_request": ["technical_support", "incident_manager", "system_administrator", "executive"],
            "update_change_request": ["technical_support", "incident_manager", "system_administrator", "executive"],
            "create_rollback_request": ["technical_support", "system_administrator", "incident_manager"],
            "update_rollback_request": ["incident_manager", "system_administrator", "executive"],
            "record_metrics": ["incident_manager", "system_administrator"],
            "update_metrics": ["incident_manager", "system_administrator"],
            "generate_report": ["incident_manager", "executive"],
            "update_report": ["incident_manager", "executive"],
            "create_kb_article": ["technical_support", "incident_manager"],
            "update_kb_article": ["technical_support", "incident_manager"],
            "create_pir": ["incident_manager", "executive"],
            "update_pir": ["incident_manager", "executive"],
            "initiate_bridge": ["incident_manager", "technical_support", "executive"],
            "close_bridge": ["incident_manager", "technical_support"],
            "request_approval": ["technical_support", "system_administrator", "incident_manager"],
            "approve_request": ["incident_manager", "executive"],
            "update_communication_status": ["incident_manager", "technical_support", "system_administrator"],
            "create_work_note": ["incident_manager", "technical_support", "system_administrator"],
            "update_work_note": ["incident_manager", "technical_support", "system_administrator"],
            "create_attachment": ["incident_manager", "technical_support", "system_administrator", "client_contact"],
            "update_escalation_status": ["incident_manager", "executive", "technical_support"],
            "update_approval_request": ["incident_manager", "system_administrator"]
        }
        
        # Actions that may require approval under certain conditions
        APPROVAL_REQUIRED_ACTIONS = [
            "create_escalation",
            "initiate_bridge",
            "create_rollback_request",
            "create_change_request",
            "close_incident",
            "conduct_rca"
        ]
        
        # Find the requester's role and user_id
        users = data.get("users", {})
        requester_role = None
        requester_user_id = None
        for user_id, user in users.items():
            if user.get("email") == requester_email:
                requester_role = user.get("role")
                requester_user_id = user_id
                break
        
        if not requester_role:
            return json.dumps({
                "authorized": False,
                "error": f"No user found with email: {requester_email}"
            })
        
        # Check if the action is defined
        if action not in ACTIONS:
            return json.dumps({
                "authorized": False,
                "error": f"Unknown action: {action}"
            })
        
        authorized_roles = ACTIONS[action]
        
        # TIER 1: Check if requester has direct authorization
        if requester_role in authorized_roles:
            return json.dumps({
                "authorized": True,
                "message": f"User with role '{requester_role}' is directly authorized to perform action '{action}'"
            })
        
        # TIER 2: Requester not directly authorized, check for an explicit approval
        # This only applies to actions that support the approval workflow
        if action in APPROVAL_REQUIRED_ACTIONS:
            approvals = data.get("approvals", {})
            
            for approval in approvals.values():
                # Check for a matching, approved record for the specific requester and action
                approval_requested_by = approval.get("requested_by")
                
                # Match by user_id
                if str(approval_requested_by) != str(requester_user_id):
                    continue
                    
                # Check if this approval is for the action being requested
                # Map action names to approval request patterns
                approval_action_match = False
                requested_action = approval.get("requested_action", "")
                
                if action == "create_escalation" and "Escalation approval" in requested_action:
                    approval_action_match = True
                elif action == "initiate_bridge" and "Bridge initiation approval" in requested_action:
                    approval_action_match = True
                elif action == "create_rollback_request" and "Rollback approval" in requested_action:
                    approval_action_match = True
                elif action == "create_change_request" and "change approval" in requested_action.lower():
                    approval_action_match = True
                elif action == "close_incident" and "Incident Closure approval" in requested_action:
                    approval_action_match = True
                elif action == "conduct_rca" and "Rca approval" in requested_action:
                    approval_action_match = True
                
                if approval_action_match and approval.get("status") == "approved":
                    # Get the approver's role
                    approver_user_id = approval.get("approver")
                    approver_role = None
                    
                    for user_id, user in users.items():
                        if str(user_id) == str(approver_user_id):
                            approver_role = user.get("role")
                            break
                    
                    # Check if the approver has an authorized role
                    if approver_role and approver_role in authorized_roles:
                        return json.dumps({
                            "authorized": True,
                            "message": f"User '{requester_email}' has a valid approval from user with role '{approver_role}' for action '{action}'"
                        })
        
        # No direct authorization or valid approval found
        return json.dumps({
            "authorized": False,
            "error": f"Role '{requester_role}' is not authorized for action '{action}', and no valid approval was found. Authorized roles: {', '.join(authorized_roles)}."
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        """Return the function schema for tool registration."""
        return {
            "type": "function",
            "function": {
                "name": "check_authorization",
                "description": "Validates authorization for Incident Management actions. First checks if the requester's role is directly authorized. If not, checks for an approved approval record from a user who has an authorized role.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "The incident management action being performed. Valid actions: create_client, update_client, create_user, update_user, deactivate_user, create_vendor, update_vendor, create_product, update_product, create_component, update_component, create_subscription, update_subscription, create_sla, update_sla, create_incident, update_incident, resolve_incident, close_incident, create_communication, update_communication, create_workaround, update_workaround, conduct_rca, update_rca, create_escalation, update_escalation, create_change_request, update_change_request, create_rollback_request, update_rollback_request, record_metrics, update_metrics, generate_report, update_report, create_kb_article, update_kb_article, create_pir, update_pir, initiate_bridge, close_bridge, request_approval, approve_request, update_communication_status, create_work_note, update_work_note, create_attachment, update_escalation_status, update_approval_request"
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