import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetTrainingPrograms(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], program_id: Optional[str] = None,
               program_type: Optional[str] = None, mandatory: Optional[bool] = None,
               status: Optional[str] = None) -> str:
        training_programs = data.get("training_programs", {})
        results = []
        
        for program in training_programs.values():
            if program_id and program.get("program_id") != program_id:
                continue
            if program_type and program.get("program_type") != program_type:
                continue
            if mandatory is not None and program.get("mandatory") != mandatory:
                continue
            if status and program.get("status") != status:
                continue
            results.append(program)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_training_programs",
                "description": "Get training programs with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "program_id": {"type": "string", "description": "Filter by program ID"},
                        "program_type": {"type": "string", "description": "Filter by program type (onboarding, compliance, technical, leadership, safety, diversity, ai_ethics)"},
                        "mandatory": {"type": "boolean", "description": "Filter by mandatory flag (True/False)"},
                        "status": {"type": "string", "description": "Filter by status (active, inactive, draft)"}
                    },
                    "required": []
                }
            }
        }
