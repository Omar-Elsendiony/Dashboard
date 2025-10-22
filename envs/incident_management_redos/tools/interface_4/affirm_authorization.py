import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class AffirmAuthorization(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, requester_email: str) -> str:
        """
        Check authorization for Incident Management actions based on SOPs.
        
        Uses two-tier logic:
        1. Direct authorization: If requester has an authorized role → authorized
        2. Approval-based authorization: If requester lacks direct role but has an 
        'approved' approval record from someone with an authorized role → authorized
        3. Otherwise → not authorized
        
        Args:
            data: Environment data containing users and approval_requests
            action: The incident management action being performed
            requester_email: Email of the user requesting the action
            
        Returns:
            JSON string with authorization result
        """
        
        # Validate inputs
        if not isinstance(data, dict):
            return json.dumps({
                "authorized": False,
                "error": "Invalid data format: expected dictionary"
            })
        
        if not isinstance(action, str) or not action.strip():
            return json.dumps({
                "authorized": False,
                "error": "Invalid action: expected non-empty string"
            })
        
        if not isinstance(requester_email, str) or not requester_email.strip():
            return json.dumps({
                "authorized": False,
                "error": "Invalid requester_email: expected non-empty string"
            })
        
        # Validate required tables exist
        if "users" not in data:
            return json.dumps({
                "authorized": False,
                "error": "Missing required 'users' data table"
            })
        
        # Single source of truth for all actions and their authorized roles
        # Based on policy SOPs "Who can perform" sections
        ACTIONS = {
            # Client Management (SOP 1.1-1.3)
            "create_client": ["account_manager", "system_administrator", "technical_support"],  # SOP 1.1
            "update_client": ["account_manager", "system_administrator"],  # SOP 1.2
            "create_sla_agreement": ["account_manager", "executive"],  # SOP 1.3
            "update_sla_agreement": ["account_manager", "executive"],  # SOP 1.3 (implied)
            
            # User Management (SOP 2.1-2.2)
            "create_user": ["system_administrator", "incident_manager"],  # SOP 2.1
            "update_user": ["system_administrator", "incident_manager"],  # SOP 2.2
            
            # Infrastructure/CI Management (SOP 3.1-3.2)
            "create_configuration_item": ["technical_support", "system_administrator"],  # SOP 3.1
            "update_configuration_item": ["technical_support", "system_administrator"],  # SOP 3.1 (implied)
            "create_ci_client_assignment": ["system_administrator", "technical_support"],  # SOP 3.2
            
            # Incident Operations (SOP 4.1-4.13)
            "create_incident": ["incident_manager", "technical_support", "executive", "system_administrator"],  # SOP 4.1
            "update_incident": ["incident_manager", "technical_support", "system_administrator", "executive"],  # SOP 4.2
            "resolve_incident": ["incident_manager", "technical_support", "executive"],  # SOP 4.4
            "close_incident": ["incident_manager", "technical_support"],  # SOP 4.4
            "create_escalation": ["incident_manager", "technical_support", "account_manager", "system_administrator", "executive"],  # SOP 4.3
            "update_escalation": ["incident_manager", "technical_support", "system_administrator", "executive"],  # Derived from 4.3 + 6.6
            "initiate_bridge": ["incident_manager", "technical_support", "executive"],  # SOP 4.5
            "close_bridge": ["incident_manager", "technical_support"],  # SOP 4.6
            "request_approval": ["technical_support", "system_administrator", "incident_manager"],  # SOP 4.7
            "approve_request": ["incident_manager", "executive"],  # SOP 4.8
            "create_problem_ticket": ["technical_support", "system_administrator", "incident_manager"],  # SOP 4.9
            "update_problem_ticket": ["technical_support", "system_administrator", "incident_manager"],  # SOP 4.10
            "link_incident_to_problem": ["technical_support", "system_administrator", "incident_manager"],  # SOP 4.11
            "create_problem_ci_assignment": ["technical_support", "system_administrator", "incident_manager"],  # SOP 4.12
            "create_incident_ci_assignment": ["incident_manager", "technical_support", "system_administrator"],  # SOP 4.13
            
            # Communication Management (SOP 5.1)
            "create_communication": ["incident_manager", "technical_support"],  # SOP 5.1
            "update_communication": ["incident_manager", "technical_support"],  # SOP 5.1 (implied)
            "update_communication_status": ["incident_manager", "technical_support", "system_administrator"],  # SOP 6.7
            
            # Change Management (SOP 6.1-6.6)
            "create_change_request": ["technical_support", "system_administrator", "executive", "incident_manager"],  # SOP 6.1
            "update_change_request": ["technical_support", "system_administrator", "executive", "incident_manager"],  # SOP 6.1 (implied)
            "create_rollback_request": ["technical_support", "system_administrator", "incident_manager"],  # SOP 6.2
            "update_rollback_request": ["technical_support", "system_administrator", "incident_manager"],  # SOP 6.2 (implied)
            "create_work_note": ["incident_manager", "technical_support", "system_administrator"],  # SOP 6.3
            "update_work_note": ["incident_manager", "technical_support", "system_administrator"],  # SOP 6.4
            "create_attachment": ["incident_manager", "technical_support", "system_administrator", "client_contact"],  # SOP 6.5
            "update_escalation_status": ["incident_manager", "executive", "technical_support"],  # SOP 6.6
            
            # Reporting and Analysis (SOP 7.1-7.2)
            "conduct_root_cause_analysis": ["technical_support", "incident_manager", "system_administrator"],  # SOP 6.8
            "update_root_cause_analysis": ["incident_manager", "technical_support", "system_administrator"],  # SOP 6.9
            "create_incident_report": ["incident_manager", "executive"],  # SOP 7.1
            "update_incident_report": ["incident_manager", "executive"],  # SOP 7.1 (implied)
            "generate_incident_report": ["incident_manager", "executive"],  # SOP 7.1 (alias)
            "create_post_incident_review": ["incident_manager", "executive"],  # SOP 7.2
            "update_post_incident_review": ["incident_manager", "executive"],  # SOP 7.2 (implied)
            
            # Approval workflow actions
            "update_approval_request": ["incident_manager", "executive"],  # SOP 4.8
        }
        
        # Actions that support approval workflow (per DB schema approval_requests.requested_action enum)
        APPROVAL_SUPPORTED_ACTIONS = {
            "create_escalation": "create_escalation",
            "initiate_bridge": "initiate_bridge", 
            "create_change_request": "create_change_request",
            "create_rollback_request": "create_rollback_request",
            "conduct_root_cause_analysis": "conduct_rca",
            "close_incident": "close_incident"
        }
        
        users = data.get("users", {})
        
        # Build efficient lookup maps
        email_to_user = {}
        user_id_to_user = {}
        
        for user_id, user in users.items():
            user_email = user.get("email", "").strip().lower()
            if user_email:
                email_to_user[user_email] = (user_id, user)
                user_id_to_user[user_id] = user
        
        # Find the requester
        requester_lookup = email_to_user.get(requester_email.strip().lower())
        
        if not requester_lookup:
            return json.dumps({
                "authorized": False,
                "error": f"No user found with email: {requester_email}"
            })
        
        requester_user_id, requester_user = requester_lookup
        requester_role = requester_user.get("role")
        requester_status = requester_user.get("status")
        
        if not requester_role:
            return json.dumps({
                "authorized": False,
                "error": f"User '{requester_email}' has no role assigned"
            })
        
        # Check if user is active
        if requester_status != "active":
            return json.dumps({
                "authorized": False,
                "error": f"User '{requester_email}' is inactive"
            })
        
        # Check if the action is defined
        if action not in ACTIONS:
            return json.dumps({
                "authorized": False,
                "error": f"Unknown action: '{action}'"
            })
        
        authorized_roles = ACTIONS[action]
        
        # TIER 1: Check if requester has direct authorization
        if requester_role in authorized_roles:
            return json.dumps({
                "authorized": True,
                "message": f"User with role '{requester_role}' is directly authorized to perform action '{action}'"
            })
        
        # TIER 2: Check for approval-based authorization
        # Only applies to actions that support approval workflow
        if action in APPROVAL_SUPPORTED_ACTIONS:
            approval_requests = data.get("approval_requests", {})
            
            for approval_id, approval in approval_requests.items():
                # Must be for this specific requester
                approval_requested_by = str(approval.get("requested_by", ""))
                if approval_requested_by != str(requester_user_id):
                    continue
                
                # Must be approved status (per DB enum: pending, approved, denied)
                approval_status = approval.get("status")
                if approval_status != "approved":
                    continue
                
                # Match action by requested_action enum field (per DB schema)
                requested_action = approval.get("requested_action", "")
                expected_requested_action = APPROVAL_SUPPORTED_ACTIONS.get(action)
                
                if requested_action != expected_requested_action:
                    continue
                
                # Validate approver has an authorized role
                approver_user_id = str(approval.get("approver", ""))
                approver_user = user_id_to_user.get(approver_user_id)
                
                if not approver_user:
                    continue
                
                approver_role = approver_user.get("role")
                
                # Check if approver has authorization for this action
                if approver_role and approver_role in authorized_roles:
                    return json.dumps({
                        "authorized": True,
                        "message": f"User '{requester_email}' has valid approval for action '{action}'"
                    })
        
        # No direct authorization or valid approval found
        return json.dumps({
            "authorized": False,
            "error": f"Role '{requester_role}' is not authorized for action '{action}'"
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        """Return the function schema for tool registration."""
        return {
            "type": "function",
            "function": {
                "name": "affirm_authorization",
    "description": "Validates authorization for Incident Management actions based on policy SOPs. Uses two-tier authorization: (1) Direct authorization if requester's role is authorized for the action, or (2) Approval-based authorization if requester has a valid approved approval request from an authorized user. Approval workflow is supported for: create_escalation, initiate_bridge, create_change_request, create_rollback_request, conduct_root_cause_analysis, close_incident.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "The incident management action being performed. Valid actions include: create_client, update_client, create_sla_agreement, update_sla_agreement, create_user, update_user, create_configuration_item, update_configuration_item, create_ci_client_assignment, create_incident, update_incident, resolve_incident, close_incident, create_escalation, update_escalation, initiate_bridge, close_bridge, request_approval, approve_request, create_problem_ticket, update_problem_ticket, link_incident_to_problem, create_problem_ci_assignment, create_incident_ci_assignment, create_communication, update_communication, update_communication_status, create_change_request, update_change_request, create_rollback_request, update_rollback_request, create_work_note, update_work_note, create_attachment, update_escalation_status, conduct_root_cause_analysis, update_root_cause_analysis, create_incident_report, update_incident_report, generate_incident_report, create_post_incident_review, update_post_incident_review, update_approval_request"
                        },
                        "requester_email": {
                            "type": "string",
                            "description": "Email address of the user requesting authorization for the action"
                        }
                    },
                    "required": ["action", "requester_email"]
                }
            }
        }