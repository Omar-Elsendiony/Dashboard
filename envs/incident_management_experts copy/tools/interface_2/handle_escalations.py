import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class HandleEscalations(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, escalation_data: Dict[str, Any] = None, escalation_id: str = None) -> str:
        """
        Create or update escalation records.

        Actions:
        - create: Create new escalation (requires escalation_data with incident_id, escalated_by_id, escalated_to_id, escalation_reason, escalation_level)
        - update: Update existing escalation (requires escalation_id and escalation_data with fields to change)
        """
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1

        def generate_code(prefix: str, table: Dict[str, Any]) -> str:
            max_num = 0
            for record in table.values():
                code = record.get("escalation_code", "")
                if code.startswith(prefix):
                    try:
                        num = int(code.split("-")[-1])
                        max_num = max(max_num, num)
                    except:
                        pass
            return f"{prefix}-{str(max_num + 1).zfill(5)}"

        if action not in ["create", "update"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid action '{action}'. Must be 'create' or 'update'"
            })

        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for escalations"
            })

        escalations = data.get("escalations", {})
        incidents = data.get("incidents", {})
        users = data.get("users", {})

        # Allowed/enums
        valid_levels = ["technical", "management", "executive", "vendor"]
        valid_reasons = ["sla_breach", "severity_increase", "resource_unavailable", "executive_request", "client_demand"]
        valid_statuses = ["open", "acknowledged", "resolved"]

        if action == "create":
            if not escalation_data:
                return json.dumps({
                    "success": False,
                    "error": "escalation_data is required for create action"
                })

            # Required fields
            required_fields = ["incident_id", "escalated_by_id", "escalated_to_id", "escalation_reason", "escalated_at", "escalation_level"]
            missing = [f for f in required_fields if f not in escalation_data]
            if missing:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields for escalation creation: {', '.join(missing)}"
                })
            
            # Only allow known fields to be supplied
            allowed_fields = [
                "incident_id", "escalated_by_id", "escalated_to_id", "escalation_reason",
                "escalated_at", "escalation_level", "acknowledged_at", "resolved_at, status"
            ]
            invalid_fields = [k for k in escalation_data.keys() if k not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for escalation creation: {', '.join(invalid_fields)}"
                })

            incident_id = str(escalation_data["incident_id"])
            escalated_by_id = str(escalation_data["escalated_by_id"])
            escalated_to_id = str(escalation_data["escalated_to_id"])
            escalation_reason = escalation_data["escalation_reason"]
            escalation_level = escalation_data["escalation_level"]
            acknowledged_at = escalation_data.get("acknowledged_at")
            resolved_at = escalation_data.get("resolved_at")
            status = escalation_data.get("status")

            # Validate incident
            if incident_id not in incidents:
                return json.dumps({"success": False, "error": f"Incident {incident_id} not found"})
            if incidents[incident_id].get("status") not in ["open", "in_progress"]:
                return json.dumps({"success": False, "error": "Incident must be open or in_progress"})

            # Validate users
            if escalated_by_id not in users or users[escalated_by_id].get("status") != "active":
                return json.dumps({"success": False, "error": f"Escalating user {escalated_by_id} not found or inactive"})
            if escalated_to_id not in users:
                return json.dumps({"success": False, "error": f"Target user {escalated_to_id} not found"})

            # Validate level/role and enums
            if escalation_level not in valid_levels:
                return json.dumps({"success": False, "error": f"Invalid escalation_level. Must be one of: {', '.join(valid_levels)}"})
            if escalation_reason not in valid_reasons:
                return json.dumps({"success": False, "error": f"Invalid escalation_reason. Must be one of: {', '.join(valid_reasons)}"})
            if status and status not in valid_statuses:
                return json.dumps({"success": False, "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"})

            # Generate and create
            new_id = generate_id(escalations)
            escalation_code = generate_code("ESC-2025", escalations)
            new_escalation = {
                "escalation_id": str(new_id),
                "escalation_code": escalation_code,
                "incident_id": incident_id,
                "escalated_by_id": escalated_by_id,
                "escalated_to_id": escalated_to_id,
                "escalation_reason": escalation_reason,
                "escalation_level": escalation_level,
                "acknowledged_at": acknowledged_at,
                "resolved_at": resolved_at,
                "status": status if status else "open",
                "escalated_at": "2025-10-02T12:00:00",
                "created_at": "2025-10-02T12:00:00",
                "updated_at": "2025-10-02T12:00:00"
            }
            escalations[str(new_id)] = new_escalation

            return json.dumps({
                "success": True,
                "action": "create",
                "escalation_id": str(new_id),
                "message": f"Escalation {new_id} created successfully",
                "escalation_data": new_escalation
            })

        elif action == "update":
            if not escalation_id:
                return json.dumps({"success": False, "error": "escalation_id is required for update action"})
            if escalation_id not in escalations:
                return json.dumps({"success": False, "error": f"Escalation {escalation_id} not found"})
            if not escalation_data:
                return json.dumps({"success": False, "error": "escalation_data is required for update action"})

            current = escalations[escalation_id].copy()

            for field in ["escalation_code", "acknowledged_at", "resolved_at", "status"]:
                if field in escalation_data:
                    value = escalation_data[field]
                    if field == "status" and value not in valid_statuses:
                        return json.dumps({"success": False, "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"})
                    current[field] = value

            current["updated_at"] = "2025-10-02T12:00:00"
            escalations[escalation_id] = current

            return json.dumps({
                "success": True,
                "action": "update",
                "escalation_id": escalation_id,
                "message": f"Escalation {escalation_id} updated successfully",
                "escalation_data": current
            })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "handle_escalations",
                "description": "Create or update escalation records in the incident management system. Supports multiple escalation levels (technical, management, executive, vendor) with role validation. Tracks escalation reasons and statuses.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {"type": "string", "enum": ["create", "update"], "description": "Action to perform"},
                        "escalation_data": {"type": "object", "description": "Escalation data object for create/update"},
                        "escalation_id": {"type": "string", "description": "Escalation ID for update action only"}
                    },
                    "required": ["action"]
                }
            }
        }
