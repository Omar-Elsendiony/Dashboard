import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class ManageEmployeeTraining(Tool):
    """
    Manages employee training records, including enrollment and progress tracking.
    """
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        operation: str,
        employee_id: Optional[str] = None,
        program_id: Optional[str] = None,
        enrollment_date: Optional[str] = None,
        training_record_id: Optional[str] = None,
        status: Optional[str] = None,
        completion_date: Optional[str] = None,
        score: Optional[float] = None,
        certificate_issued: Optional[bool] = None,
        expiry_date: Optional[str] = None,
    ) -> str:
        """
        Executes the specified operation (create or update) on employee training records.
        """
        def generate_id(table: Dict[str, Any]) -> str:
            """Generates a new unique ID for a record."""
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        timestamp = "2025-10-01T12:00:00"
        employee_trainings = data.get("employee_training", {})
        employees = data.get("employees", {})
        programs = data.get("training_programs", {})

        if operation == "create":
            if not all([employee_id, program_id, enrollment_date]):
                return json.dumps({"error": "Missing required parameters for create operation."})

            if employee_id not in employees:
                return json.dumps({"error": f"Employee with ID {employee_id} not found."})
            if program_id not in programs:
                return json.dumps({"error": f"Training program with ID {program_id} not found."})

            new_record_id = generate_id(employee_trainings)
            new_record = {
                "training_record_id": new_record_id,
                "employee_id": employee_id,
                "program_id": program_id,
                "enrollment_date": enrollment_date,
                "status": "enrolled",
                "completion_date": None,
                "score": None,
                "certificate_issued": False,
                "expiry_date": None,
                "created_at": timestamp,
                "updated_at": timestamp,
            }
            employee_trainings[new_record_id] = new_record
            return json.dumps(new_record)

        elif operation == "update":
            if not all([training_record_id, status]):
                return json.dumps({"error": "Missing required parameters for update operation."})
            
            if training_record_id not in employee_trainings:
                return json.dumps({"error": f"Training record with ID {training_record_id} not found."})
            
            valid_statuses = ["in_progress", "completed", "failed", "cancelled"]
            if status not in valid_statuses:
                return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}."})

            record_to_update = employee_trainings[training_record_id]
            record_to_update["status"] = status
            if completion_date is not None:
                record_to_update["completion_date"] = completion_date
            if score is not None:
                record_to_update["score"] = score
            if certificate_issued is not None:
                record_to_update["certificate_issued"] = certificate_issued
            if expiry_date is not None:
                record_to_update["expiry_date"] = expiry_date
            
            record_to_update["updated_at"] = timestamp
            return json.dumps(record_to_update)

        else:
            return json.dumps({"error": "Invalid operation. Must be 'create' or 'update'."})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        """
        Returns the schema for the ManageEmployeeTraining tool.
        """
        return {
            "type": "function",
            "function": {
                "name": "manage_employee_training",
                "description": "Handles employee enrollment in training programs (create) and tracks their progress and completion (update).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation": {"type": "string", "description": "Action: 'create' or 'update'."},
                        "employee_id": {"type": "string", "description": "The ID of the employee to be enrolled. Required for 'create'."},
                        "program_id": {"type": "string", "description": "The ID of the training program for enrollment. Required for 'create'."},
                        "enrollment_date": {"type": "string", "description": "The date the employee was enrolled (YYYY-MM-DD). Required for 'create'."},
                        "training_record_id": {"type": "string", "description": "The unique ID of the employee's training record. Required for 'update'."},
                        "status": {"type": "string", "description": "New status: 'in_progress', 'completed', 'failed', 'cancelled'. Required for 'update'."},
                        "completion_date": {"type": "string", "description": "The date the employee completed the training (YYYY-MM-DD). Optional for 'update'."},
                        "score": {"type": "number", "description": "The final score or grade, if applicable. Optional for 'update'."},
                        "certificate_issued": {"type": "boolean", "description": "'True', 'False'. Optional for 'update'."},
                        "expiry_date": {"type": "string", "description": "The expiration date of the certification, if applicable (YYYY-MM-DD). Optional for 'update'."},
                    },
                    "required": ["operation"],
                },
            },
        }
