import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class HandleImprovements(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, action: str, improvement_data: Dict[str, Any] = None, rca_id: str = None, review_id: str = None) -> str:
        """
        Create or update root cause analysis records or post incident review records.

        Entity Types:
        - root_cause_analyses
        - post_incident_reviews
        
        Actions:
        - create: Create new RCA or new PIR
        - update: Update existing RCA (requires rca_id and fields to update) or PIR (requires review_id and fields to update)
        """
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        def generate_rca_number(rca_id: int) -> str:
            return f"RCA{str(rca_id).zfill(7)}"
        
        if entity_type not in ["root_cause_analyses", "post_incident_reviews"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'root_cause_analyses' or 'post_incident_reviews'"
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
        
        # get existing data tables
        root_cause_analyses = data.get("root_cause_analyses", {})
        post_incident_reviews = data.get("post_incident_reviews", {})
        incidents = data.get("incidents", {})
        problem_tickets = data.get("problem_tickets", {}) # Added for problem_ticket_id validation
        users = data.get("users", {})

        # allowed enums
        valid_methods = ["5_whys", "fishbone", "timeline", "fault_tree", "kepner_tregoe"]
        valid_statuses = ["assigned", "in_progress", "completed", "approved"]
        valid_pir_statuses = ["scheduled", "completed", "cancelled"]

        # valid values
        required_incident_statuses = ["resolved", "closed"]
        required_incident_statuses_pir = ["closed"]
        required_incident_severity = ["P1", "P2"]
        required_user_status = ["active"]
        

        # Handle root_cause_analyses
        if entity_type == "root_cause_analyses":
            # for create action
            if action == "create":
                if not improvement_data:
                    return json.dumps({
                        "success": False,
                        "error": "improvement_data is required for create action"
                    })

                # Validate required fields
                required_fields = ["rca_title", "assigned_to", "due_date", "reported_by", "analysis_method"]

                missing_fields = [field for field in required_fields if field not in improvement_data]
                if missing_fields:
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: Missing required fields for create action: {', '.join(missing_fields)}"
                    })
                
                # Validate non-empty required fields
                for field in required_fields:
                    if not improvement_data[field] or str(improvement_data[field]).strip() == "":
                        return json.dumps({
                            "success": False,
                            "error": f"Field '{field}' cannot be empty"
                        })
                
                # Validate incident_id OR problem_ticket_id
                incident_id = improvement_data.get("incident_id") # Changed from associated_incident_id
                problem_ticket_id = improvement_data.get("problem_ticket_id")

                if not incident_id and not problem_ticket_id:
                    return json.dumps({
                        "success": False,
                        "error": "Halt: Either 'incident_id' or 'problem_ticket_id' must be provided"
                    })
                if incident_id and problem_ticket_id:
                     return json.dumps({
                        "success": False,
                        "error": "Halt: Only one of 'incident_id' or 'problem_ticket_id' can be provided, not both"
                    })

                # Validate incident exists if provided
                if incident_id:
                    if str(incident_id) not in incidents:
                        return json.dumps({
                            "success": False,
                            "error": "Halt: Incident not found"
                        })
                    # Validate that incident status is resolved or closed
                    incident_status = incidents[str(incident_id)]["status"]
                    if incident_status not in required_incident_statuses:
                        return json.dumps({
                            "success": False,
                            "error": f"Halt: Incident status must be one of: {', '.join(required_incident_statuses)}"
                        })
                    # Validate that incident severity is P1 or P2
                    incident_severity = incidents[str(incident_id)]["severity"]
                    if incident_severity not in required_incident_severity:
                        return json.dumps({
                            "success": False,
                            "error": f"Halt: Incident severity must be one of: {', '.join(required_incident_severity)}"
                        })
                
                # Validate problem ticket exists if provided
                if problem_ticket_id:
                    if str(problem_ticket_id) not in problem_tickets:
                        return json.dumps({
                            "success": False,
                            "error": "Halt: Problem ticket not found"
                        })

                # Allowed fields
                allowed_fields = ["incident_id", "problem_ticket_id", "rca_title", "assigned_to", "due_date", "reported_by", "analysis_method", "root_cause_summary", "status"]

                rca_fields = [field for field in improvement_data if field not in allowed_fields]
                if rca_fields:
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: Unrecognized fields in improvement_data: {', '.join(rca_fields)}"
                    })
                
                # Validate that assigned_to user exists
                if str(improvement_data["assigned_to"]) not in users:
                    return json.dumps({
                        "success": False,
                        "error": "Halt: User assigned_to not found"
                    })
                
                # Validate that assigned_to user is active
                if users[str(improvement_data["assigned_to"])]["status"] not in required_user_status: 
                    return json.dumps({ 
                        "success": False, 
                        "error": "Halt: User assigned_to must be active" 
                    })
                
                # Validate that reported_by user exists
                if str(improvement_data["reported_by"]) not in users:
                    return json.dumps({
                        "success": False,
                        "error": "Halt: User reported_by not found"
                    })
                
                # Validate that reported_by user is active
                if users[str(improvement_data["reported_by"])]["status"] not in required_user_status: 
                    return json.dumps({ 
                        "success": False, 
                        "error": "Halt: User reported_by must be active" 
                    })
                
                # Validate analysis_method if provided
                analysis_method = improvement_data.get("analysis_method")
                if analysis_method and analysis_method not in valid_methods:
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: Invalid analysis method - must be one of: {', '.join(valid_methods)}"
                    })
                
                # Validate optional fields are not empty if provided
                optional_fields = ["root_cause_summary"]
                for field in optional_fields:
                    if field in improvement_data and improvement_data[field] is not None:
                        if str(improvement_data[field]).strip() == "":
                            return json.dumps({
                                "success": False,
                                "error": f"Field '{field}' cannot be empty if provided"
                            })
                
                # Validate status
                status = improvement_data.get("status", "assigned")
                if status not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: Invalid status - must be one of: {', '.join(valid_statuses)}"
                    })
                
                # Generate new RCA ID
                new_rca_id = generate_id(root_cause_analyses)
                rca_number = generate_rca_number(new_rca_id)
                
                # Create new RCA record
                new_rca = {
                    "rca_id": str(new_rca_id),
                    "rca_number": str(rca_number),
                    "incident_id": str(incident_id) if incident_id else None, # Changed from associated_incident_id
                    "problem_ticket_id": str(problem_ticket_id) if problem_ticket_id else None,
                    "rca_title": improvement_data["rca_title"],
                    "assigned_to": str(improvement_data["assigned_to"]),
                    "due_date": improvement_data["due_date"],
                    "analysis_method": improvement_data["analysis_method"],
                    "root_cause_summary": improvement_data["root_cause_summary"] if improvement_data.get("root_cause_summary") not in (None, "") else None,
                    "status": status,
                    "completed_at": None,
                    "approved_by": None,
                    "reported_by": str(improvement_data["reported_by"]),
                    "created_at": "2025-10-07T12:00:00",
                    "updated_at": "2025-10-07T12:00:00"
                }
                
                root_cause_analyses[str(new_rca_id)] = new_rca
                
                return json.dumps({
                    "success": True,
                    "action": "create",
                    "rca_id": str(new_rca_id),
                    "message": f"RCA {new_rca_id} created successfully",
                    "improvement_data": new_rca
                })
            
            # for update action
            elif action == "update":
                if not rca_id:
                    return json.dumps({
                        "success": False,
                        "error": "rca_id is required for update action"
                    })
                
                if str(rca_id) not in root_cause_analyses:
                    return json.dumps({
                        "success": False,
                        "error": "Halt: RCA not found"
                    })
                
                if not improvement_data:
                    return json.dumps({
                        "success": False,
                        "error": "improvement_data is required for update action"
                    })
                
                # Validate at least one optional field is provided
                update_fields = ["incident_id", "problem_ticket_id", "rca_title", "assigned_to", "analysis_method", "root_cause_summary", "status", "due_date", "completed_at", "approved_by"]

                provided_fields = [field for field in update_fields if field in improvement_data]
                if not provided_fields:
                    return json.dumps({
                        "success": False,
                        "error": f"At least one optional field must be provided for updates {', '.join(update_fields)}"
                    })
                
                # Validate only allowed fields for updates
                invalid_fields = [field for field in improvement_data.keys() if field not in update_fields]
                if invalid_fields:
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: Invalid fields for RCA updating: {', '.join(invalid_fields)}"
                    })
                
                # Validate non-empty fields
                for field, value in improvement_data.items():
                    if field not in ["incident_id", "problem_ticket_id", "analysis_method", "root_cause_summary", "completed_at", "approved_by"] and value is not None and str(value).strip() == "":
                        return json.dumps({
                            "success": False,
                            "error": f"Field '{field}' cannot be empty"
                        })
                    elif field in ["incident_id", "problem_ticket_id", "analysis_method", "root_cause_summary", "completed_at", "approved_by"] and value is not None and str(value).strip() == "":
                        return json.dumps({
                            "success": False,
                            "error": f"Field '{field}' cannot be empty if provided"
                        })
                
                # Validate incident_id OR problem_ticket_id if either is provided
                incident_id_update = improvement_data.get("incident_id")
                problem_ticket_id_update = improvement_data.get("problem_ticket_id")

                if incident_id_update is not None and problem_ticket_id_update is not None:
                    return json.dumps({
                        "success": False,
                        "error": "Halt: Only one of 'incident_id' or 'problem_ticket_id' can be provided, not both"
                    })
                
                # If both are provided as None, it means the user wants to clear both, which is not allowed.
                current_incident_id = root_cause_analyses[str(rca_id)].get("incident_id")
                current_problem_ticket_id = root_cause_analyses[str(rca_id)].get("problem_ticket_id")

                final_incident_id = incident_id_update if "incident_id" in improvement_data else current_incident_id
                final_problem_ticket_id = problem_ticket_id_update if "problem_ticket_id" in improvement_data else current_problem_ticket_id

                if not final_incident_id and not final_problem_ticket_id:
                    return json.dumps({
                        "success": False,
                        "error": "Halt: Either 'incident_id' or 'problem_ticket_id' must be provided and not null"
                    })

                # Validate incident exists if provided
                if incident_id_update:
                    if str(incident_id_update) not in incidents:
                        return json.dumps({
                            "success": False,
                            "error": "Halt: Incident not found"
                        })
                    # Validate that incident status is resolved or closed
                    incident_status = incidents[str(incident_id_update)]["status"]
                    if incident_status not in required_incident_statuses:
                        return json.dumps({
                            "success": False,
                            "error": f"Halt: Incident status must be one of: {', '.join(required_incident_statuses)}"
                        })
                    # Validate that incident severity is P1 or P2
                    incident_severity = incidents[str(incident_id_update)]["severity"]
                    if incident_severity not in required_incident_severity:
                        return json.dumps({
                            "success": False,
                            "error": f"Halt: Incident severity must be one of: {', '.join(required_incident_severity)}"
                        })
                
                # Validate problem ticket exists if provided
                if problem_ticket_id_update:
                    if str(problem_ticket_id_update) not in problem_tickets:
                        return json.dumps({
                            "success": False,
                            "error": "Halt: Problem ticket not found"
                        })

                if "assigned_to" in improvement_data:
                    # Validate that assigned_to user exists if provided
                    if str(improvement_data["assigned_to"]) not in users:
                        return json.dumps({
                            "success": False,
                            "error": "Halt: User assigned_to not found"
                        })

                    # Validate that assigned_to user is active if provided
                    if users[str(improvement_data["assigned_to"])]["status"] not in required_user_status: 
                        return json.dumps({ 
                            "success": False, 
                            "error": "Halt: User assigned_to must be active" 
                        })
                    
                # Validate analysis_method if provided
                if "analysis_method" in improvement_data:
                    if improvement_data["analysis_method"] not in valid_methods:
                        return json.dumps({
                            "success": False,
                            "error": f"Halt: Invalid analysis method - must be one of: {', '.join(valid_methods)}"
                        })
                
                # Validate status if provided
                status = improvement_data.get("status")
                if status and status not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: Invalid status - must be one of: {', '.join(valid_statuses)}"
                    })
                
                approved_by = improvement_data.get("approved_by")
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
                for key, value in improvement_data.items():
                    if key in ["incident_id", "problem_ticket_id", "analysis_method", "root_cause_summary", "completed_at", "approved_by"]:
                        updated_rca[key] = str(value) if value not in (None, "") else None
                    elif key == "assigned_to":
                        updated_rca[key] = str(value)
                    else:
                        updated_rca[key] = value
                
                updated_rca["updated_at"] = "2025-10-07T12:00:00"

                root_cause_analyses[str(rca_id)] = updated_rca
                
                return json.dumps({
                    "success": True,
                    "action": "update",
                    "rca_id": str(rca_id),
                    "message": f"RCA {rca_id} updated successfully",
                    "improvement_data": updated_rca
                })
        
        # Handle post_incident_reviews
        elif entity_type == "post_incident_reviews":
            # for create action
            if action == "create":
                if not improvement_data:
                    return json.dumps({
                        "success": False,
                        "error": "improvement_data is required for create action"
                    })
                
                # Validate required fields for create
                required_fields = ["incident_id", "scheduled_date", "facilitator", "review_notes", "lessons_learned", "action_items", "created_by"]
                
                missing_fields = [field for field in required_fields if field not in improvement_data]
                if missing_fields:
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: Missing required fields for create action: {', '.join(missing_fields)}"
                    })
                
                # Validate non-empty required fields
                for field in required_fields:
                    if not improvement_data[field] or str(improvement_data[field]).strip() == "":
                        return json.dumps({
                            "success": False,
                            "error": f"Field '{field}' cannot be empty"
                        })
                
                # Allowed fields
                allowed_fields = ["incident_id", "scheduled_date", "facilitator", "review_notes", "lessons_learned", "action_items", "status", "created_by"]

                pir_fields = [field for field in improvement_data if field not in allowed_fields]
                if pir_fields:
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: Unrecognized fields in improvement_data: {', '.join(pir_fields)}"
                    })
                
                # Validate that incident exists
                if str(improvement_data["incident_id"]) not in incidents:
                        return json.dumps({
                            "success": False,
                            "error": "Halt: Incident not found"
                        })
                
                # Validate that incident status is closed
                incident_status = incidents[str(improvement_data["incident_id"])]["status"]
                if incident_status not in required_incident_statuses_pir:
                    return json.dumps({
                        "success": False,
                        "error": "Halt: Incident status must be closed"
                    })
                
                # Validate facilitator user exists
                if str(improvement_data["facilitator"]) not in users:
                    return json.dumps({
                        "success": False,
                        "error": "Halt: User 'facilitator' not found"
                    })
                
                # Validate that facilitator user is active
                if users[str(improvement_data["facilitator"])]["status"] != "active":
                    return json.dumps({
                        "success": False,
                        "error": "Halt: User 'facilitator' must be active"
                    })
                
                # Validate status enum
                status = improvement_data.get("status", "scheduled")
                if status not in valid_pir_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: Invalid pir status - must be one of: {', '.join(valid_pir_statuses)}"
                    })
                
                # Validate created_by user exists
                if str(improvement_data["created_by"]) not in users:
                    return json.dumps({
                        "success": False,
                        "error": "Halt: User 'created_by' not found"
                    })
                
                # Validate that created_by user is active
                if users[str(improvement_data["created_by"])]["status"] != "active":
                    return json.dumps({
                        "success": False,
                        "error": "Halt: User 'created_by' must be active"
                    })
                
                # Generate new PIR ID
                new_pir_id = generate_id(post_incident_reviews)

                # Create new pir record
                new_pir = {
                    "review_id": str(new_pir_id),
                    "incident_id": str(improvement_data["incident_id"]),
                    "scheduled_date": improvement_data["scheduled_date"],
                    "facilitator": str(improvement_data["facilitator"]),
                    "review_notes": improvement_data["review_notes"],
                    "lessons_learned": improvement_data["lessons_learned"],
                    "action_items": improvement_data["action_items"],
                    "status": status,
                    "created_by": str(improvement_data["created_by"]),
                    "created_at": "2025-10-07T12:00:00"
                }

                post_incident_reviews[str(new_pir_id)] = new_pir

                return json.dumps({
                    "success": True,
                    "action": "create",
                    "review_id": str(new_pir_id),
                    "message": f"Post incident review {new_pir_id} created successfully",
                    "improvement_data": new_pir
                })
            
            # for update action
            elif action == "update":
                if not review_id:
                    return json.dumps({
                        "success": False,
                        "error": "review_id is required for update action"
                    })
                
                if str(review_id) not in post_incident_reviews:
                    return json.dumps({
                        "success": False,
                        "error": "Halt: Post incident review not found"
                    })
                
                if not improvement_data:
                    return json.dumps({
                        "success": False,
                        "error": "improvement_data is required for update action"
                    })
                
                # Validate at least one optional field is provided
                update_fields = ["incident_id", "scheduled_date", "facilitator", "review_notes", "lessons_learned", "action_items", "status"]

                provided_fields = [field for field in update_fields if field in improvement_data]
                if not provided_fields:
                    return json.dumps({
                        "success": False,
                        "error": f"At least one optional field must be provided for updates {', '.join(update_fields)}"
                    })
                
                # Validate only allowed fields for updates
                invalid_fields = [field for field in improvement_data.keys() if field not in update_fields]
                if invalid_fields:
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: Invalid fields for pir updating: {', '.join(invalid_fields)}"
                    })
                
                # Validate non-empty fields
                for field, value in improvement_data.items():
                    if value is not None and str(value).strip() == "":
                        return json.dumps({
                            "success": False,
                            "error": f"Field '{field}' cannot be empty"
                        })
                    
                if "facilitator" in improvement_data:
                    if str(improvement_data["facilitator"]) not in users:
                        return json.dumps({
                            "success": False,
                            "error": "Halt: User 'facilitator' not found"
                        })
                    
                    if users[str(improvement_data["facilitator"])]["status"] != "active":
                        return json.dumps({
                            "success": False,
                            "error": "Halt: User 'facilitator' must be active"
                        })
                    
                if "status" in improvement_data:
                    if improvement_data["status"] not in valid_pir_statuses:
                        return json.dumps({
                            "success": False,
                            "error": f"Halt: Invalid status. Must be one of: {', '.join(valid_pir_statuses)}"
                        })
                    
                # Get current PIR record
                current_pir = post_incident_reviews[str(review_id)]
                # Update PIR record with modified information
                updated_pir = current_pir.copy()
                for key, value in improvement_data.items():
                    if key == "facilitator":
                        updated_pir[key] = str(value)
                    else:
                        updated_pir[key] = value

                post_incident_reviews[str(review_id)] = updated_pir

                return json.dumps({
                    "success": True,
                    "action": "update",
                    "review_id": str(review_id),
                    "message": f"Post incident review {review_id} updated successfully",
                    "improvement_data": updated_pir
                })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "handle_improvements",
                "description": "Create or update root cause analysis or post incident review records in the incident management system. For root cause analyses, manages RCA workflow including assignment, analysis methods, and approval processes. For post incident reviews, handles review scheduling, facilitation, and documentation of lessons learned. For RCAs, either incident_id or problem_ticket_id must be provided, but not both.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Entity type to manage: 'root_cause_analyses' for root cause analyses, 'post_incident_reviews' for post incident reviews"
                        },
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' to create new record, 'update' to modify existing record"
                        },
                        "improvement_data": {
                            "type": "object",
                            "description": "Improvement data object containing fields for creating or updating RCA or PIR records",
                            "properties": {
                                "incident_id": { # Renamed from associated_incident_id
                                    "type": "string",
                                    "description": "Related incident identifier for RCA (required for RCA create if problem_ticket_id is not provided, cannot be empty, must exist and be resolved/closed with P1/P2 severity). Can be set to null for update if problem_ticket_id is provided."
                                },
                                "problem_ticket_id": {
                                    "type": "string",
                                    "description": "Related problem ticket identifier for RCA (required for RCA create if incident_id is not provided, cannot be empty, must exist). Can be set to null for update if incident_id is provided."
                                },
                                "rca_title": {
                                    "type": "string",
                                    "description": "Title of the root cause analysis (required for RCA create, cannot be empty)"
                                },
                                "assigned_to": {
                                    "type": "string",
                                    "description": "User identifier assigned to conduct the analysis (required for RCA create, cannot be empty, must be active user)"
                                },
                                "due_date": {
                                    "type": "string",
                                    "description": "Date by which analysis should be completed (required for RCA create, cannot be empty)"
                                },
                                "reported_by": {
                                    "type": "string",
                                    "description": "User identifier who reported the need for RCA (required for RCA create, cannot be empty, must be active user)"
                                },
                                "analysis_method": {
                                    "type": "string",
                                    "description": "Analysis methodology used (required for RCA create). Must be one of: 5_whys, fishbone, timeline, fault_tree, kepner_tregoe"                                },
                                "root_cause_summary": {
                                    "type": "string",
                                    "description": "Summary of identified root cause (optional for RCA, cannot be empty if provided)"
                                },
                                "status": {
                                    "type": "string",
                                    "description": "Status (optional, defaults based on entity type). For RCA: assigned, in_progress, completed, approved. For PIR: scheduled, completed, cancelled"
                                },
                                "completed_at": {
                                    "type": "string",
                                    "description": "Timestamp when analysis was completed (optional for RCA, cannot be empty if provided)"
                                },
                                "approved_by": {
                                    "type": "string",
                                    "description": "User identifier who approved the analysis (optional for RCA, required when status is approved, must be active user)"
                                },
                                "scheduled_date": {
                                    "type": "string",
                                    "description": "Date for the post-incident review (required for PIR create, cannot be empty)"
                                },
                                "facilitator": {
                                    "type": "string",
                                    "description": "User who will facilitate the review (required for PIR create, cannot be empty, must be active user)"
                                },
                                "review_notes": {
                                    "type": "string",
                                    "description": "Notes for the review (required for PIR create, cannot be empty)"
                                },
                                "lessons_learned": {
                                    "type": "string",
                                    "description": "Lessons learned from the incident (required for PIR create, cannot be empty)"
                                },
                                "action_items": {
                                    "type": "string",
                                    "description": "Action items identified (required for PIR create, cannot be empty)"
                                },
                                "created_by": {
                                    "type": "string",
                                    "description": "User identifier who created the post incident review (required for PIR create, cannot be empty, must be active user)"
                                }
                            }
                        },
                        "rca_id": {
                            "type": "string",
                            "description": "Unique identifier of the RCA. Required for RCA update action only."
                        },
                        "review_id": {
                            "type": "string",
                            "description": "Unique identifier of the PIR. Required for PIR update action only."
                        }
                    },
                    "required": ["entity_type", "action"]
                }
            }
        }