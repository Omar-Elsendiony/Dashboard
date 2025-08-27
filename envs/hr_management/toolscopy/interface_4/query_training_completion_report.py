import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class QueryTrainingCompletionReport(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], program_id: str = None, 
               department_id: str = None) -> str:
        training_programs = data.get("training_programs", {})
        employee_training = data.get("employee_training", {})
        employees = data.get("employees", {})
        job_positions = data.get("job_positions", {})
        users = data.get("users", {})
        
        results = []
        
        for program_key, program in training_programs.items():
            if program_id and program_key != program_id:
                continue
            
            # Count enrollments and completions for this program
            total_enrolled = 0
            completed = 0
            failed = 0
            in_progress = 0
            
            for training in employee_training.values():
                if training.get("program_id") != program_key:
                    continue
                
                # Filter by department if specified
                if department_id:
                    employee = employees.get(training.get("employee_id"), {})
                    position = job_positions.get(employee.get("position_id"), {})
                    if position.get("department_id") != department_id:
                        continue
                
                total_enrolled += 1
                status = training.get("status")
                if status == "completed":
                    completed += 1
                elif status == "failed":
                    failed += 1
                elif status in ["enrolled", "in_progress"]:
                    in_progress += 1
            
            completion_rate = (completed / total_enrolled * 100) if total_enrolled > 0 else 0
            
            report = {
                "program_id": program_key,
                "program_name": program.get("program_name"),
                "program_type": program.get("program_type"),
                "total_enrolled": total_enrolled,
                "completed": completed,
                "failed": failed,
                "in_progress": in_progress,
                "completion_rate_percent": round(completion_rate, 2)
            }
            
            results.append(report)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "query_training_completion_report",
                "description": "Get training completion statistics",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "program_id": {"type": "string", "description": "Filter by specific training program"},
                        "department_id": {"type": "string", "description": "Filter by department"}
                    },
                    "required": []
                }
            }
        }
