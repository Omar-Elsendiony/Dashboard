import json
import uuid
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UploadDocument(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        user_id: str,
        worker_id: str,
        title: str,
        file_type: str,
        status: str = "pending"
    ) -> str:
        # Validate presence of user and worker (if needed)
        users = data.get("users", {})
        workers = data.get("workers", {})
        if user_id not in users:
            raise ValueError("User ID not found")
        if worker_id not in workers:
            raise ValueError("Worker ID not found")

        documents = data.setdefault("documents", {})
        document_id = str(uuid.uuid4())

        documents[document_id] = {
            "user_id": user_id,
            "worker_id": worker_id,
            "title": title,
            "file_type": file_type,
            "status": status
        }

        return json.dumps({
            "document_id": document_id,
            "user_id": user_id,
            "worker_id": worker_id,
            "title": title,
            "file_type": file_type,
            "status": status
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "upload_document",
                "description": "Creates a new document associated with a user and worker.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "The ID of the user who owns the document"
                        },
                        "worker_id": {
                            "type": "string",
                            "description": "The ID of the worker related to this document"
                        },
                        "title": {
                            "type": "string",
                            "description": "Title or name of the document"
                        },
                        "file_type": {
                            "type": "string",
                            "description": "Type of file (e.g., pdf, jpg, png)"
                        },
                        "status": {
                            "type": "string",
                            "description": "Initial status of the document (e.g., pending, approved, flagged)",
                            "default": "pending"
                        }
                    },
                    "required": ["user_id", "worker_id", "title", "file_type"]
                }
            }
        }
