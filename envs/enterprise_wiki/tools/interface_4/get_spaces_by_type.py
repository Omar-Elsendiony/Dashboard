import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool

class GetSpacesByType(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], type: str) -> str:
        spaces = data.get("spaces", {})
        filtered = [s for s in spaces.values() if s.get("type") == type]
        return json.dumps(filtered)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_spaces_by_type",
                "description": "Get all spaces matching a specific type",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "type": {"type": "string"}
                    },
                    "required": ["type"]
                }
            }
        }
