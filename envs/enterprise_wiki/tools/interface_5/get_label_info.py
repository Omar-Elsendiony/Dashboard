import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetLabelInfo(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], label_id: int) -> str:
        label = data.get("labels", {}).get(str(label_id))
        if not label:
            raise ValueError("Label not found")
        return json.dumps(label)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_label_info",
                "description": "Retrieve information about a specific label",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "label_id": {"type": "integer", "description": "ID of the label"}
                    },
                    "required": ["label_id"]
                }
            }
        }
