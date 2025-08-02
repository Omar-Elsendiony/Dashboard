import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class IncrementLabelUsageCount(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], label_id: int) -> str:
        labels = data.get("labels", {})
        label = labels.get(str(label_id))
        if not label:
            raise ValueError("Label not found")

        label["usage_count"] = label.get("usage_count", 0) + 1

        return json.dumps({
            "status": "incremented",
            "label_id": label_id,
            "usage_count": label["usage_count"]
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "increment_label_usage_count",
                "description": "Increment the usage count of a label by 1",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "label_id": {"type": "integer", "description": "Label ID"}
                    },
                    "required": ["label_id"]
                }
            }
        }
