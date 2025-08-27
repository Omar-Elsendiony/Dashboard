import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetEmployeeTraining(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], training_record_id: Optional[str] = None,
               employee_id: Optional[str] = None, program_id: Optional[str] = None,
               status: Optional[str] = None) -> str:
        employee_training = data.get("employee_training", {})
        results = []
        
        for training in employee_training.values():
            if training_record_id and training.get("training_record_id") != training_record_id:
                continue
            if employee_id and training.get("employee_id") != employee_id:
                continue
            if program_id and training.get("program_id") != program_id:
                continue
            if status and training.get("status") != status:
                continue
            results.append(training)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "fetch_employee_training",
                "description": "Get employee training records with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "training_record_id": {"type": "string", "description": "Filter by training record ID"},
                        "employee_id": {"type": "string", "description": "Filter by employee ID"},
                        "program_id": {"type": "string", "description": "Filter by program ID"},
                        "status": {"type": "string", "description": "Filter by status (enrolled, in_progress, completed, failed, cancelled)"}
                    },
                    "required": []
                }
            }
        }
