import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class ProcessJobPositionSkills(Tool):
    """
    Execute job position skills associations including adding and removing skills.
    """
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        action: str,
        position_id: str,
        skill_id: Optional[str] = None,
    ) -> str:
        """
        Executes the specified action (add or remove) on job position skills associations.
        """
        def generate_id(table: Dict[str, Any]) -> str:
            """Generates a new unique ID for a record."""
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        job_positions = data.get("job_positions", {})
        job_position_skills = data.get("job_position_skills", {})
        skills = data.get("skills", {})

        # Validate position exists
        if position_id not in job_positions:
            return json.dumps({
                "error": f"Job position with ID '{position_id}' not found"
            })

        if action == "add":
            # skill_id is required for add
            if not skill_id:
                return json.dumps({
                    "error": "Missing required parameter 'skill_id' for add operation"
                })

            # Validate skill exists
            if skill_id not in skills:
                return json.dumps({
                    "error": f"Skill with ID '{skill_id}' not found"
                })

            # Check if association already exists
            for existing_association in job_position_skills.values():
                if (existing_association.get("position_id") == position_id and 
                    existing_association.get("skill_id") == skill_id):
                    return json.dumps({
                        "error": f"Skill {skill_id} is already associated with position {position_id}"
                    })

            # Generate new association ID
            new_association_id = generate_id(job_position_skills)

            # Create new association
            new_association = {
                "position_id": position_id,
                "skill_id": skill_id
            }

            # Add to job position skills data
            job_position_skills[new_association_id] = new_association

            return json.dumps({
                "success": True,
                "message": f"Skill {skill_id} added to position {position_id} successfully",
                "association_id": new_association_id,
                "association_data": new_association
            })

        elif action == "remove":
            # skill_id is required for remove
            if not skill_id:
                return json.dumps({
                    "error": "Missing required parameter 'skill_id' for remove operation"
                })

            # Find the association to remove
            association_to_remove = None
            association_id_to_remove = None
            
            for assoc_id, association in job_position_skills.items():
                if (association.get("position_id") == position_id and 
                    association.get("skill_id") == skill_id):
                    association_to_remove = association
                    association_id_to_remove = assoc_id
                    break

            if not association_to_remove:
                return json.dumps({
                    "error": f"No association found between position {position_id} and skill {skill_id}"
                })

            # Remove the association
            del job_position_skills[association_id_to_remove]

            return json.dumps({
                "success": True,
                "message": f"Skill {skill_id} removed from position {position_id} successfully",
                "removed_association_id": association_id_to_remove
            })

        elif action == "list":
            # List all skills associated with the position
            associated_skills = []
            
            for association in job_position_skills.values():
                if association.get("position_id") == position_id:
                    skill_id = association.get("skill_id")
                    skill_info = skills.get(skill_id, {})
                    associated_skills.append({
                        "skill_id": skill_id,
                        "skill_name": skill_info.get("skill_name", "Unknown"),
                        "skill_category": skill_info.get("category", "Unknown")
                    })

            return json.dumps({
                "success": True,
                "message": f"Found {len(associated_skills)} skills associated with position {position_id}",
                "position_id": position_id,
                "associated_skills": associated_skills
            })

        else:
            return json.dumps({
                "error": f"Invalid action '{action}'. Must be 'add', 'remove', or 'list'"
            })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "process_job_position_skills",
                "description": "Execute skill associations for job positions. Supports adding new skill requirements to positions, removing existing skill associations, and listing all skills associated with a position. Validates that both position and skill exist before creating associations. Prevents duplicate associations between the same position and skill. Used for job position skills management workflows including defining skill requirements for roles.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "The action to perform: 'add' to associate a skill with position, 'remove' to remove skill association, 'list' to show all skills for position",
                            "enum": ["add", "remove", "list"]
                        },
                        "position_id": {
                            "type": "string",
                            "description": "Job position ID (required for all operations)"
                        },
                        "skill_id": {
                            "type": "string",
                            "description": "Skill ID (required for add and remove operations)"
                        }
                    },
                    "required": ["action", "position_id"]
                }
            }
        }