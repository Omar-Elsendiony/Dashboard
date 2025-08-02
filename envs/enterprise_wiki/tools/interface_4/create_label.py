import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateLabel(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        name: str,
        space_id: int,
        created_by: int,
        color: str = None,
        description: str = None
    ) -> str:
        labels = data.get("labels", {})
        label_id = max([int(lid) for lid in labels.keys()], default=0) + 1


        created_at = "2025-07-01T00:00:00Z"
        new_label = {
            "id": label_id,
            "name": name,
            "color": color,
            "description": description,
            "space_id": space_id,
            "created_by": created_by,
            "usage_count": 0,
            "created_at": created_at
        }

        labels[str(label_id)] = new_label
        return json.dumps(new_label)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_label",
                "description": "Create a label within a space",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Label name"
                    },
                    "space_id": {
                        "type": "integer",
                        "description": "Space the label belongs to"
                    },
                    "created_by": {
                        "type": "integer",
                        "description": "User who created the label"
                    },
                    "color": {
                        "type": "string",
                        "description": "Optional color of the label (e.g., #ff0000, red, blue, etc.)",
                    },
                    "description": {
                        "type": "string",
                        "description": "Optional description of the label's purpose"
                    }
                },
                "required": ["name", "space_id", "created_by"]
            }

            }
        }
