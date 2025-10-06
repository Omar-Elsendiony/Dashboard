import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class HandleRollbackRequests(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, rollback_data: Dict[str, Any], rollback_id: str = None) -> str:
        """
        Create or update rollback request records.

        rollback_data must include:
        - action (required): 'create' or 'update'
        For create:
            - change_id (required)
            - requested_by_id (required)
            - Optional: incident_id, approved_by_id, executed_at, validation_completed, status
        For update:
            - rollback_id (required)
            - Optional: approved_by_id, executed_at, validation_completed, status
        """

        def generate_id(table:  Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        def generate_code(prefix: str, table: Dict[str, Any]) -> str:
            max_num = 0
            for record in table.values():
                code = record.get("rollback_code", "")
                if code.startswith(prefix):
                    try:
                        num = int(code.split("-")[-1])
                        max_num = max(max_num, num)
                    except:
                        pass
            return f"{prefix}-{str(max_num + 1).zfill(5)}"

        rollback_requests = data.get("rollback_requests", {})
        change_requests = data.get("change_requests", {})
        incidents = data.get("incidents", {})
        users = data.get("users", {})

        change_id = rollback_data.get("change_id")
        requested_by_id = rollback_data.get("requested_by_id")
        incident_id = rollback_data.get("incident_id")
        approved_by_id = rollback_data.get("approved_by_id")
        executed_at = rollback_data.get("executed_at")
        validation_completed = rollback_data.get("validation_completed")
        status = rollback_data.get("status")

        valid_statuses = ["requested", "approved", "in_progress", "completed", "failed"]

        if action not in ["create", "update"]:
            return json.dumps({
                "success": False, 
                "error": f"Invalid {action}. Must be 'create' or 'update'"
            })

        if action == "create":
            if not all([change_id, requested_by_id]):
                return json.dumps({"success": False, "error": "change_id and requested_by_id are required for create"})

            if change_id not in change_requests:
                return json.dumps({"success": False, "error": f"Change request {change_id} not found"})

            if requested_by_id not in users:
                return json.dumps({"success": False, "error": f"Requesting user {requested_by_id} not found"})

            if users[requested_by_id].get("role") not in ["system_administrator", "executive", "incident_manager"]:
                return json.dumps({"success": False, "error": f"Invalid role for requesting user {requested_by_id}"})

            if incident_id and incident_id not in incidents:
                return json.dumps({"success": False, "error": f"Incident {incident_id} not found"})

            if status and status not in valid_statuses:
                return json.dumps({"success": False, "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"})

            new_id = generate_id(rollback_requests)
            rollback_code = generate_code("RBK-2025", rollback_requests)

            new_request = {
                "rollback_id": str(new_id),
                "rollback_code": rollback_code,
                "change_id": change_id,
                "incident_id": incident_id,
                "requested_by_id": requested_by_id,
                "approved_by_id": approved_by_id,
                "executed_at": executed_at,
                "validation_completed": validation_completed if validation_completed is not None else False,
                "status": status if status else "requested",
                "created_at": "2025-10-02T12:00:00"
            }

            rollback_requests[str(new_id)] = new_request

            return json.dumps({
                "success": True, 
                "action": "create", 
                "rollback_id": str(new_id),
                "message": f"Rollback request {new_id} created successfully", 
                "rollback_request_data": new_request
            })

        elif action == "update":
            if not rollback_id:
                return json.dumps({"success": False, "error": "rollback_id is required for update"})

            if rollback_id not in rollback_requests:
                return json.dumps({"success": False, "error": f"Rollback request {rollback_id} not found"})

            if not any([approved_by_id is not None, executed_at, validation_completed is not None, status]):
                return json.dumps({"success": False, "error": "At least one field must be provided for update"})

            if status and status not in valid_statuses:
                return json.dumps({"success": False, "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"})

            updated_request = rollback_requests[rollback_id].copy()
            for field, value in [("approved_by_id", approved_by_id), ("executed_at", executed_at),
                                 ("validation_completed", validation_completed), ("status", status)]:
                if value is not None:
                    updated_request[field] = value

            rollback_requests[rollback_id] = updated_request

            return json.dumps({
                "success": True, 
                "action": "update", 
                "rollback_id": rollback_id,
                "message": f"Rollback request {rollback_id} updated successfully", 
                "rollback_request_data": updated_request
            })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "handle_rollback_requests",
                "description": "Create or update rollback request records in the incident management system. Tracks rollback execution, approvals, validation completion, and status progression. Ensures proper authorization from system administrators, executives, or incident managers. Essential for incident recovery, change management safety, and maintaining system reliability.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {"type": "string", "enum": ["create", "update"], "description": "Action to perform"},
                        "rollback_data": {
                            "type": "object",
                            "description": "Rollback request data",
                            "properties": {
                                "change_id": {"type": "string", "description": "Change request ID (required for create)"},
                                "requested_by_id": {"type": "string", "description": "Requesting user ID (required for create)"},
                                "incident_id": {"type": "string", "description": "Associated incident ID (optional)"},
                                "approved_by_id": {"type": "string", "description": "Approver user ID (optional)"},
                                "executed_at": {"type": "string", "description": "Execution timestamp YYYY-MM-DDTHH:MM:SS (optional)"},
                                "validation_completed": {"type": "boolean", "description": "Validation completed (optional)"},
                                "status": {"type": "string", "enum": ["requested", "approved", "in_progress", "completed", "failed"], "description": "Current status (optional)"}
                            },
                        },
                        "rollback_id": {"type": "string", "description": "ID of the Rollback request (required for update)"},
                    },
                    "required": ["action"]
                }
            }
        }
