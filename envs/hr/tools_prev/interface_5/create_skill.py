import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class CreateSkill(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], skill_name: str, status: str = "active") -> str:
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        skills = data.setdefault("skills", {})
        
        # Validate status
        valid_statuses = ["active", "inactive"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        # Check if skill already exists
        for skill in skills.values():
            if skill.get("skill_name").lower() == skill_name.lower():
                raise ValueError(f"Skill '{skill_name}' already exists")
        
        skill_id = generate_id(skills)
        timestamp = "2025-10-01T00:00:00"
        
        new_skill = {
            "skill_id": skill_id,
            "skill_name": skill_name,
            "status": status,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        skills[skill_id] = new_skill
        return json.dumps({"skill_id": skill_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_skill",
                "description": "Create a new skill in the system",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "skill_name": {"type": "string", "description": "Name of the skill"},
                        "status": {"type": "string", "description": "Skill status (active, inactive), defaults to active"}
                    },
                    "required": ["skill_name"]
                }
            }
        }
