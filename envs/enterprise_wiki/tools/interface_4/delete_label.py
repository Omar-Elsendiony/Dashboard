import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class DeleteLabel(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], label_id: int) -> str:
        labels = data.get("labels", {})
        if str(label_id) not in labels:
            raise ValueError("Label not found")

        deleted_label = labels.pop(str(label_id))
        return json.dumps(deleted_label)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "delete_label",
                "description": "Delete a label",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "label_id": {"type": "integer", "description": "ID of the label to delete"}
                    },
                    "required": ["label_id"]
                }
            }
        }
