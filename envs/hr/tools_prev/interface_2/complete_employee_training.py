import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class CompleteEmployeeTraining(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], training_record_id: str, completion_date: str,
               status: str, score: Optional[float] = None, certificate_issued: bool = False,
               expiry_date: Optional[str] = None) -> str:
        
        employee_training = data.get("employee_training", {})
        
        # Validate training record exists
        if training_record_id not in employee_training:
            return json.dumps({"success": False, "error": f"Training record {training_record_id} not found", "halt": True})
        
        # Validate status
        valid_statuses = ['completed', 'failed']
        if status not in valid_statuses:
            return json.dumps({"success": False, "error": f"Invalid status. Must be one of {valid_statuses}", "halt": True})
        
        # Validate score if provided
        if score is not None and (score < 0 or score > 100):
            return json.dumps({"success": False, "error": "Score must be between 0 and 100", "halt": True})
        
        training_record = employee_training[training_record_id]
        
        # Update training record
        training_record["completion_date"] = completion_date
        training_record["status"] = status
        training_record["score"] = score
        training_record["certificate_issued"] = certificate_issued
        training_record["expiry_date"] = expiry_date
        training_record["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps({"success": True, "message": "Training completion recorded"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "complete_employee_training",
                "description": "Record completion of employee training",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "training_record_id": {"type": "string", "description": "Training record ID"},
                        "completion_date": {"type": "string", "description": "Completion date"},
                        "status": {"type": "string", "description": "Status (completed, failed)"},
                        "score": {"type": "number", "description": "Training score (0-100)"},
                        "certificate_issued": {"type": "boolean", "description": "Whether certificate was issued (True/False)"},
                        "expiry_date": {"type": "string", "description": "Certificate expiry date"}
                    },
                    "required": ["training_record_id", "completion_date", "status"]
                }
            }
        }
