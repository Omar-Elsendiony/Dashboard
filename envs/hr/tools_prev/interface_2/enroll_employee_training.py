import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class EnrollEmployeeTraining(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], employee_id: str, program_id: str,
               enrollment_date: str, status: str = 'enrolled') -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        employees = data.get("employees", {})
        training_programs = data.get("training_programs", {})
        employee_training = data.get("employee_training", {})
        
        # Validate employee exists
        if employee_id not in employees:
            return json.dumps({"success": False, "error": f"Employee {employee_id} not found", "halt": True})
        
        # Validate training program exists
        if program_id not in training_programs:
            return json.dumps({"success": False, "error": f"Training program {program_id} not found", "halt": True})
        
        # Validate status
        valid_statuses = ['enrolled', 'in_progress', 'completed', 'failed', 'cancelled']
        if status not in valid_statuses:
            return json.dumps({"success": False, "error": f"Invalid status. Must be one of {valid_statuses}", "halt": True})
        
        training_record_id = generate_id(employee_training)
        timestamp = "2025-10-01T00:00:00"
        
        new_training = {
            "training_record_id": training_record_id,
            "employee_id": employee_id,
            "program_id": program_id,
            "enrollment_date": enrollment_date,
            "completion_date": None,
            "status": status,
            "score": None,
            "certificate_issued": False,
            "expiry_date": None,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        employee_training[training_record_id] = new_training
        return json.dumps({"training_record_id": training_record_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "enroll_employee_training",
                "description": "Enroll an employee in a training program",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "employee_id": {"type": "string", "description": "Employee ID"},
                        "program_id": {"type": "string", "description": "Training program ID"},
                        "enrollment_date": {"type": "string", "description": "Enrollment date"},
                        "status": {"type": "string", "description": "Status (enrolled, in_progress, completed, failed, cancelled), defaults to enrolled"}
                    },
                    "required": ["employee_id", "program_id", "enrollment_date"]
                }
            }
        }
