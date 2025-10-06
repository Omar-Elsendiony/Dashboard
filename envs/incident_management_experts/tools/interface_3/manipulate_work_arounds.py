import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ManipulateWorkArounds(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, workaround_data: Dict[str, Any] = None, workaround_id: str = None) -> str:
        """
        Create or update workaround records.
        
        Actions:
        - create: Create new workaround record (requires workaround_data with incident_id, implemented_by_id, effectiveness, status, implemented_at)
        - update: Update existing workaround record (requires workaround_id and workaround_data with changes)
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
        
        # Access workarounds data
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for workarounds"
            })
        
        workarounds = data.get("workarounds", {})
        
        if action == "create":
            if not workaround_data:
                return json.dumps({
                    "success": False,
                    "error": "workaround_data is required for create action"
                })
            
            # Validate required fields for creation
            required_fields = ["incident_id", "implemented_by_id", "effectiveness", "status", "implemented_at"]
            missing_fields = [field for field in required_fields if field not in workaround_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields for workaround creation: {', '.join(missing_fields)}"
                })
            
            # Validate only allowed fields are present
            allowed_fields = ["incident_id", "implemented_by_id", "effectiveness", "status", "implemented_at"]
            invalid_fields = [field for field in workaround_data.keys() if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for workaround creation: {', '.join(invalid_fields)}"
                })
            
            # Validate enum fields
            valid_effectiveness = ["complete", "partial", "minimal"]
            if workaround_data["effectiveness"] not in valid_effectiveness:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid effectiveness '{workaround_data['effectiveness']}'. Must be one of: {', '.join(valid_effectiveness)}"
                })
            
            valid_statuses = ["active", "inactive", "replaced"]
            if workaround_data["status"] not in valid_statuses:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid status '{workaround_data['status']}'. Must be one of: {', '.join(valid_statuses)}"
                })
            
            # Generate new workaround ID
            new_workaround_id = generate_id(workarounds)
            
            # Create new workaround record
            new_workaround = {
                "workaround_id": str(new_workaround_id),
                "incident_id": str(workaround_data["incident_id"]),
                "implemented_by_id": str(workaround_data["implemented_by_id"]),
                "effectiveness": workaround_data["effectiveness"],
                "status": workaround_data["status"],
                "implemented_at": workaround_data["implemented_at"],
                "created_at": "2025-10-01T00:00:00"
            }
            
            workarounds[str(new_workaround_id)] = new_workaround
            
            return json.dumps({
                "success": True,
                "action": "create",
                "workaround_id": str(new_workaround_id),
                "workaround_data": new_workaround
            })
        
        elif action == "update":
            if not workaround_id:
                return json.dumps({
                    "success": False,
                    "error": "workaround_id is required for update action"
                })
            
            if workaround_id not in workarounds:
                return json.dumps({
                    "success": False,
                    "error": f"Workaround record {workaround_id} not found"
                })
            
            if not workaround_data:
                return json.dumps({
                    "success": False,
                    "error": "workaround_data is required for update action"
                })
            
            # Validate only allowed fields are present for updates
            allowed_update_fields = ["effectiveness", "status"]
            invalid_fields = [field for field in workaround_data.keys() if field not in allowed_update_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for workaround update: {', '.join(invalid_fields)}. Cannot update incident_id, implemented_by_id, or implemented_at."
                })
            
            # Validate enum fields if provided
            if "effectiveness" in workaround_data:
                valid_effectiveness = ["complete", "partial", "minimal"]
                if workaround_data["effectiveness"] not in valid_effectiveness:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid effectiveness '{workaround_data['effectiveness']}'. Must be one of: {', '.join(valid_effectiveness)}"
                    })
            
            if "status" in workaround_data:
                valid_statuses = ["active", "inactive", "replaced"]
                if workaround_data["status"] not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid status '{workaround_data['status']}'. Must be one of: {', '.join(valid_statuses)}"
                    })
            
            # Get current workaround data
            current_workaround = workarounds[workaround_id].copy()
            
            # Update workaround record
            updated_workaround = current_workaround.copy()
            for key, value in workaround_data.items():
                updated_workaround[key] = value
            
            workarounds[workaround_id] = updated_workaround
            
            return json.dumps({
                "success": True,
                "action": "update",
                "workaround_id": str(workaround_id),
                "workaround_data": updated_workaround
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manipulate_work_arounds",
                "description": "Create or update workaround records in the incident management system. This tool manages temporary solutions implemented to mitigate incident impact while permanent fixes are being developed. For creation, establishes new workaround records with comprehensive validation to track implementation details and effectiveness. For updates, modifies existing workaround records while maintaining data integrity. Validates effectiveness levels and status values according to incident management best practices. Essential for incident mitigation tracking, solution effectiveness measurement, and operational continuity during incident resolution.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' to establish new workaround record, 'update' to modify existing workaround record",
                            "enum": ["create", "update"]
                        },
                        "workaround_data": {
                            "type": "object",
                            "description": "Workaround data object. For create: requires incident_id, implemented_by_id, effectiveness, status, implemented_at. For update: includes workaround fields to change (incident_id, implemented_by_id, implemented_at cannot be updated). SYNTAX: {\"key\": \"value\"}",
                            "properties": {
                                "incident_id": {
                                    "type": "string",
                                    "description": "Reference to the incident record (required for create only, cannot be updated)"
                                },
                                "implemented_by_id": {
                                    "type": "string",
                                    "description": "User ID who implemented the workaround (required for create only, cannot be updated)"
                                },
                                "effectiveness": {
                                    "type": "string",
                                    "description": "Effectiveness level of the workaround: 'complete', 'partial', 'minimal'",
                                    "enum": ["complete", "partial", "minimal"]
                                },
                                "status": {
                                    "type": "string",
                                    "description": "Current status of the workaround: 'active', 'inactive', 'replaced'",
                                    "enum": ["active", "inactive", "replaced"]
                                },
                                "implemented_at": {
                                    "type": "string",
                                    "description": "Timestamp when workaround was implemented (required for create only, cannot be updated)"
                                }
                            }
                        },
                        "workaround_id": {
                            "type": "string",
                            "description": "Unique identifier of the workaround record (required for update action only)"
                        }
                    },
                    "required": ["action"]
                }
            }
        }
