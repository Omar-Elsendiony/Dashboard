import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateSpace(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        key: str,
        name: str,
        created_by: int,
        description: str = None,
        space_type: str = "global",
        anonymous_access: bool = False,
        public_signup: bool = False,
        theme: str = None,
        logo_url: str = None
    ) -> str:
        spaces = data.get("spaces", {})
        space_id = max([int(sid) for sid in spaces.keys()], default=0) + 1



        new_space = {
            "id": space_id,
            "key": key,
            "name": name,
            "description": description,
            "type": space_type,
            "status": "current",
            "homepage_id": None,
            "theme": theme,
            "logo_url": logo_url,
            "anonymous_access": anonymous_access,
            "public_signup": public_signup,
            "created_by": created_by,
            "created_at": "2025-07-17T00:00:00Z",
            "updated_at": "2025-07-17T00:00:00Z"
        }

        spaces[str(space_id)] = new_space
        return json.dumps(new_space)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_space",
                "description": "Create a new space",
            "parameters": {
                "type": "object",
                "properties": {
                    "key": { "type": "string", "description": "Unique key for the space" },
                    "name": { "type": "string", "description": "Space name" },
                    "created_by": { "type": "integer", "description": "User ID of space creator" },
                    "description": { "type": "string", "description": "Optional space description" },
                    "space_type": { 
                        "type": "string",
                        "enum": ["global", "personal", "private"],
                        "default": "global",
                        "description": "Type of the space"
                    },
                    "anonymous_access": {
                        "type": "boolean",
                        "description": "Whether anonymous users can view the space"
                    },
                    "public_signup": {
                        "type": "boolean",
                        "description": "Whether users can sign up to the space publicly"
                    },
                        "theme": { "type": "string", "description": "Optional theme name for the space" },
                        "logo_url": { "type": "string", "description": "Optional logo image URL" }
                },
                "required": ["key", "name", "created_by"]
            }

            }
        }
