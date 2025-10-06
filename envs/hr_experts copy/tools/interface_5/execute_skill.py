import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class ExecuteSkill(Tool):
    """
    Execute skills including creation and updates for skills management.
    """
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        action: str,
        skill_id: Optional[str] = None,
        skill_name: Optional[str] = None,
        status: Optional[str] = None,
    ) -> str:
        """
        Executes the specified action (create or update) on skills.
        """
        def generate_id(table: Dict[str, Any]) -> str:
            """Generates a new unique ID for a record."""
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        timestamp = "2025-10-01T12:00:00"
        skills = data.get("skills", {})

        # Validate supported statuses
        supported_statuses = ["active", "inactive"]

        if action == "create":
            # Required fields for skill creation
            if not skill_name:
                return json.dumps({
                    "error": "Missing required parameter 'skill_name' for create operation"
                })

            # Validate status if provided
            if status and status not in supported_statuses:
                return json.dumps({
                    "error": f"Invalid status '{status}'. Must be one of: {', '.join(supported_statuses)}"
                })

            # Check for duplicate skill names
            for existing_skill in skills.values():
                if existing_skill.get("skill_name", "").lower() == skill_name.lower():
                    return json.dumps({
                        "error": f"Skill with name '{skill_name}' already exists"
                    })

            # Generate new skill ID
            new_skill_id = generate_id(skills)

            # Create new skill record
            new_skill = {
                "skill_id": new_skill_id,
                "skill_name": skill_name.strip(),
                "status": status if status else "active",
                "created_at": timestamp,
                "updated_at": timestamp
            }

            # Add to skills data
            skills[new_skill_id] = new_skill

            return json.dumps({
                "success": True,
                "message": f"Skill '{skill_name}' created successfully",
                "skill_id": new_skill_id,
                "skill_data": new_skill
            })

        elif action == "update":
            # Required field for skill update
            if not skill_id:
                return json.dumps({
                    "error": "Missing required parameter 'skill_id' for update operation"
                })

            # At least one optional field must be provided
            if not any([skill_name, status]):
                return json.dumps({
                    "error": "At least one optional parameter (skill_name, status) must be provided for update operation"
                })

            # Check if skill exists
            if skill_id not in skills:
                return json.dumps({
                    "error": f"Skill with ID '{skill_id}' not found"
                })

            # Validate status if provided
            if status and status not in supported_statuses:
                return json.dumps({
                    "error": f"Invalid status '{status}'. Must be one of: {', '.join(supported_statuses)}"
                })

            # Check for duplicate skill names (excluding current skill)
            if skill_name:
                for existing_skill_id, existing_skill in skills.items():
                    if (existing_skill_id != skill_id and 
                        existing_skill.get("skill_name", "").lower() == skill_name.lower()):
                        return json.dumps({
                            "error": f"Skill with name '{skill_name}' already exists"
                        })

            # Update skill record
            skill_record = skills[skill_id]
            
            if skill_name:
                skill_record["skill_name"] = skill_name.strip()
            if status:
                skill_record["status"] = status
            
            skill_record["updated_at"] = timestamp

            return json.dumps({
                "success": True,
                "message": f"Skill with ID '{skill_id}' updated successfully",
                "skill_id": skill_id,
                "skill_data": skill_record
            })

        else:
            return json.dumps({
                "error": f"Invalid action '{action}'. Must be 'create' or 'update'"
            })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "execute_skill",
                "description": "Execute skills including creation and updates. For creation, requires skill_name and optionally accepts status (active, inactive). For updates, requires skill_id and at least one optional field (skill_name, status). Validates skill name uniqueness and status values. Used for skills management workflows including creating new skills and updating existing skill information.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "The action to perform: 'create' to create a new skill, 'update' to modify an existing skill",
                            "enum": ["create", "update"]
                        },
                        "skill_id": {
                            "type": "string",
                            "description": "Skill ID (required for update operations)"
                        },
                        "skill_name": {
                            "type": "string",
                            "description": "Name of the skill (required for create, optional for update)"
                        },
                        "status": {
                            "type": "string",
                            "description": "Status of the skill: 'active' or 'inactive' (optional for both create and update)",
                            "enum": ["active", "inactive"]
                        }
                    },
                    "required": ["action"]
                }
            }
        }