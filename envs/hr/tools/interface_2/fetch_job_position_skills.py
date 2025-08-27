import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetJobPositionSkills(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], position_id: str = None, skill_id: str = None) -> str:
        job_position_skills = data.get("job_position_skills", {})
        results = []
        
        for assignment in job_position_skills.values():
            if position_id and assignment.get("position_id") != position_id:
                continue
            if skill_id and assignment.get("skill_id") != skill_id:
                continue
            results.append(assignment)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "fetch_job_position_skills",
                "description": "Retrieve skill assignments for job positions",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "position_id": {"type": "string", "description": "Filter by job position ID"},
                        "skill_id": {"type": "string", "description": "Filter by skill ID"}
                    },
                    "required": []
                }
            }
        }
