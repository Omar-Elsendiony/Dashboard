
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ListDocumentsByUser(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: str) -> str:
        documents = data.get("documents", {})
        result = [
            {**d, "document_id": doc_id}
            for doc_id, d in documents.items()
            if d.get("user_id") == user_id
        ]
        result.sort(key=lambda x: x.get("title", ""), reverse=True)
        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_documents_by_user",
                "description": "Returns all uploaded documents for a user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "User ID to retrieve documents for"
                        }
                    },
                    "required": ["user_id"]
                }
            }
        }
