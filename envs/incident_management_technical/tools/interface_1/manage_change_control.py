import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class ManageChangeControl(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        action: str,
        entity_type: str = "change_request",
        change_request_data: Optional[Dict[str, Any]] = None,
        rollback_request_data: Optional[Dict[str, Any]] = None,
        change_id: Optional[str] = None
    ) -> str:
        """
        Create or update change request or rollback request records.

        Entity Types:
        - change_request: For managing change requests
        - rollback_request: For managing rollback requests

        Actions:
        - create: Create a new change/rollback request record
        - update: Update an existing change/rollback request record
        """

        def generate_id(table: Dict[str, Any], prefix: str) -> str:
            if not table:
                return f"{prefix}1"
            max_id = 0
            for k in table.keys():
                try:
                    num = int(k[len(prefix):])
                    if num > max_id:
                        max_id = num
                except ValueError:
                    continue
            return f"{prefix}{max_id + 1}"

        def generate_change_number(table: Dict[str, Any]) -> str:
            if not table:
                return "CHG0000001"
            max_num = 0
            for change in table.values():
                change_num = change.get("change_number", "")
                if change_num.startswith("CHG"):
                    try:
                        num = int(change_num[3:])
                        if num > max_num:
                            max_num = num
                    except ValueError:
                        continue
            return f"CHG{max_num + 1:07d}"

        def generate_rollback_number(table: Dict[str, Any]) -> str:
            if not table:
                return "RBK0000001"
            max_num = 0
            for rollback in table.values():
                rollback_num = rollback.get("rollback_number", "")
                if rollback_num.startswith("RBK"):
                    try:
                        num = int(rollback_num[3:])
                        if num > max_num:
                            max_num = num
                    except ValueError:
                        continue
            return f"RBK{max_num + 1:07d}"

        timestamp = "2025-10-07T12:00:00"

        if entity_type not in ["change_request", "rollback_request"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'change_request' or 'rollback_request'"
            })

        if action not in ["create", "update"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid action '{action}'. Must be 'create' or 'update'"
            })

        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format"
            })

        change_requests = data.get("change_requests", {})
        rollback_requests = data.get("rollback_requests", {})
        users = data.get("users", {})
        incidents = data.get("incidents", {})
        problem_tickets = data.get("problem_tickets", {})

        # Define valid enums based on DBML schema
        valid_change_types = ["standard", "normal", "emergency"]
        valid_risk_levels = ["low", "medium", "high", "critical"]
        valid_change_statuses = ["requested", "approved", "denied", "scheduled", "implemented", "cancelled"]
        valid_rollback_statuses = ["requested", "approved", "executed", "failed"]

        # ==================== CHANGE REQUEST LOGIC ====================
        if entity_type == "change_request" and action == "create":
            if not change_request_data:
                return json.dumps({
                    "success": False,
                    "error": "change_request_data is required for create action"
                })

            # Validate required fields as per DBML
            required_fields = ["title", "description", "change_type", "risk_level", "requested_by"]
            missing_fields = [field for field in required_fields if field not in change_request_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields: {', '.join(missing_fields)}"
                })
            
            # Validate non-empty required fields
            for field in required_fields:
                if not change_request_data[field] or (isinstance(change_request_data[field], str) and change_request_data[field].strip() == ""):
                    return json.dumps({
                        "success": False,
                        "error": f"Field '{field}' cannot be empty"
                    })

            # Validate enums
            if change_request_data["change_type"] not in valid_change_types:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid change_type '{change_request_data['change_type']}'. Must be one of: {', '.join(valid_change_types)}"
                })
            if change_request_data["risk_level"] not in valid_risk_levels:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid risk_level '{change_request_data['risk_level']}'. Must be one of: {', '.join(valid_risk_levels)}"
                })
            
            # Status defaults to 'requested' if not provided
            status = change_request_data.get("status", "requested")
            if status not in valid_change_statuses:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid status '{status}'. Must be one of: {', '.join(valid_change_statuses)}"
                })

            # Validate requested_by user exists and is active
            requested_by = str(change_request_data["requested_by"]).strip().strip('"')
            if requested_by not in users:
                return json.dumps({
                    "success": False,
                    "error": f"User '{requested_by}' not found"
                })
            if users[requested_by]["status"] != "active":
                return json.dumps({
                    "success": False,
                    "error": f"User '{requested_by}' is not active"
                })
            
            # Validate optional approved_by if provided
            approved_by = change_request_data.get("approved_by")
            if approved_by:
                approved_by = str(approved_by).strip().strip('"')
                if approved_by not in users:
                    return json.dumps({
                        "success": False,
                        "error": f"Approved by user '{approved_by}' not found"
                    })
                if users[approved_by]["status"] != "active":
                    return json.dumps({
                        "success": False,
                        "error": f"Approved by user '{approved_by}' is not active"
                    })
            
            # Validate optional incident_id if provided
            incident_id = change_request_data.get("incident_id")
            if incident_id:
                incident_id = str(incident_id).strip().strip('"')
                if incident_id not in incidents:
                    return json.dumps({
                        "success": False,
                        "error": f"Incident '{incident_id}' not found"
                    })
            
            # Validate optional problem_ticket_id if provided
            problem_ticket_id = change_request_data.get("problem_ticket_id")
            if problem_ticket_id:
                problem_ticket_id = str(problem_ticket_id).strip().strip('"')
                if problem_ticket_id not in problem_tickets:
                    return json.dumps({
                        "success": False,
                        "error": f"Problem ticket '{problem_ticket_id}' not found"
                    })

            new_id = generate_id(change_requests, "")
            new_change_number = generate_change_number(change_requests)
            
            new_cr = {
                "change_id": new_id,
                "change_number": new_change_number,
                "incident_id": incident_id if incident_id else None,
                "problem_ticket_id": problem_ticket_id if problem_ticket_id else None,
                "title": change_request_data["title"],
                "description": change_request_data["description"],
                "change_type": change_request_data["change_type"],
                "risk_level": change_request_data["risk_level"],
                "requested_by": requested_by,
                "approved_by": approved_by if approved_by else None,
                "status": status,
                "implementation_date": change_request_data.get("implementation_date"),
                "created_at": timestamp,
                "updated_at": timestamp
            }
            change_requests[new_id] = new_cr
            return json.dumps({
                "success": True,
                "action": "create",
                "change_id": new_id,
                "change_request_data": new_cr
            })

        elif entity_type == "change_request" and action == "update":
            if not change_id:
                return json.dumps({
                    "success": False,
                    "error": "change_id is required for update action"
                })
            change_id = str(change_id).strip().strip('"')
            if change_id not in change_requests:
                return json.dumps({
                    "success": False,
                    "error": f"Change request '{change_id}' not found"
                })

            if not change_request_data:
                return json.dumps({
                    "success": False,
                    "error": "change_request_data is required for update action"
                })

            # Allowed fields for update (change_id, change_number, created_at are not updatable)
            allowed_fields = [
                "title", "description", "change_type", "risk_level", "status",
                "requested_by", "approved_by", "implementation_date",
                "incident_id", "problem_ticket_id"
            ]
            invalid_fields = [field for field in change_request_data if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for update: {', '.join(invalid_fields)}"
                })
            
            # Validate non-empty fields (if provided, they shouldn't be empty strings, but nullable fields can be None)
            nullable_fields = ["approved_by", "implementation_date", "incident_id", "problem_ticket_id"]
            for field, value in change_request_data.items():
                if field not in nullable_fields and (value is None or (isinstance(value, str) and value.strip() == "")):
                    return json.dumps({
                        "success": False,
                        "error": f"Field '{field}' cannot be empty"
                    })
                elif field in nullable_fields and (isinstance(value, str) and value.strip() == ""):
                    change_request_data[field] = None # Treat empty string as null for nullable fields

            # Validate enums if provided
            if "change_type" in change_request_data and change_request_data["change_type"] not in valid_change_types:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid change_type. Must be one of: {', '.join(valid_change_types)}"
                })
            if "risk_level" in change_request_data and change_request_data["risk_level"] not in valid_risk_levels:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid risk_level. Must be one of: {', '.join(valid_risk_levels)}"
                })
            if "status" in change_request_data and change_request_data["status"] not in valid_change_statuses:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid status. Must be one of: {', '.join(valid_change_statuses)}"
                })

            # Validate user fields if provided
            for user_field in ["requested_by", "approved_by"]:
                if user_field in change_request_data and change_request_data[user_field] is not None:
                    user_id = str(change_request_data[user_field]).strip().strip('"')
                    if user_id not in users:
                        return json.dumps({
                            "success": False,
                            "error": f"User '{user_id}' for field '{user_field}' not found"
                        })
                    if users[user_id]["status"] != "active":
                        return json.dumps({
                            "success": False,
                            "error": f"User '{user_id}' for field '{user_field}' is not active"
                        })
                    change_request_data[user_field] = user_id
                elif user_field in change_request_data and change_request_data[user_field] is None:
                    change_request_data[user_field] = None # Allow setting to null

            # Validate incident_id if provided
            if "incident_id" in change_request_data and change_request_data["incident_id"] is not None:
                incident_id = str(change_request_data["incident_id"]).strip().strip('"')
                if incident_id not in incidents:
                    return json.dumps({
                        "success": False,
                        "error": f"Incident '{incident_id}' not found"
                    })
                change_request_data["incident_id"] = incident_id
            elif "incident_id" in change_request_data and change_request_data["incident_id"] is None:
                change_request_data["incident_id"] = None # Allow setting to null
            
            # Validate problem_ticket_id if provided
            if "problem_ticket_id" in change_request_data and change_request_data["problem_ticket_id"] is not None:
                problem_ticket_id = str(change_request_data["problem_ticket_id"]).strip().strip('"')
                if problem_ticket_id not in problem_tickets:
                    return json.dumps({
                        "success": False,
                        "error": f"Problem ticket '{problem_ticket_id}' not found"
                    })
                change_request_data["problem_ticket_id"] = problem_ticket_id
            elif "problem_ticket_id" in change_request_data and change_request_data["problem_ticket_id"] is None:
                change_request_data["problem_ticket_id"] = None # Allow setting to null

            updated_cr = change_requests[change_id].copy()
            for key, value in change_request_data.items():
                updated_cr[key] = value
            updated_cr["updated_at"] = timestamp
            change_requests[change_id] = updated_cr
            return json.dumps({
                "success": True,
                "action": "update",
                "change_id": change_id,
                "change_request_data": updated_cr
            })

        # ==================== ROLLBACK REQUEST LOGIC ====================
        elif entity_type == "rollback_request" and action == "create":
            if not rollback_request_data:
                return json.dumps({
                    "success": False,
                    "error": "rollback_request_data is required for create action"
                })

            # Validate required fields as per DBML schema
            required_fields = ["change_id", "incident_id", "title", "rollback_reason", "requested_by"]
            missing_fields = [field for field in required_fields if field not in rollback_request_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields: {', '.join(missing_fields)}"
                })
            
            # Validate non-empty required fields
            for field in required_fields:
                if not rollback_request_data[field] or (isinstance(rollback_request_data[field], str) and rollback_request_data[field].strip() == ""):
                    return json.dumps({
                        "success": False,
                        "error": f"Field '{field}' cannot be empty"
                    })

            # Status defaults to 'requested' if not provided
            status = rollback_request_data.get("status", "requested")
            if status not in valid_rollback_statuses:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid status '{status}'. Must be one of: {', '.join(valid_rollback_statuses)}"
                })

            # Validate change_id FK
            change_id_fk = str(rollback_request_data["change_id"]).strip().strip('"')
            if change_id_fk not in change_requests:
                return json.dumps({
                    "success": False,
                    "error": f"Change request '{change_id_fk}' not found"
                })

            # Validate incident_id FK
            incident_id_fk = str(rollback_request_data["incident_id"]).strip().strip('"')
            if incident_id_fk not in incidents:
                return json.dumps({
                    "success": False,
                    "error": f"Incident '{incident_id_fk}' not found"
                })

            # Validate requested_by user exists and is active
            requested_by = str(rollback_request_data["requested_by"]).strip().strip('"')
            if requested_by not in users:
                return json.dumps({
                    "success": False,
                    "error": f"User '{requested_by}' not found"
                })
            if users[requested_by]["status"] != "active":
                return json.dumps({
                    "success": False,
                    "error": f"User '{requested_by}' is not active"
                })

            new_id = generate_id(rollback_requests, "")
            new_rollback_number = generate_rollback_number(rollback_requests)
            
            new_rbk = {
                "rollback_id": new_id,
                "rollback_number": new_rollback_number,
                "change_id": change_id_fk,
                "incident_id": incident_id_fk,
                "title": rollback_request_data["title"],
                "rollback_reason": rollback_request_data["rollback_reason"],
                "requested_by": requested_by,
                "status": status,
                "executed_at": rollback_request_data.get("executed_at"),
                "created_at": timestamp
            }
            rollback_requests[new_id] = new_rbk
            return json.dumps({
                "success": True,
                "action": "create",
                "rollback_id": new_id,
                "rollback_request_data": new_rbk
            })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manage_change_control",
                "description": "Create or update change request records, and create rollback request records in the change management system. This tool supports documenting, categorizing, and tracking changes to IT services and infrastructure, as well as creating rollback requests for problematic changes. Note: rollback_requests only support create action, not update.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' to establish a new record, 'update' to modify an existing change request (not supported for rollback_requests)."
                        },
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to manage. Must be one of: change_request, rollback_request. change_request for change requests (supports create and update), rollback_request for rollback requests (only supports create). Defaults to 'change_request'."
                        },
                        "change_request_data": {
                            "type": "object",
                            "description": "Data object containing fields for creating or updating a change request (used when entity_type='change_request').",
                            "properties": {
                                "title": {
                                    "type": "string",
                                    "description": "Brief title or summary of the change (required for create, cannot be empty). Updatable."
                                },
                                "description": {
                                    "type": "string",
                                    "description": "Detailed description of the change, including its purpose and scope (required for create, cannot be empty). Updatable."
                                },
                                "change_type": {
                                    "type": "string",
                                    "description": "Classification of the change (required for create). Must be one of: standard, normal, emergency. Updatable."
                                },
                                "risk_level": {
                                    "type": "string",
                                    "description": "Risk level of the change (required for create). Must be one of: low, medium, high, critical. Updatable."
                                },
                                "status": {
                                    "type": "string",
                                    "description": "Current status of the change request (optional for create, defaults to 'requested'). Must be one of: requested, approved, denied, scheduled, implemented, cancelled. Updatable."
                                },
                                "requested_by": {
                                    "type": "string",
                                    "description": "User ID of the person who requested the change (required for create, must be an active user). Updatable."
                                },
                                "approved_by": {
                                    "type": "string",
                                    "description": "User ID of the person who approved the change (optional, must be an active user if provided). Updatable, can be set to null."
                                },
                                "implementation_date": {
                                    "type": "string",
                                    "description": "Date/timestamp when change was implemented (optional). Accepts YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS format. Updatable, can be set to null."
                                },
                                "incident_id": {
                                    "type": "string",
                                    "description": "Related incident ID (optional, must exist if provided). Updatable, can be set to null."
                                },
                                "problem_ticket_id": {
                                    "type": "string",
                                    "description": "Related problem ticket ID (optional, must exist if provided). Updatable, can be set to null."
                                }
                            }
                        },
                        "rollback_request_data": {
                            "type": "object",
                            "description": "Data object containing fields for creating a rollback request (used when entity_type='rollback_request'). Only supports create action.",
                            "properties": {
                                "change_id": {
                                    "type": "string",
                                    "description": "ID of the change request to be rolled back (required for create, cannot be empty, must exist)."
                                },
                                "incident_id": {
                                    "type": "string",
                                    "description": "ID of the incident that prompted the rollback (required for create, cannot be empty, must exist)."
                                },
                                "title": {
                                    "type": "string",
                                    "description": "Brief title or summary of the rollback (required for create, cannot be empty)."
                                },
                                "rollback_reason": {
                                    "type": "string",
                                    "description": "Detailed reason for the rollback (required for create, cannot be empty)."
                                },
                                "requested_by": {
                                    "type": "string",
                                    "description": "User ID of the person who requested the rollback (required for create, must be an active user)."
                                },
                                "status": {
                                    "type": "string",
                                    "description": "Current status of the rollback request (optional for create, defaults to 'requested'). Must be one of: requested, approved, executed, failed."
                                },
                                "executed_at": {
                                    "type": "string",
                                    "description": "Date/timestamp when rollback was executed (optional). Accepts YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS format."
                                }
                            }
                        },
                        "change_id": {
                            "type": "string",
                            "description": "The unique identifier of the change request to update. Required for 'update' action only when entity_type='change_request'."
                        }
                    },
                    "required": ["action"]
                }
            }
        }