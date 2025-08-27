import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateSkill(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], skill_id: str, skill_name: str = None, status: str = None) -> str:
        skills = data.get("skills", {})
        
        if skill_id not in skills:
            raise ValueError(f"Skill {skill_id} not found")
        
        skill = skills[skill_id]
        
        if skill_name is not None:
            skill["skill_name"] = skill_name
        
        if status is not None:
            valid_statuses = ["active", "inactive"]
            if status not in valid_statuses:
                raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
            skill["status"] = status
        
        skill["updated_at"] = "2025-10-01T00:00:00"

        return json.dumps({"skill_after_update": skill})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_skill",
                "description": "Update an existing skill",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "skill_id": {"type": "string", "description": "ID of the skill to update"},
                        "skill_name": {"type": "string", "description": "Updated skill name"},
                        "status": {"type": "string", "description": "Updated status (active, inactive)"}
                    },
                    "required": ["skill_id"]
                }
            }
        }
