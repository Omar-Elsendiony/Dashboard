import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetSkills(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], skill_id: str = None, skill_name: str = None, status: str = None) -> str:
        skills = data.get("skills", {})
        results = []
        
        for skill in skills.values():
            if skill_id and skill.get("skill_id") != skill_id:
                continue
            if skill_name and skill.get("skill_name") != skill_name:
                continue
            if status and skill.get("status") != status:
                continue
            results.append(skill)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_skills",
                "description": "Retrieve skills with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "skill_id": {"type": "string", "description": "Filter by skill ID"},
                        "skill_name": {"type": "string", "description": "Filter by skill name"},
                        "status": {"type": "string", "description": "Filter by status (active, inactive)"}
                    },
                    "required": []
                }
            }
        }
