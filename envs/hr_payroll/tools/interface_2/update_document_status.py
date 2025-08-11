
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdateDocumentStatus(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], document_id: str, new_status: str) -> str:
        documents = data.get("documents", {})
        if document_id not in documents:
            raise ValueError("Document not found")

        doc = documents[document_id]
        if doc.get("status") in ["archived", "deleted"]:
            raise ValueError("Document cannot be updated in its current state")

        doc["status"] = new_status
        return json.dumps({"document_id": document_id, "new_status": new_status})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_document_status",
                "description": "Changes the status of a document",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "document_id": {
                            "type": "string",
                            "description": "The ID of the document"
                        },
                        "new_status": {
                            "type": "string",
                            "description": "The new status of the document"
                        }
                    },
                    "required": ["document_id", "new_status"]
                }
            }
        }
