import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class ManageTrainingPrograms(Tool):
    """
    Manages training programs, including creation and modification.
    """
    
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        operation: str,
        program_id: Optional[str] = None,
        program_name: Optional[str] = None,
        program_type: Optional[str] = None,
        duration_hours: Optional[int] = None,
        delivery_method: Optional[str] = None,
        mandatory: Optional[bool] = None, # Corrected: Default changed from False to None
        status: Optional[str] = None,     # Corrected: Default changed from "active" to None
    ) -> str:
        """
        Executes the specified operation (create or update) on training programs.
        """
        def generate_id(table: Dict[str, Any]) -> str:
            """Generates a new unique ID for a record."""
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        timestamp = "2025-10-01T12:00:00"
        training_programs = data.get("training_programs", {})

        if operation == "create":
            # For 'create', set defaults if not provided
            effective_mandatory = mandatory if mandatory is not None else False
            effective_status = status if status is not None else "active"

            if not all([program_name, program_type, duration_hours, delivery_method]):
                return json.dumps({"error": "Missing required parameters for create operation."})

            valid_types = ["onboarding", "compliance", "technical", "leadership", "safety", "diversity", "ai_ethics"]
            if program_type not in valid_types:
                return json.dumps({"error": f"Invalid program type. Must be one of {valid_types}."})

            valid_methods = ["in_person", "online", "hybrid", "self_paced"]
            if delivery_method not in valid_methods:
                return json.dumps({"error": f"Invalid delivery method. Must be one of {valid_methods}."})
            
            valid_statuses = ["active", "inactive", "draft"]
            if effective_status not in valid_statuses:
                return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}."})

            new_program_id = generate_id(training_programs)
            new_program = {
                "program_id": new_program_id,
                "program_name": program_name,
                "program_type": program_type,
                "duration_hours": duration_hours,
                "delivery_method": delivery_method,
                "mandatory": effective_mandatory,
                "status": effective_status,
                "created_at": timestamp,
                "updated_at": timestamp,
            }
            training_programs[new_program_id] = new_program
            return json.dumps(new_program)

        elif operation == "update":
            if not program_id:
                return json.dumps({"error": "program_id is required for update operation."})
            if program_id not in training_programs:
                return json.dumps({"error": f"Training program with ID {program_id} not found."})

            program_to_update = training_programs[program_id]
            if program_name is not None:
                program_to_update["program_name"] = program_name
            if program_type is not None:
                program_to_update["program_type"] = program_type
            if duration_hours is not None:
                program_to_update["duration_hours"] = duration_hours
            if delivery_method is not None:
                program_to_update["delivery_method"] = delivery_method
            if mandatory is not None:
                program_to_update["mandatory"] = mandatory
            if status is not None:
                program_to_update["status"] = status
            
            program_to_update["updated_at"] = timestamp
            return json.dumps(program_to_update)

        else:
            return json.dumps({"error": "Invalid operation. Must be 'create' or 'update'."})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        """
        Returns the schema for the ManageTrainingPrograms tool.
        """
        return {
            "type": "function",
            "function": {
                "name": "manage_training_programs",
                "description": "Allows for the creation of new corporate training programs and the modification of existing ones.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation": {"type": "string", "description": "Action: 'create' or 'update'."},
                        "program_name": {"type": "string", "description": "The official name of the training program. Required for 'create'."},
                        "program_type": {"type": "string", "description": "'onboarding', 'compliance', 'technical', 'leadership', 'safety', 'diversity', 'ai_ethics'. Required for 'create'."},
                        "duration_hours": {"type": "integer", "description": "Total length in hours. Required for 'create'."},
                        "delivery_method": {"type": "string", "description": "'in_person', 'online', 'hybrid', 'self_paced'. Required for 'create'."},
                        "mandatory": {"type": "boolean", "description": "'True', 'False'. Defaults to false."},
                        "status": {"type": "string", "description": "'active', 'inactive', 'draft'. Defaults to 'active'."},
                        "program_id": {"type": "string", "description": "The ID of the training program to update. Required for 'update'."},
                    },
                    "required": ["operation"],
                },
            },
        }