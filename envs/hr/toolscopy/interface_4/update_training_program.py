import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateTrainingProgram(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], program_id: str, program_name: Optional[str] = None,
               description: Optional[str] = None, duration_hours: Optional[int] = None,
               delivery_method: Optional[str] = None, mandatory: Optional[bool] = None,
               status: Optional[str] = None) -> str:
        
        training_programs = data.get("training_programs", {})
        
        # Validate program exists
        if program_id not in training_programs:
            return json.dumps({"success": False, "error": f"Training program {program_id} not found", "halt": True})
        
        program = training_programs[program_id]
        
        # Validate delivery_method if provided
        if delivery_method is not None:
            valid_delivery_methods = ['in_person', 'online', 'hybrid', 'self_paced']
            if delivery_method not in valid_delivery_methods:
                return json.dumps({"success": False, "error": f"Invalid delivery_method. Must be one of {valid_delivery_methods}", "halt": True})
        
        # Validate status if provided
        if status is not None:
            valid_statuses = ['active', 'inactive', 'draft']
            if status not in valid_statuses:
                return json.dumps({"success": False, "error": f"Invalid status. Must be one of {valid_statuses}", "halt": True})
        
        # Update fields
        if program_name is not None:
            program["program_name"] = program_name
        if description is not None:
            program["description"] = description
        if duration_hours is not None:
            program["duration_hours"] = duration_hours
        if delivery_method is not None:
            program["delivery_method"] = delivery_method
        if mandatory is not None:
            program["mandatory"] = mandatory
        if status is not None:
            program["status"] = status
        
        program["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps({"success": True, "message": "Training program updated"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_training_program",
                "description": "Update an existing training program",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "program_id": {"type": "string", "description": "Program ID"},
                        "program_name": {"type": "string", "description": "Updated program name"},
                        "description": {"type": "string", "description": "Updated description"},
                        "duration_hours": {"type": "integer", "description": "Updated duration in hours"},
                        "delivery_method": {"type": "string", "description": "Updated delivery method (in_person, online, hybrid, self_paced)"},
                        "mandatory": {"type": "boolean", "description": "Updated mandatory flag (True/False)"},
                        "status": {"type": "string", "description": "Updated status (active, inactive, draft)"}
                    },
                    "required": ["program_id"]
                }
            }
        }
