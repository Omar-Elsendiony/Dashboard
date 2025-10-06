import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class HandleChangeRequests(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, change_data: Dict[str, Any] = None, change_id: str = None) -> str:
        """
        Create or update change request records.

        Actions:
        - create: Create new change request (requires change_data with title, change_type, requested_by_id, risk_level)
        - update: Update existing change request (requires change_id and change_data with fields to change)
        """
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1

        def generate_code(prefix: str, table: Dict[str, Any]) -> str:
            max_num = 0
            for record in table.values():
                code = record.get("change_code", "")
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
                "error": "Invalid data format for change requests"
            })

        change_requests = data.get("change_requests", {})
        incidents = data.get("incidents", {})
        users = data.get("users", {})

        # Enums/allowed values
        valid_change_types = ["emergency", "standard", "normal"]
        valid_risk_levels = ["high", "medium", "low"]
        valid_statuses = ["requested", "approved", "scheduled", "in_progress", "completed", "failed", "rolled_back"]

        # Approval roles allowed (require at least one)
        # approver_roles = ["technical_support", "incident_manager", "system_administrator", "executive"]

        if action == "create":
            if not change_data:
                return json.dumps({
                    "success": False,
                    "error": "change_data is required for create action"
                })

            # Validate required fields
            required_fields = ["title", "change_type", "requested_by_id", "risk_level"]
            missing = [f for f in required_fields if f not in change_data or change_data.get(f) in [None, ""]]
            if missing:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields for change creation: {', '.join(missing)}"
                })

            # Approval: require at least one approver flagged True in the change_data
            # if not any(change_data.get(role) for role in approver_roles):
            #     return json.dumps({
            #         "success": False,
            #         "error": "Missing approval for creating change request. Required: technical_support OR incident_manager OR system_administrator OR executive"
            #     })

            # Only allow known fields to be supplied
            allowed_fields = [
                "title", "change_type", "requested_by_id", "approved_by_id", "risk_level",
                "incident_id", "scheduled_start", "scheduled_end", "actual_start", "actual_end", "status"
            ]
            invalid_fields = [k for k in change_data.keys() if k not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for change creation: {', '.join(invalid_fields)}"
                })

            title = change_data["title"]
            change_type = change_data["change_type"]
            requested_by_id = str(change_data["requested_by_id"])
            risk_level = change_data["risk_level"]
            incident_id = change_data.get("incident_id")
            approved_by_id = change_data.get("approved_by_id")
            scheduled_start = change_data.get("scheduled_start")
            scheduled_end = change_data.get("scheduled_end")
            actual_start = change_data.get("actual_start")
            actual_end = change_data.get("actual_end")
            status = change_data.get("status")

            # Validate enums
            if change_type not in valid_change_types:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid change_type. Must be one of: {', '.join(valid_change_types)}"
                })

            if risk_level not in valid_risk_levels:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid risk_level. Must be one of: {', '.join(valid_risk_levels)}"
                })

            if status and status not in valid_statuses:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                })

            # Validate incident if specified
            if incident_id and incident_id not in incidents:
                return json.dumps({
                    "success": False,
                    "error": f"Incident {incident_id} not found"
                })

            # Validate requested_by exists
            if requested_by_id not in users:
                return json.dumps({
                    "success": False,
                    "error": f"Requester {requested_by_id} not found"
                })

            # Generate and create
            new_id = generate_id(change_requests)
            change_code = generate_code("CHG-2024", change_requests)
            new_change_request = {
                "change_id": str(new_id),
                "change_code": change_code,
                "incident_id": incident_id,
                "title": title,
                "change_type": change_type,
                "requested_by_id": requested_by_id,
                "approved_by_id": approved_by_id,
                "risk_level": risk_level,
                "scheduled_start": scheduled_start,
                "scheduled_end": scheduled_end,
                "actual_start": actual_start,
                "actual_end": actual_end,
                "status": status if status else "requested",
                "created_at": "2025-10-02T12:00:00",
                "updated_at": "2025-10-02T12:00:00"
            }

            change_requests[str(new_id)] = new_change_request

            return json.dumps({
                "success": True,
                "action": "create",
                "change_id": str(new_id),
                "message": f"Change request {new_id} created successfully",
                "change_request_data": new_change_request
            })

        elif action == "update":
            if not change_id:
                return json.dumps({
                    "success": False,
                    "error": "change_id is required for update action"
                })

            if change_id not in change_requests:
                return json.dumps({
                    "success": False,
                    "error": f"Change request {change_id} not found"
                })

            if not change_data:
                return json.dumps({
                    "success": False,
                    "error": "change_data is required for update action"
                })

            # Approval required for updates as well (at least one)
            # if not any(change_data.get(role) for role in approver_roles):
            #     return json.dumps({
            #         "success": False,
            #         "error": "Missing approval for updating change request. Required: technical_support OR incident_manager OR system_administrator OR executive"
            #     })

            # Only allow known update fields
            allowed_update_fields = [
                "title", "change_type", "requested_by_id", "approved_by_id", "risk_level",
                "incident_id", "scheduled_start", "scheduled_end", "actual_start", "actual_end", "status"
            ]
            invalid_fields = [k for k in change_data.keys() if k not in allowed_update_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for change update: {', '.join(invalid_fields)}"
                })

            # At least one valid field must be present
            if not any(field in change_data for field in allowed_update_fields):
                return json.dumps({
                    "success": False,
                    "error": "At least one updatable field must be provided in change_data"
                })

            current_change = change_requests[change_id].copy()

            # Validate and apply updates
            if "title" in change_data:
                current_change["title"] = change_data["title"]

            if "change_type" in change_data:
                ct = change_data["change_type"]
                if ct not in valid_change_types:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid change_type. Must be one of: {', '.join(valid_change_types)}"
                    })
                current_change["change_type"] = ct

            if "requested_by_id" in change_data:
                rb = str(change_data["requested_by_id"])
                if rb not in users:
                    return json.dumps({
                        "success": False,
                        "error": f"Requester {rb} not found"
                    })
                current_change["requested_by_id"] = rb

            if "approved_by_id" in change_data:
                current_change["approved_by_id"] = change_data["approved_by_id"]

            if "risk_level" in change_data:
                rl = change_data["risk_level"]
                if rl not in valid_risk_levels:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid risk_level. Must be one of: {', '.join(valid_risk_levels)}"
                    })
                current_change["risk_level"] = rl

            if "incident_id" in change_data:
                inc = change_data["incident_id"]
                if inc and inc not in incidents:
                    return json.dumps({
                        "success": False,
                        "error": f"Incident {inc} not found"
                    })
                current_change["incident_id"] = inc

            if "scheduled_start" in change_data:
                current_change["scheduled_start"] = change_data["scheduled_start"]
            if "scheduled_end" in change_data:
                current_change["scheduled_end"] = change_data["scheduled_end"]
            if "actual_start" in change_data:
                current_change["actual_start"] = change_data["actual_start"]
            if "actual_end" in change_data:
                current_change["actual_end"] = change_data["actual_end"]

            if "status" in change_data:
                st = change_data["status"]
                if st not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                    })
                current_change["status"] = st

            current_change["updated_at"] = "2025-10-02T12:00:00"
            change_requests[change_id] = current_change

            return json.dumps({
                "success": True,
                "action": "update",
                "change_id": change_id,
                "message": f"Change request {change_id} updated successfully",
                "change_request_data": current_change
            })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "handle_change_requests",
                "description": "Create or update change request records in the incident management system. Manages emergency, standard, and normal changes.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' or 'update'",
                            "enum": ["create", "update"]
                        },
                        "change_data": {
                            "type": "object",
                            "description": "Change data object. For create: requires title (short text), change_type (enum), requested_by_id (user ID), risk_level (enum). For update: include fields to change. SYNTAX: {\"key\": \"value\"}",
                            "properties": {
                                "title": {"type": "string", "description": "Change title (required for create)"},
                                "change_type": {
                                    "type": "string",
                                    "description": "Type of change (required for create)",
                                    "enum": ["emergency", "standard", "normal"]
                                },
                                "requested_by_id": {"type": "string", "description": "Requester user ID (required for create)"},
                                "risk_level": {
                                    "type": "string",
                                    "description": "Risk level (required for create)",
                                    "enum": ["high", "medium", "low"]
                                },
                                "incident_id": {"type": "string", "description": "Associated incident ID (optional)"},
                                "approved_by_id": {"type": "string", "description": "Approver user ID (optional)"},
                                "scheduled_start": {"type": "string", "description": "Scheduled start timestamp (optional)"},
                                "scheduled_end": {"type": "string", "description": "Scheduled end timestamp (optional)"},
                                "actual_start": {"type": "string", "description": "Actual start timestamp (optional)"},
                                "actual_end": {"type": "string", "description": "Actual end timestamp (optional)"},
                                "status": {
                                    "type": "string",
                                    "description": "Current status (optional)",
                                    "enum": ["requested", "approved", "scheduled", "in_progress", "completed", "failed", "rolled_back"]
                                },
                                # Inline approver flags (used to indicate approval presence)
                                # "technical_support": {"type": "boolean", "description": "Technical support approval flag (optional)"},
                                # "incident_manager": {"type": "boolean", "description": "Incident manager approval flag (optional)"},
                                # "system_administrator": {"type": "boolean", "description": "System admin approval flag (optional)"},
                                # "executive": {"type": "boolean", "description": "Executive approval flag (optional)"}
                            }
                        },
                        "change_id": {
                            "type": "string",
                            "description": "Unique identifier of the change request (required for update action only)"
                        }
                    },
                    "required": ["action"]
                }
            }
        }
