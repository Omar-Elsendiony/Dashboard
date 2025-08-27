import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class AssignSkillToPosition(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], position_id: str, skill_id: str) -> str:
        job_positions = data.get("job_positions", {})
        skills = data.get("skills", {})
        job_position_skills = data.setdefault("job_position_skills", {})
        
        # Validate position exists
        if position_id not in job_positions:
            raise ValueError(f"Job position {position_id} not found")
        
        # Validate skill exists
        if skill_id not in skills:
            raise ValueError(f"Skill {skill_id} not found")
        
        # Check if assignment already exists
        for assignment in job_position_skills.values():
            if (assignment.get("position_id") == position_id and 
                assignment.get("skill_id") == skill_id):
                return json.dumps({"status": "already_assigned"})
        
        # Create composite key for the assignment
        assignment_key = f"{position_id}_{skill_id}"
        
        new_assignment = {
            "position_id": position_id,
            "skill_id": skill_id,
            "created_at": "2025-10-01T00:00:00"
        }
        
        job_position_skills[assignment_key] = new_assignment
        return json.dumps({"success": True, "message": "Skill assigned to position"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "assign_skill_to_position",
                "description": "Assign a skill requirement to a job position",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "position_id": {"type": "string", "description": "ID of the job position"},
                        "skill_id": {"type": "string", "description": "ID of the skill"}
                    },
                    "required": ["position_id", "skill_id"]
                }
            }
        }
