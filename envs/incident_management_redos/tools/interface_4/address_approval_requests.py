import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class AddressApprovalRequests(Tool):
    """
    Create and update approval requests for escalations, bridges, changes, rollbacks, RCAs, and incident closures.
    """
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        action: str,
        approval_id: Optional[str] = None,
        reference_id: Optional[str] = None,
        reference_type: Optional[str] = None,
        requested_by: Optional[str] = None,
        requested_action: Optional[str] = None,
        approver: Optional[str] = None,
        status: Optional[str] = None
    ) -> str:
        """
        Create or update approval request records.

        Actions:
        - create: Create new approval request (requires reference_id, reference_type, requested_by, requested_action, approver)
        - update: Update existing approval request (requires approval_id; optional: status)
        """
        def generate_id(table: Dict[str, Any]) -> str:
            """Generates a new unique ID for a record."""
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        timestamp = "2025-10-07T12:00:00"
        approvals = data.get("approval_requests", {})
        users = data.get("users", {})

        valid_reference_types = ["escalation", "bridge", "change", "rollback", "rca", "incident_closure"]
        valid_requested_actions = [
            "create_escalation", "initiate_bridge", "create_change_request",
            "create_rollback_request", "conduct_rca", "close_incident"
        ]
        valid_statuses = ["pending", "approved", "denied"]

        if action not in ["create", "update"]:
            return json.dumps({
                "success": False,
                "error": "Invalid action. Must be 'create' or 'update'"
            })

        if action == "update" and not approval_id:
            return json.dumps({
                "success": False,
                "error": "approval_id is required for update action"
            })

        if action == "create":
            if not all([reference_id, reference_type, requested_by, requested_action, approver]):
                return json.dumps({
                    "success": False,
                    "error": "reference_id, reference_type, requested_by, requested_action, and approver are required for create action"
                })

            # Validate users exist and are active
            for user_id in [requested_by, approver]:
                if user_id not in users:
                    return json.dumps({
                        "success": False,
                        "error": f"User with ID {user_id} not found"
                    })
                if users[user_id]["status"] != "active":
                    return json.dumps({
                        "success": False,
                        "error": f"User with ID {user_id} is not active"
                    })

            if reference_type not in valid_reference_types:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid reference_type. Must be one of: {', '.join(valid_reference_types)}"
                })

            # Validate requested_action
            if requested_action not in valid_requested_actions:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid requested_action. Must be one of: {', '.join(valid_requested_actions)}"
                })

            new_id = generate_id(approvals)
            new_approval = {
                "approval_id": new_id,
                "reference_id": reference_id,
                "reference_type": reference_type,
                "requested_by": requested_by,
                "requested_action": requested_action,
                "approver": approver,
                "status": "pending",
                "requested_at": timestamp,
                "responded_at": None
            }
            approvals[new_id] = new_approval

            return json.dumps({
                "success": True,
                "action": "create",
                "approval_id": new_id,
                "approval_data": new_approval
            })

        if action == "update":
            if approval_id not in approvals:
                return json.dumps({
                    "success": False,
                    "error": f"Approval request with ID {approval_id} not found"
                })

            # Validate at least one field is being updated
            if status is None:
                return json.dumps({
                    "success": False,
                    "error": "status must be provided for update"
                })

            existing_approval = approvals[approval_id]

            if status is not None:
                if status not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                    })
                existing_approval["status"] = status
                if status in ["approved", "denied"]:
                    existing_approval["responded_at"] = timestamp

            return json.dumps({
                "success": True,
                "action": "update",
                "approval_id": approval_id,
                "approval_data": existing_approval
            })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        """
        Returns comprehensive information about the tool's capabilities, parameters, and data schema.
        """
        return {
            "type": "function",
            "function": {
                "name": "address_approval_requests",
                "description": "Create/update approval requests for various items requiring approval. Supports escalations, bridges, changes, rollbacks, RCAs, and incident closures. Actions: 'create' (requires reference_id, reference_type, requested_by, requested_action, approver), 'update' (requires approval_id; optional: status).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' or 'update'",
                            "enum": ["create", "update"]
                        },
                        "approval_id": {
                            "type": "string",
                            "description": "Required for update. ID of the approval request to update"
                        },
                        "reference_id": {
                            "type": "string",
                            "description": "Required for create. ID of the item needing approval (e.g., escalation_id, bridge_id, change_id)"
                        },
                        "reference_type": {
                            "type": "string",
                            "description": "Required for create. Type of item requiring approval",
                            "enum": ["escalation", "bridge", "change", "rollback", "rca", "incident_closure"]
                        },
                        "requested_by": {
                            "type": "string",
                            "description": "Required for create. ID of the active user requesting approval"
                        },
                        "requested_action": {
                            "type": "string",
                            "description": "Required for create. Specific action being requested",
                            "enum": ["create_escalation", "initiate_bridge", "create_change_request", "create_rollback_request", "conduct_rca", "close_incident"]
                        },
                        "approver": {
                            "type": "string",
                            "description": "Required for create. ID of the active user who needs to approve"
                        },
                        "status": {
                            "type": "string",
                            "description": "For update only. New status of the approval request",
                            "enum": ["pending", "approved", "denied"]
                        }
                    },
                    "required": ["action"]
                }
            }
        }