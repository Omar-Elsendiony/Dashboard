import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ManageRootCauseAnalyses(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, rca_data: Dict[str, Any] = None, rca_id: str = None) -> str:
        """
        Conduct (create) or update root cause analysis records.
        
        Actions:
        - conduct: Create new RCA (requires incident_id, rca_title, assigned_to, due_date, status)
        - update: Update existing RCA (requires rca_id and fields to update)
        """
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        def generate_rca_number(rca_id: int) -> str:
            return f"RCA{str(rca_id).zfill(7)}"
        
        if action not in ["conduct", "update"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid action '{action}'. Must be 'conduct' or 'update'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format"
            })
        
        # get existing data tables
        root_cause_analyses = data.get("root_cause_analyses", {})
        incidents = data.get("incidents", {})
        users = data.get("users", {})

        # allowed enums
        valid_methods = ["5_whys", "fishbone", "timeline", "fault_tree", "kepner_tregoe"]
        valid_statuses = ["assigned", "in_progress", "completed", "approved"]

        # allowed values
        required_incident_statuses = ["resolved", "closed"]
        required_incident_severity = ["P1", "P2"]
        required_user_status = ["active"]
        

        # for conduct action
        if action == "conduct":
            if not rca_data:
                return json.dumps({
                    "success": False,
                    "error": "rca_data is required for conduct action"
                })

            # Validate required fields
            required_fields = ["incident_id", "rca_title", "assigned_to", "due_date"]

            missing_fields = [field for field in required_fields if field not in rca_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Missing required fields for conduct action: {', '.join(missing_fields)}"
                })
            
            # Allowed fields
            allowed_fields = ["rca_title", "incident_id", "assigned_to", "analysis_method", "root_cause_summary", "status", "due_date"]

            rca_fields = [field for field in rca_data if field not in allowed_fields]
            if rca_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Unrecognized fields in rca_data: {', '.join(rca_fields)}"
                })
            
            # Validate that incident exists
            if str(rca_data["incident_id"]) not in incidents:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Incident not found"
                })
            
            # Validate that incident status is resolved or closed
            incident_status = incidents[str(rca_data["incident_id"])]["status"]
            if incident_status not in required_incident_statuses:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Incident status must be one of: {', '.join(required_incident_statuses)}"
                })
            
            # Validate that incident severity is P1 or P2
            incident_severity = incidents[str(rca_data["incident_id"])]["severity"]
            if incident_severity not in required_incident_severity:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Incident severity must be one of: {', '.join(required_incident_severity)}"
                })
            
            # Validate that assigned_to user exists
            if str(rca_data["assigned_to"]) not in users:
                return json.dumps({
                    "success": False,
                    "error": "Halt: User assigned_to not found"
                })
            
            # Validate that assigned_to user is active
            if users[str(rca_data["assigned_to"])]["status"] not in required_user_status: 
                return json.dumps({ 
                    "success": False, 
                    "error": "Halt: User assigned_to must be active" 
                })
            
            # Validate rca_title is not empty
            title = rca_data.get("rca_title")
            if not title or not title.strip():  
                return json.dumps({
                    "success": False,
                    "error": "Halt: rca_title cannot be empty"
                })
            
            # Validate status
            status = rca_data.get("status", "assigned")
            if status not in valid_statuses:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Invalid status - must be one of: {', '.join(valid_statuses)}"
                })
            
            # Validate analysis_method if provided
            analysis_method = rca_data.get("analysis_method")
            if analysis_method and analysis_method not in valid_methods:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Invalid analysis method - must be one of: {', '.join(valid_methods)}"
                })
            
            # Generate new RCA ID
            new_rca_id = generate_id(root_cause_analyses)
            rca_number = generate_rca_number(new_rca_id)
            
            # Create new RCA record
            new_rca = {
                "rca_id": str(new_rca_id),
                "rca_number": str(rca_number),
                "rca_title": rca_data["rca_title"],
                "incident_id": str(rca_data["incident_id"]),
                "assigned_to": str(rca_data["assigned_to"]),
                "analysis_method": analysis_method if analysis_method else None,
                "root_cause_summary": rca_data["root_cause_summary"] if "root_cause_summary" in rca_data else None,
                "status": status,
                "due_date": rca_data["due_date"],
                "completed_at": rca_data["completed_at"] if "completed_at" in rca_data else None,
                "approved_by": str(rca_data["approved_by"]) if "approved_by" in rca_data else None,
                "created_at": "2025-10-07T00:00:00",
                "updated_at": "2025-10-07T00:00:00"
            }
            
            root_cause_analyses[str(new_rca_id)] = new_rca
            
            return json.dumps({
                "success": True,
                "action": "conduct",
                "rca_id": str(new_rca_id),
                "message": f"RCA {new_rca_id} created successfully",
                "rca_data": new_rca
            })
        

        # for update action
        elif action == "update":
            if not rca_id:
                return json.dumps({
                    "success": False,
                    "error": "Halt: rca_id is required for update action"
                })
            
            if str(rca_id) not in root_cause_analyses:
                return json.dumps({
                    "success": False,
                    "error": "Halt: RCA not found"
                })
            
            if not rca_data:
                return json.dumps({
                    "success": False,
                    "error": "rca_data is required for conduct action"
                })
            
            # Validate at least one optional field is provided
            update_fields = ["rca_title", "assigned_to", "analysis_method", "root_cause_summary", "status", "due_date", "completed_at", "approved_by"]

            provided_fields = [field for field in update_fields if field in rca_data]
            if not provided_fields:
                return json.dumps({
                    "success": False,
                    "error": f"At least one optional field must be provided for updates {', '.join(update_fields)}"
                })
            
            # Validate only allowed fields for updates
            invalid_fields = [field for field in rca_data.keys() if field not in update_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for RCA updating: {', '.join(invalid_fields)}"
                })
            
            # Validate rca_title is not empty if provided
            if "rca_title" in rca_data:
                if not str(rca_data["rca_title"]).strip():  
                    return json.dumps({
                        "success": False,
                        "error": "Halt: rca_title cannot be empty"
                    })
            
            if "assigned_to" in rca_data:
                # Validate that assigned_to user exists if provided
                if str(rca_data["assigned_to"]) not in users:
                    return json.dumps({
                        "success": False,
                        "error": "Halt: User assigned_to not found"
                    })

                # Validate that assigned_to user is active if provided
                if users[str(rca_data["assigned_to"])]["status"] not in required_user_status: 
                    return json.dumps({ 
                        "success": False, 
                        "error": "Halt: User assigned_to must be active" 
                    })
            
            # Validate analysis_method if provided
            analysis_method = rca_data.get("analysis_method")
            if analysis_method and analysis_method not in valid_methods:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Invalid analysis method - must be one of: {', '.join(valid_methods)}"
                })
            
            # Validate status if provided
            status = rca_data.get("status")
            if status and status not in valid_statuses:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Invalid status - must be one of: {', '.join(valid_statuses)}"
                })
            
            approved_by = rca_data.get("approved_by")
            if approved_by:  
                # Validate that approved_by user exists if provided
                if str(approved_by) not in users:
                    return json.dumps({
                        "success": False,
                        "error": "Halt: User approved_by not found"
                    })
            
                # Validate that approved_by user is active if provided
                if users[str(approved_by)]["status"] not in required_user_status: 
                    return json.dumps({ 
                        "success": False, 
                        "error": "Halt: User approved_by must be active" 
                    })
            
            # If status is approved, approved_by is required
            if status == "approved" and not approved_by:
                return json.dumps({
                    "success": False,
                    "error": "Halt: approved_by is required when status is approved"
                })
            
            # Get current RCA record
            current_rca = root_cause_analyses[str(rca_id)]
            # Update RCA record with modified information
            updated_rca = current_rca.copy()
            for key, value in rca_data.items():
                if key in ["analysis_method", "root_cause_summary", "completed_at", "approved_by"]:
                    updated_rca[key] = str(value) if value not in (None, "") else None
                else:
                    updated_rca[key] = value
            
            updated_rca["updated_at"] = "2025-10-07T00:00:00"

            root_cause_analyses[str(rca_id)] = updated_rca
            
            return json.dumps({
                "success": True,
                "action": "update",
                "rca_id": str(rca_id),
                "message": f"RCA {rca_id} updated successfully",
                "rca_data": updated_rca
            })
        
        
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manage_root_cause_analyses",
                "description": "Conduct or update root cause analysis records in the incident management system. This tool manages RCA lifecycle including creation, progress tracking, and completion. For Conducting: establishes new RCA with incident linkage, analyst assignment, and due date. For updates: modifies RCA details, status transitions, and approval tracking. Validates incident/user existence, enforces status transitions (assigned, in_progress, completed, approved), validates analysis methods, and ensures approval requirements. Essential for post-incident investigation, continuous improvement, and compliance with ITIL best practices.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'conduct' to establish new RCA, 'update' to modify existing RCA",
                            "enum": ["conduct", "update"]
                        },
                        "rca_data": {
                            "type": "object",
                            "description": "Data for conducting or updating the RCA record",
                            "properties": {
                                "rca_title": {
                                    "type": "string",
                                    "description": "Title of the root cause analysis (required for conduct)"
                                },
                                "incident_id": {
                                    "type": "string",
                                    "description": "Related incident identifier (required for conduct)"
                                },
                                "assigned_to": {
                                    "type": "string",
                                    "description": "User identifier conducting the analysis (required for conduct, must exist in system)"
                                },
                                "due_date": {
                                    "type": "string",
                                    "description": "Date by which analysis should be completed in YYYY-MM-DD format (required for conduct)"
                                },
                                "analysis_method": {
                                    "type": "string",
                                    "description": "Analysis methodology used (optional for conduct): 5_whys, fishbone, timeline, fault_tree, kepner_tregoe",
                                    "enum": ["5_whys", "fishbone", "timeline", "fault_tree", "kepner_tregoe"]
                                },
                                "root_cause_summary": {
                                    "type": "string",
                                    "description": "Summary of identified root cause (optional for conduct)"
                                },
                                "status": {
                                    "type": "string",
                                    "description": "RCA status (optional for conduct): assigned, in_progress, completed, approved",
                                    "enum": ["assigned", "in_progress", "completed", "approved"]
                                },
                                "completed_at": {
                                    "type": "string",
                                    "description": "Timestamp when analysis was completed in YYYY-MM-DDTHH:MM:SS format"
                                },
                                "approved_by": {
                                    "type": "string",
                                    "description": "User identifier who approved the analysis (required when status is approved)"
                                }
                            }
                        },
                        "rca_id": {
                            "type": "string",
                            "description": "Unique identifier of the RCA (required for update action)"
                        }
                    },
                    "required": ["action"]
                }
            }
        }
