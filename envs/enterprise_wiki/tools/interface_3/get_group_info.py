import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetGroupInfo(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], group_id: int) -> str:
        groups = data.get("groups", {})
        return json.dumps(groups.get(str(group_id), {}))

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_group_info",
                "description": "Get information about a group",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "group_id": {"type": "integer", "description": "Group ID"}
                    },
                    "required": ["group_id"]
                }
            }
        }
