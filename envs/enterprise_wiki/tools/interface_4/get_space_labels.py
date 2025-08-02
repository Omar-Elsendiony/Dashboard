import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetSpaceLabels(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], space_id: str) -> str:
        labels = data.get("labels", {})
        space_labels = [label for label in labels.values() if str(label.get("space_id")) == space_id]
        return json.dumps(space_labels)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_space_labels",
                "description": "Get all labels for a specific space",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "space_id": {"type": "string", "description": "Space ID"},
                    },
                    "required": ["space_id"]
                }
            }
        }
