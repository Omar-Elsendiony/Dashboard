import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class HandleRootCauseAnalysis(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, rca_data: Dict[str, Any] = None, rca_id: str = None) -> str:
        """
        Create or update root cause analysis records.
        
        Actions:
        - create: Create new RCA record (requires rca_data with incident_id, analysis_method, conducted_by_id, status)
        - update: Update existing RCA record (requires rca_id and rca_data with changes)
        """
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        if action not in ["create", "update"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid action '{action}'. Must be 'create' or 'update'"
            })
        
        # Access root_cause_analysis data
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for root_cause_analysis"
            })
        
        root_cause_analysis = data.get("root_cause_analysis", {})
        
        if action == "create":
            if not rca_data:
                return json.dumps({
                    "success": False,
                    "error": "rca_data is required for create action"
                })
            
            # Validate required fields for creation
            required_fields = ["incident_id", "analysis_method", "conducted_by_id", "status"]
            missing_fields = [field for field in required_fields if field not in rca_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields for RCA creation: {', '.join(missing_fields)}"
                })
            
            # Validate only allowed fields are present
            allowed_fields = ["incident_id", "analysis_method", "conducted_by_id", "completed_at", "status"]
            invalid_fields = [field for field in rca_data.keys() if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for RCA creation: {', '.join(invalid_fields)}"
                })
            
            # Validate enum fields
            valid_analysis_methods = ["five_whys", "fishbone", "timeline_analysis", "fault_tree"]
            if rca_data["analysis_method"] not in valid_analysis_methods:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid analysis_method '{rca_data['analysis_method']}'. Must be one of: {', '.join(valid_analysis_methods)}"
                })
            
            valid_statuses = ["in_progress", "completed", "approved"]
            if rca_data["status"] not in valid_statuses:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid status '{rca_data['status']}'. Must be one of: {', '.join(valid_statuses)}"
                })
            
            # Check for existing RCA for the same incident
            incident_id = rca_data["incident_id"]
            for existing_rca in root_cause_analysis.values():
                if existing_rca.get("incident_id") == incident_id:
                    return json.dumps({
                        "success": False,
                        "error": f"Root cause analysis already exists for incident {incident_id}"
                    })
            
            # Generate new RCA ID
            new_rca_id = generate_id(root_cause_analysis)
            
            # Create new RCA record
            new_rca = {
                "rca_id": str(new_rca_id),
                "incident_id": str(rca_data["incident_id"]),
                "analysis_method": rca_data["analysis_method"],
                "conducted_by_id": str(rca_data["conducted_by_id"]),
                "completed_at": rca_data.get("completed_at"),
                "status": rca_data["status"],
                "created_at": "2025-10-01T00:00:00"
            }
            
            root_cause_analysis[str(new_rca_id)] = new_rca
            
            return json.dumps({
                "success": True,
                "action": "create",
                "rca_id": str(new_rca_id),
                "rca_data": new_rca
            })
        
        elif action == "update":
            if not rca_id:
                return json.dumps({
                    "success": False,
                    "error": "rca_id is required for update action"
                })
            
            if rca_id not in root_cause_analysis:
                return json.dumps({
                    "success": False,
                    "error": f"Root cause analysis record {rca_id} not found"
                })
            
            if not rca_data:
                return json.dumps({
                    "success": False,
                    "error": "rca_data is required for update action"
                })
            
            # Validate only allowed fields are present for updates
            allowed_update_fields = ["analysis_method", "completed_at", "status"]
            invalid_fields = [field for field in rca_data.keys() if field not in allowed_update_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for RCA update: {', '.join(invalid_fields)}. Cannot update incident_id or conducted_by_id."
                })
            
            # Validate enum fields if provided
            if "analysis_method" in rca_data:
                valid_analysis_methods = ["five_whys", "fishbone", "timeline_analysis", "fault_tree"]
                if rca_data["analysis_method"] not in valid_analysis_methods:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid analysis_method '{rca_data['analysis_method']}'. Must be one of: {', '.join(valid_analysis_methods)}"
                    })
            
            if "status" in rca_data:
                valid_statuses = ["in_progress", "completed", "approved"]
                if rca_data["status"] not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid status '{rca_data['status']}'. Must be one of: {', '.join(valid_statuses)}"
                    })
            
            # Get current RCA data
            current_rca = root_cause_analysis[rca_id].copy()
            
            # Validate status transitions
            current_status = current_rca.get("status")
            new_status = rca_data.get("status")
            
            if new_status and current_status == "approved" and new_status != "approved":
                return json.dumps({
                    "success": False,
                    "error": "Cannot change status from approved to another status"
                })
            
            # If status is being changed to completed, set completed_at if not provided
            if new_status == "completed" and current_status != "completed" and "completed_at" not in rca_data:
                rca_data["completed_at"] = "2025-10-01T00:00:00"
            
            # Update RCA record
            updated_rca = current_rca.copy()
            for key, value in rca_data.items():
                updated_rca[key] = value
            
            root_cause_analysis[rca_id] = updated_rca
            
            return json.dumps({
                "success": True,
                "action": "update",
                "rca_id": str(rca_id),
                "rca_data": updated_rca
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "handle_root_cause_analysis",
                "description": "Create or update root cause analysis records in the incident management system. This tool manages the systematic investigation process to identify underlying causes of incidents and prevent recurrence. For creation, establishes new RCA records with comprehensive validation to ensure proper methodology selection and prevent duplicate analyses for the same incident. For updates, modifies existing RCA records while maintaining data integrity and enforcing proper status transitions. Validates analysis methods and status values according to incident management best practices. Essential for continuous improvement, incident prevention, and organizational learning from operational failures.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' to establish new RCA record, 'update' to modify existing RCA record",
                            "enum": ["create", "update"]
                        },
                        "rca_data": {
                            "type": "object",
                            "description": "Root cause analysis data object. For create: requires incident_id (unique), analysis_method, conducted_by_id, status, with optional completed_at. For update: includes RCA fields to change (incident_id and conducted_by_id cannot be updated). SYNTAX: {\"key\": \"value\"}",
                            "properties": {
                                "incident_id": {
                                    "type": "string",
                                    "description": "Reference to the incident record (required for create only, cannot be updated, must be unique)"
                                },
                                "analysis_method": {
                                    "type": "string",
                                    "description": "Root cause analysis methodology: 'five_whys', 'fishbone', 'timeline_analysis', 'fault_tree'",
                                    "enum": ["five_whys", "fishbone", "timeline_analysis", "fault_tree"]
                                },
                                "conducted_by_id": {
                                    "type": "string",
                                    "description": "User ID who is conducting the analysis (required for create only, cannot be updated)"
                                },
                                "completed_at": {
                                    "type": "string",
                                    "description": "Timestamp when analysis was completed (optional, automatically set when status changes to completed)"
                                },
                                "status": {
                                    "type": "string",
                                    "description": "Current status of the analysis: 'in_progress', 'completed', 'approved' (approved status cannot be changed)",
                                    "enum": ["in_progress", "completed", "approved"]
                                }
                            }
                        },
                        "rca_id": {
                            "type": "string",
                            "description": "Unique identifier of the RCA record (required for update action only)"
                        }
                    },
                    "required": ["action"]
                }
            }
        }
