import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class CreateTrainingProgram(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], program_name: str, program_type: str,
               duration_hours: int, delivery_method: str, description: Optional[str] = None,
               mandatory: bool = False, status: str = 'active') -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        training_programs = data.get("training_programs", {})
        
        # Validate program_type
        valid_program_types = ['onboarding', 'compliance', 'technical', 'leadership', 'safety', 'diversity', 'ai_ethics']
        if program_type not in valid_program_types:
            return json.dumps({"success": False, "error": f"Invalid program_type. Must be one of {valid_program_types}", "halt": True})
        
        # Validate delivery_method
        valid_delivery_methods = ['in_person', 'online', 'hybrid', 'self_paced']
        if delivery_method not in valid_delivery_methods:
            return json.dumps({"success": False, "error": f"Invalid delivery_method. Must be one of {valid_delivery_methods}", "halt": True})
        
        # Validate status
        valid_statuses = ['active', 'inactive', 'draft']
        if status not in valid_statuses:
            return json.dumps({"success": False, "error": f"Invalid status. Must be one of {valid_statuses}", "halt": True})
        
        program_id = generate_id(training_programs)
        timestamp = "2025-10-01T00:00:00"
        
        new_program = {
            "program_id": program_id,
            "program_name": program_name,
            "program_type": program_type,
            "description": description,
            "duration_hours": duration_hours,
            "delivery_method": delivery_method,
            "mandatory": mandatory,
            "status": status,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        training_programs[program_id] = new_program
        return json.dumps({"program_id": program_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_training_program",
                "description": "Create a new training program",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "program_name": {"type": "string", "description": "Program name"},
                        "program_type": {"type": "string", "description": "Program type (onboarding, compliance, technical, leadership, safety, diversity, ai_ethics)"},
                        "duration_hours": {"type": "integer", "description": "Duration in hours"},
                        "delivery_method": {"type": "string", "description": "Delivery method (in_person, online, hybrid, self_paced)"},
                        "description": {"type": "string", "description": "Program description"},
                        "mandatory": {"type": "boolean", "description": "Whether program is mandatory (True/False)"},
                        "status": {"type": "string", "description": "Status (active, inactive, draft), defaults to active"}
                    },
                    "required": ["program_name", "program_type", "duration_hours", "delivery_method"]
                }
            }
        }
