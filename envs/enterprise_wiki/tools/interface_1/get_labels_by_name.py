import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetLabelsByName(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], label_name: str) -> str:
        labels = data.get("labels", {})
        
        matching_labels = []
        for label_id, label in labels.items():
            if label.get("name") == label_name:
                matching_labels.append(label)
        
        return json.dumps(matching_labels)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_labels_by_name",
                "description": "Get labels by name",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "label_name": {
                            "type": "string",
                            "description": "The name of the label to search for"
                        }
                    },
                    "required": ["label_name"]
                }
            }
        }
