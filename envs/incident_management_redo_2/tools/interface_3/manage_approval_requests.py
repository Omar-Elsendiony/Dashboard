import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class ManageApprovalRequests(Tool):
    """
    Create and update approval requests for various items requiring approval.
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
        status: Optional[str] = None,
        approval_notes: Optional[str] = None
    ) -> str:
        """
        Create or update approval request records.

        Actions:
        - create: Create new approval request (requires reference_id, reference_type, requested_by, requested_action, approver)
        - update: Update existing approval request (requires approval_id and at least one field to update)
        """
        def generate_id(table: Dict[str, Any]) -> str:
            """Generates a new unique ID for a record."""
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        def generate_approval_number(approval_id: str) -> str:
            """Generate a formatted approval request number."""
            return f"APR{approval_id.zfill(8)}"

        timestamp = "2025-10-01T12:00:00"
        approvals = data.get("approval_requests", {})
        users = data.get("users", {})

        valid_reference_types = ["escalation", "bridge", "change", "rollback", "incident_closure", "rca"]
        valid_statuses = ["pending", "approved", "denied", "cancelled"]

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

            new_id = generate_id(approvals)
            approval_number = generate_approval_number(new_id)
            new_approval = {
                "approval_id": new_id,
                "approval_number": approval_number,
                "reference_id": reference_id,
                "reference_type": reference_type,
                "requested_by": requested_by,
                "requested_action": requested_action,
                "approver": approver,
                "status": "pending",
                "approval_notes": approval_notes.strip() if approval_notes else None,
                "requested_at": timestamp,
                "responded_at": None,
                "created_at": timestamp,
                "updated_at": timestamp,
                "last_modified_by": requested_by,
                "version": 1,
                "history": [{
                    "timestamp": timestamp,
                    "action": "created",
                    "user_id": requested_by,
                    "details": "Approval request created"
                }]
            }
            approvals[new_id] = new_approval

            return json.dumps({
                "success": True,
                "action": "create",
                "approval_id": new_id,
                "approval_number": approval_number,
                "approval_data": new_approval
            })

        if action == "update":
            if approval_id not in approvals:
                return json.dumps({
                    "success": False,
                    "error": f"Approval request with ID {approval_id} not found"
                })

            # Validate at least one field is being updated
            update_fields = [status, approval_notes]
            if all(v is None for v in update_fields):
                return json.dumps({
                    "success": False,
                    "error": "At least one field must be provided for update"
                })

            existing_approval = approvals[approval_id]

            history_entry = {
                "timestamp": timestamp,
                "action": "updated",
                "user_id": approver,
                "changes": []
            }

            if status is not None:
                if status not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                    })
                history_entry["changes"].append({"field": "status", "old": existing_approval["status"], "new": status})
                existing_approval["status"] = status
                if status in ["approved", "denied"]:
                    existing_approval["responded_at"] = timestamp

            if approval_notes is not None:
                history_entry["changes"].append({"field": "approval_notes", "old": existing_approval["approval_notes"], "new": approval_notes.strip()})
                existing_approval["approval_notes"] = approval_notes.strip()

            existing_approval["updated_at"] = timestamp
            existing_approval["last_modified_by"] = approver
            existing_approval["version"] += 1
            existing_approval["history"].append(history_entry)

            return json.dumps({
                "success": True,
                "action": "update",
                "approval_id": approval_id,
                "approval_number": existing_approval["approval_number"],
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
                "name": "manage_approval_requests",
                "description": "Create/update approval requests for various items requiring approval. Actions: 'create' (requires reference_id, reference_type, requested_by, requested_action, approver; optional: approval_notes), 'update' (requires approval_id; optional: status, approval_notes).",
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
                            "description": "Required for create. ID of the item needing approval"
                        },
                        "reference_type": {
                            "type": "string",
                            "description": "Type of item requiring approval: escalation, bridge, change, rollback, incident_closure, rca",
                            "enum": ["escalation", "bridge", "change", "rollback", "incident_closure", "rca"]
                        },
                        "requested_by": {
                            "type": "string",
                            "description": "Required for create. ID of the active user requesting approval"
                        },
                        "requested_action": {
                            "type": "string",
                            "description": "Required for create. Description of the action requiring approval"
                        },
                        "approver": {
                            "type": "string",
                            "description": "Required for create. ID of the active user who needs to approve"
                        },
                        "status": {
                            "type": "string",
                            "description": "Status of the approval request",
                            "enum": ["pending", "approved", "denied", "cancelled"]
                        },
                        "approval_notes": {
                            "type": "string",
                            "description": "Notes provided during approval/denial"
                        }
                    },
                    "required": ["action"]
                }
            }
        }