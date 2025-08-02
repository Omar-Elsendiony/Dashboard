import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetUserAttachments(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: int) -> str:
        attachments = data.get("attachments", {}).values()
        result = [a for a in attachments if str(a.get("uploaded_by")) == str(user_id)]
        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_user_attachments",
                "description": "Get all attachments uploaded by a specific user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "integer", "description": "User ID"}
                    },
                    "required": ["user_id"]
                }
            }
        }
