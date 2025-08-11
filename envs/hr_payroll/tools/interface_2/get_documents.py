import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetDocuments(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        document_id: str = None,
        user_id: str = None,
        worker_id: str = None,
        title: str = None,
        file_type: str = None,
        status: str = None
    ) -> str:
        documents = data.get("documents", {})

        def matches(doc_id, doc):
            if document_id and doc_id != document_id:
                return False
            if user_id and doc.get("user_id") != user_id:
                return False
            if worker_id and doc.get("worker_id") != worker_id:
                return False
            if title and title.lower() not in doc.get("title", "").lower():
                return False
            if file_type and doc.get("file_type") != file_type:
                return False
            if status and doc.get("status") != status:
                return False
            return True

        result = [
            {**doc, "document_id": doc_id}
            for doc_id, doc in documents.items()
            if matches(doc_id, doc)
        ]
        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_documents",
                "description": (
                    "Retrieves documents with optional filters on document_id, user_id, worker_id, title, "
                    "file_type, and status. Partial match allowed for title."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "document_id": {
                            "type": "string",
                            "description": "Exact document ID (unique identifier)"
                        },
                        "user_id": {
                            "type": "string",
                            "description": "Filter by user ID"
                        },
                        "worker_id": {
                            "type": "string",
                            "description": "Filter by worker ID"
                        },
                        "title": {
                            "type": "string",
                            "description": "Filter by partial or full title (case-insensitive)"
                        },
                        "file_type": {
                            "type": "string",
                            "description": "Filter by file type (e.g., pdf, jpg)"
                        },
                        "status": {
                            "type": "string",
                            "description": "Filter by status (e.g., approved, rejected, flagged)"
                        }
                    },
                    "required": []
                }
            }
        }
