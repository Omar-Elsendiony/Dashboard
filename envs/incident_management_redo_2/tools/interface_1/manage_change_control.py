import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ManageChangeControl(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, action: str, change_control_data: Dict[str, Any] = None, change_id: str = None, rollback_id: str = None) -> str:
        """
        Create or update change control records (change requests or rollback requests).
        
        Entity Types:
        - change_requests: Manage change requests
        - rollback_requests: Manage rollback requests
        
        Actions:
        - create: Create new change or rollback request
        - update: Update existing change or rollback request
        """
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        def generate_number(entity_type: str, entity_id: int) -> str:
            """Generate entity number based on type"""
            if entity_type == "change_requests":
                return f"CHG{str(entity_id).zfill(7)}"
            elif entity_type == "rollback_requests":
                return f"RBK{str(entity_id).zfill(7)}"
        
        if entity_type not in ["change_requests", "rollback_requests"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'change_requests' or 'rollback_requests'"
            })
        
        if action not in ["create", "update"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid action '{action}'. Must be 'create' or 'update'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        # get existing data tables
        change_requests = data.get("change_requests", {})
        rollback_requests = data.get("rollback_requests", {})
        incidents = data.get("incidents", {})
        users = data.get("users", {})

        # allowed enums
        valid_change_types = ["standard", "normal", "emergency"]
        valid_risk_levels = ["low", "medium", "high", "critical"]
        valid_change_statuses = ["requested", "approved", "denied", "scheduled", "implemented", "cancelled", "rolled_back"]
        valid_rollback_statuses = ["requested", "approved", "executed", "failed"]

        
        # Handle change_requests
        if entity_type == "change_requests":
            # for create action
            if action == "create":
                if not change_control_data:
                    return json.dumps({
                        "success": False,
                        "error": "change_control_data is required for create action"
                    })

                # Validate required fields for create
                required_fields = ["title", "description", "change_type", "risk_level", "requested_by"]
                
                missing_fields = [field for field in required_fields if field not in change_control_data]
                if missing_fields:
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: Missing required fields for create action: {', '.join(missing_fields)}"
                    })
                
                # Allowed fields
                allowed_fields = ["incident_id", "title", "description", "change_type", "risk_level", "requested_by", "approved_by", "status", "implementation_date"]

                change_fields = [field for field in change_control_data if field not in allowed_fields]
                if change_fields:
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: Unrecognized fields in change_control_data: {', '.join(change_fields)}"
                    })
                
                # Validate title is not empty
                if not str(change_control_data["title"]).strip():
                    return json.dumps({
                        "success": False,
                        "error": "Halt: title cannot be empty"
                    })
                
                # Validate description is not empty
                if not str(change_control_data["description"]).strip():
                    return json.dumps({
                        "success": False,
                        "error": "Halt: description cannot be empty"
                    })
                
                # Validate change_type enum
                if change_control_data["change_type"] not in valid_change_types:
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: Invalid change_type. Must be one of: {', '.join(valid_change_types)}"
                    })
                
                # Validate risk_level enum
                if change_control_data["risk_level"] not in valid_risk_levels:
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: Invalid risk_level. Must be one of: {', '.join(valid_risk_levels)}"
                    })
                
                # Validate requested_by user exists
                if str(change_control_data["requested_by"]) not in users:
                    return json.dumps({
                        "success": False,
                        "error": "Halt: User requested_by not found"
                    })
                
                # Validate that requested_by user is active
                if users[str(change_control_data["requested_by"])]["status"] != "active": 
                    return json.dumps({ 
                        "success": False, 
                        "error": "Halt: User requested_by must be active" 
                    })
                
                if "approved_by" in change_control_data:
                    # Validate approved_by user exists if provided
                    if str(change_control_data["approved_by"]) not in users:
                        return json.dumps({
                            "success": False,
                            "error": "Halt: User approved_by not found"
                        })
                    
                    # Validate that approved_by user is active
                    if users[str(change_control_data["approved_by"])]["status"] != "active":
                        return json.dumps({
                            "success": False,
                            "error": "Halt: User approved_by must be active"
                        })
                
                # Validate incident_id exists if provided
                if "incident_id" in change_control_data and change_control_data["incident_id"] not in incidents:
                    return json.dumps({
                        "success": False,
                        "error": "Halt: Incident not found"
                    })
                
                # Validate status enum
                status = change_control_data.get("status", "requested")
                if status not in valid_change_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: Invalid change status - must be one of: {', '.join(valid_change_statuses)}"
                    })
                
                # Generate new change ID
                new_change_id = generate_id(change_requests)
                change_number = generate_number("change_requests", new_change_id)
                
                # Create new change request record
                new_change = {
                    "change_id": str(new_change_id),
                    "change_number": str(change_number),
                    "incident_id": str(change_control_data["incident_id"]) if "incident_id" in change_control_data else None,
                    "title": change_control_data["title"],
                    "description": change_control_data["description"],
                    "change_type": change_control_data["change_type"],
                    "risk_level": change_control_data["risk_level"],
                    "requested_by": change_control_data["requested_by"],
                    "approved_by": change_control_data["approved_by"] if "approved_by" in change_control_data else None,
                    "status": status,
                    "implementation_date": change_control_data["implementation_date"] if "implementation_date" in change_control_data else None,
                    "created_at": "2025-10-07T00:00:00",
                    "updated_at": "2025-10-07T00:00:00"
                }
                
                change_requests[str(new_change_id)] = new_change
                
                return json.dumps({
                    "success": True,
                    "action": "create",
                    "change_id": str(new_change_id),
                    "message": f"Change request {new_change_id} created successfully",
                    "change_data": new_change
                })
            

            # for update action
            elif action == "update":
                if not change_id:
                    return json.dumps({
                        "success": False,
                        "error": "Halt: change_id is required for update action"
                    })
                
                if str(change_id) not in change_requests:
                    return json.dumps({
                        "success": False,
                        "error": "Halt: Change request not found"
                    })
                
                if not change_control_data:
                    return json.dumps({
                        "success": False,
                        "error": "change_control_data is required for create action"
                    })
                
                # Validate at least one optional field is provided
                update_fields = ["incident_id", "title", "description", "change_type", "risk_level", "requested_by", "approved_by", "status", "implementation_date"]

                provided_fields = [field for field in update_fields if field in change_control_data]
                if not provided_fields:
                    return json.dumps({
                        "success": False,
                        "error": f"At least one optional field must be provided for updates {', '.join(update_fields)}"
                    })
                
                # Validate only allowed fields for updates
                invalid_fields = [field for field in change_control_data.keys() if field not in update_fields]
                if invalid_fields:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid fields for change updating: {', '.join(invalid_fields)}"
                    })

                if "title" in change_control_data:
                    if not str(change_control_data["title"]).strip():
                        return json.dumps({
                            "success": False,
                            "error": "Halt: title cannot be empty"
                        })
                
                if "description" in change_control_data:
                    if not str(change_control_data["description"]).strip():
                        return json.dumps({
                            "success": False,
                            "error": "Halt: description cannot be empty"
                        })
                
                if "change_type" in change_control_data:
                    if change_control_data["change_type"] not in valid_change_types:
                        return json.dumps({
                            "success": False,
                            "error": f"Halt: Invalid change_type. Must be one of: {', '.join(valid_change_types)}"
                        })
                
                if "risk_level" in change_control_data:
                    if change_control_data["risk_level"] not in valid_risk_levels:
                        return json.dumps({
                            "success": False,
                            "error": f"Halt: Invalid risk_level. Must be one of: {', '.join(valid_risk_levels)}"
                        })
                
                if "approved_by" in change_control_data:
                    if str(change_control_data["approved_by"]) not in users:
                        return json.dumps({
                            "success": False,
                            "error": "Halt: User approved_by not found"
                        })
                    
                    if users[str(change_control_data["approved_by"])]["status"] != "active":
                        return json.dumps({
                            "success": False,
                            "error": "Halt: User approved_by must be active"
                        })
                    
                if "status" in change_control_data:
                    if change_control_data["status"] not in valid_change_statuses:
                        return json.dumps({
                            "success": False,
                            "error": f"Halt: Invalid status. Must be one of: {', '.join(valid_change_statuses)}"
                        })
                
                if "incident_id" in change_control_data:
                    if change_control_data["incident_id"] not in incidents:
                        return json.dumps({
                            "success": False,
                            "error": "Halt: Incident not found"
                        })
                
                # Get current change request record
                current_change = change_requests[str(change_id)]
                # Update change request record
                updated_change = current_change.copy()
                for key, value in change_control_data.items():
                    if key in ["incident_id", "approved_by", "implementation_date"]:
                        updated_change[key] = str(value) if value not in (None, "") else None
                    else:
                        updated_change[key] = value
                
                updated_change["updated_at"] = "2025-10-07T00:00:00"

                change_requests[change_id] = updated_change
                
                return json.dumps({
                    "success": True,
                    "action": "update",
                    "change_id": str(change_id),
                    "message": f"Change request {change_id} updated successfully",
                    "change_data": updated_change
                })
        
        # Handle rollback_requests
        elif entity_type == "rollback_requests":
            # for create action
            if action == "create":
                if not change_control_data:
                    return json.dumps({
                        "success": False,
                        "error": "change_control_data is required for create action"
                    })
                
                # Validate required fields for create
                required_fields = ["change_id", "title", "rollback_reason", "requested_by"]
                
                missing_fields = [field for field in required_fields if field not in change_control_data]
                if missing_fields:
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: Missing required fields for create action: {', '.join(missing_fields)}"
                    })
                
                # Allowed fields
                allowed_fields = ["change_id", "incident_id", "title", "rollback_reason", "requested_by", "status", "executed_at"]

                rollback_fields = [field for field in change_control_data if field not in allowed_fields]
                if rollback_fields:
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: Unrecognized fields in change_control_data: {', '.join(rollback_fields)}"
                    })

                # Validate change_id exists
                if str(change_control_data["change_id"]) not in change_requests:
                    return json.dumps({
                        "success": False,
                        "error": "Halt: Change request not found"
                    })
                
                # Validate that incident exists if provided
                if "incident_id" in change_control_data:
                    if str(change_control_data["incident_id"]) not in incidents:
                        return json.dumps({
                            "success": False,
                            "error": "Halt: Incident not found"
                        })
                
                # Validate title is not empty
                if not str(change_control_data["title"]).strip():
                    return json.dumps({
                        "success": False,
                        "error": "Halt: title cannot be empty"
                    })
                
                # Validate rollback_reason is not empty
                if not str(change_control_data["rollback_reason"]).strip():
                    return json.dumps({
                        "success": False,
                        "error": "Halt: rollback_reason cannot be empty"
                    })
                
                # Validate requested_by user exists
                if str(change_control_data["requested_by"]) not in users:
                    return json.dumps({
                        "success": False,
                        "error": "Halt: User requested_by not found"
                    })
                
                # Validate that requested_by user is active
                if users[str(change_control_data["requested_by"])]["status"] != "active":
                    return json.dumps({
                        "success": False,
                        "error": "Halt: User requested_by must be active"
                    })
                
                # Validate status enum
                status = change_control_data.get("status", "requested")
                if status not in valid_rollback_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: Invalid rollback status - must be one of: {', '.join(valid_rollback_statuses)}"
                    })
                
                # Generate new rollback ID
                new_rollback_id = generate_id(rollback_requests)
                rollback_number = generate_number("rollback_requests", new_rollback_id)
                
                # Create new rollback request record
                new_rollback = {
                    "rollback_id": str(new_rollback_id),
                    "rollback_number": str(rollback_number),
                    "change_id": str(change_control_data["change_id"]),
                    "incident_id": str(change_control_data["incident_id"]) if "incident_id" in change_control_data else None,
                    "title": change_control_data["title"],
                    "rollback_reason": change_control_data["rollback_reason"],
                    "requested_by": change_control_data["requested_by"],
                    "status": status,
                    "executed_at": change_control_data["executed_at"] if "executed_at" in change_control_data else None,
                    "created_at": "2025-10-07T00:00:00"
                }
                
                rollback_requests[str(new_rollback_id)] = new_rollback
                
                return json.dumps({
                    "success": True,
                    "action": "create",
                    "rollback_id": str(new_rollback_id),
                    "message": f"Rollback request {new_rollback_id} created successfully",
                    "rollback_data": new_rollback
                })
            
            # for update action
            elif action == "update":
                if not rollback_id:
                    return json.dumps({
                        "success": False,
                        "error": "Halt: rollback_id is required for update action"
                    })
                
                if rollback_id not in rollback_requests:
                    return json.dumps({
                        "success": False,
                        "error": "Halt: Rollback request not found"
                    })
                
                if not change_control_data:
                    return json.dumps({
                        "success": False,
                        "error": "change_control_data is required for update action"
                    })
                
                update_fields = ["change_id", "incident_id", "title", "rollback_reason", "requested_by", "status", "executed_at"]

                provided_fields = [field for field in update_fields if field in change_control_data]
                if not provided_fields:
                    return json.dumps({
                        "success": False,
                        "error": f"At least one optional field must be provided for updates {', '.join(update_fields)}"
                    })
                
                # Validate only allowed fields for updates
                invalid_fields = [field for field in change_control_data.keys() if field not in update_fields]
                if invalid_fields:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid fields for rollback updating: {', '.join(invalid_fields)}"
                    })

                # Validate change_id exists if provided
                if "change_id" in change_control_data:
                    if str(change_control_data["change_id"]) not in change_requests:
                        return json.dumps({
                            "success": False,
                            "error": "Halt: Change request not found"
                        })
                
                # Validate that incident exists if provided
                if "incident_id" in change_control_data:
                    if str(change_control_data["incident_id"]) not in incidents:
                        return json.dumps({
                            "success": False,
                            "error": "Halt: Incident not found"
                        })
                
                # Validate title is not empty if provided
                if "title" in change_control_data:
                    if not str(change_control_data["title"]).strip():
                        return json.dumps({
                            "success": False,
                            "error": "Halt: title cannot be empty"
                        })
                
                # Validate rollback_reason is not empty if provided
                if "rollback_reason" in change_control_data:
                    if not str(change_control_data["rollback_reason"]).strip():
                        return json.dumps({
                            "success": False,
                            "error": "Halt: rollback_reason cannot be empty"
                        })
                
                # Validate requested_by user exists if provided
                if "requested_by" in change_control_data:
                    if str(change_control_data["requested_by"]) not in users:
                        return json.dumps({
                            "success": False,
                            "error": "Halt: User requested_by not found"
                        })
                
                    # Validate that requested_by user is active
                    if users[str(change_control_data["requested_by"])]["status"] != "active":
                        return json.dumps({
                            "success": False,
                            "error": "Halt: User requested_by must be active"
                        })
                    
                if "status" in change_control_data:
                    if change_control_data["status"] not in valid_rollback_statuses:
                        return json.dumps({
                            "success": False,
                            "error": f"Halt: Invalid status. Must be one of: {', '.join(valid_rollback_statuses)}"
                        })
                
                # Get current rollback request
                current_rollback = rollback_requests[str(rollback_id)]
                # Update rollback request record
                updated_rollback = current_rollback.copy()
                for key, value in change_control_data.items():
                    if key in ["incident_id", "executed_at"]:
                        updated_rollback[key] = str(value) if value not in (None, "") else None
                    else:
                        updated_rollback[key] = value
                
                rollback_requests[str(rollback_id)] = updated_rollback
                
                return json.dumps({
                    "success": True,
                    "action": "update",
                    "rollback_id": str(rollback_id),
                    "message": f"Rollback request {rollback_id} updated successfully",
                    "rollback_data": updated_rollback
                })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manage_change_control",
                "description": "Create or update change control records (change requests or rollback requests) in the incident management system. This tool manages change control workflows with comprehensive validation of changes, rollbacks, risk levels, and approval processes. For change requests: creates and updates change records with proper validation of change types (standard, normal, emergency), risk levels (low, medium, high, critical), and status transitions. For rollback requests: manages rollback workflows linked to change requests and incidents. Validates user assignments, incident relationships, and maintains change audit trail. Essential for change management, rollback procedures, and maintaining proper change control processes.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Entity type to manage: 'change_requests' for change requests, 'rollback_requests' for rollback requests",
                            "enum": ["change_requests", "rollback_requests"]
                        },
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' to create new record, 'update' to modify existing record",
                            "enum": ["create", "update"]
                        },
                        "change_control_data": {
                            "type": "object",
                            "description": "Data for creating or updating change or rollback requests.",
                            "properties": {
                                "change_id": {
                                    "type": "string",
                                    "description": "Unique identifier of the change request (required for create of rollback_requests)"
                                },
                                "incident_id": {
                                    "type": "string",
                                    "description": "Related incident identifier (optional for create of rollback_requests or change_requests)"
                                },
                                "title": {
                                    "type": "string",
                                    "description": "Title of the change or rollback (required for create, cannot be empty)"
                                },
                                "change_type": {
                                    "type": "string",
                                    "description": "Type of change (required for create of change_requests). Must be one of: standard, normal, emergency",
                                    "enum": ["standard", "normal", "emergency"]
                                },
                                "risk_level": {
                                    "type": "string",
                                    "description": "Risk level of the change (required for create of change_requests). Must be one of: low, medium, high, critical",
                                    "enum": ["low", "medium", "high", "critical"]
                                },
                                "description": {
                                    "type": "string",
                                    "description": "Description of the change (required for create of change_requests, cannot be empty)"
                                },
                                "requested_by": {
                                    "type": "string",
                                    "description": "User identifier requesting the change or rollback (required for create, must exist in system)"
                                },
                                "approved_by": {
                                    "type": "string",
                                    "description": "User identifier approving the change (optional, must exist in system if provided)"
                                },
                                "status": {
                                    "type": "string",
                                    "description": "Status of the change or rollback (required for create). For change_requests: requested, approved, denied, scheduled, implemented, cancelled, rolled_back. For rollback_requests: requested, approved, executed, failed"
                                },
                                "implementation_date": {
                                    "type": "string",
                                    "description": "Implementation timestamp in YYYY-MM-DDTHH:MM:SS format (for change_requests)"
                                },
                                "rollback_reason": {
                                    "type": "string",
                                    "description": "Reason for rollback (required for create of rollback_requests, cannot be empty)"
                                },
                                "executed_at": {
                                    "type": "string",
                                    "description": "Execution timestamp in YYYY-MM-DDTHH:MM:SS format (for rollback_requests)"
                                }
                            }
                        },
                        "change_id": {
                            "type": "string",
                            "description": "Unique identifier of the change request (required for update of change_requests)"
                        },
                        "rollback_id": {
                            "type": "string",
                            "description": "Unique identifier of the rollback request (required for update of rollback_requests)"
                        }
                    },
                    "required": ["entity_type", "action"]
                }
            }
        }
