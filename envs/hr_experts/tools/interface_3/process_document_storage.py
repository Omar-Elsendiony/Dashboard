import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class ProcessDocumentStorage(Tool):
    """
    Execute document storage, including uploads and metadata updates.
    """
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        operation: str,
        document_id: Optional[str] = None,
        document_name: Optional[str] = None,
        document_type: Optional[str] = None,
        file_path: Optional[str] = None,
        uploaded_by: Optional[str] = None,
        employee_id: Optional[str] = None,
        confidentiality_level: Optional[str] = 'internal',
        retention_period_years: Optional[int] = 7,
        status: Optional[str] = None,
        expiry_date: Optional[str] = None,
    ) -> str:
        """
        Executes the specified operation (create or update) on documents.
        """
        def generate_id(table: Dict[str, Any]) -> str:
            """Generates a new unique ID for a record."""
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)


        timestamp = "2025-10-01T12:00:00"
        documents = data.get("document_storage", {})
        users = data.get("users", {})
        employees = data.get("employees", {})

        if operation == "create":
            if not all([document_name, document_type, file_path, uploaded_by]):
                return json.dumps({"error": "Missing required parameters for create operation."})
            
            if uploaded_by not in users:
                return json.dumps({"error": f"User with ID {uploaded_by} not found."})
            if employee_id and employee_id not in employees:
                return json.dumps({"error": f"Employee with ID {employee_id} not found."})

            valid_types = ["contract", "policy", "handbook", "form", "certificate", "report", "resume", "offer_letter"]
            if document_type not in valid_types:
                return json.dumps({"error": f"Invalid document type. Must be one of {valid_types}."})

            new_doc_id = generate_id(documents)
            new_document = {
                "document_id": new_doc_id,
                "document_name": document_name,
                "document_type": document_type,
                "employee_id": employee_id,
                "file_path": file_path,
                "upload_date": timestamp,
                "uploaded_by": uploaded_by,
                "confidentiality_level": confidentiality_level,
                "retention_period_years": retention_period_years,
                "expiry_date": expiry_date,
                "status": "active",
                "created_at": timestamp,
            }
            documents[new_doc_id] = new_document
            return json.dumps(new_document)

        elif operation == "update":
            if not all([document_id, status]):
                return json.dumps({"error": "Missing required parameters for update operation."})
            
            if document_id not in documents:
                return json.dumps({"error": f"Document with ID {document_id} not found."})

            valid_statuses = ["active", "archived", "deleted"]
            if status not in valid_statuses:
                return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}."})
            
            doc_to_update = documents[document_id]
            doc_to_update["status"] = status
            if document_name is not None:
                doc_to_update["document_name"] = document_name
            if confidentiality_level is not None:
                doc_to_update["confidentiality_level"] = confidentiality_level
            if expiry_date is not None:
                doc_to_update["expiry_date"] = expiry_date
            
            return json.dumps(doc_to_update)

        else:
            return json.dumps({"error": "Invalid operation. Must be 'create' or 'update'."})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        """
        Returns the schema for the ManageDocumentStorage tool.
        """
        return {
            "type": "function",
            "function": {
                "name": "process_document_storage",
                "description": "Handles the uploading of new documents (create) and the modification of their metadata or status (update).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation": {"type": "string", "description": "Action: 'create' or 'update'."},
                        "document_name": {"type": "string", "description": "The display name of the document. Required for 'create', optional for 'update'."},
                        "document_type": {"type": "string", "description": "Type: 'contract', 'policy', 'handbook', 'form', 'certificate', 'report', 'resume', 'offer_letter'. Required for 'create'."},
                        "file_path": {"type": "string", "description": "The storage path where the document file is located. Required for 'create'."},
                        "uploaded_by": {"type": "string", "description": "The user ID of the person uploading the document. Required for 'create'."},
                        "employee_id": {"type": "string", "description": "The ID of the employee associated with this document. Optional for 'create'."},
                        "confidentiality_level": {"type": "string", "description": "Security level, defaults to 'internal'. Optional for 'create' and 'update'."},
                        "retention_period_years": {"type": "integer", "description": "The number of years the document must be stored. Defaults to 7. Optional for 'create'."},
                        "document_id": {"type": "string", "description": "The ID of the document to be updated. Required for 'update'."},
                        "status": {"type": "string", "description": "New status: 'active', 'archived', 'deleted'. Required for 'update'."},
                        "expiry_date": {"type": "string", "description": "A new or updated expiration date (YYYY-MM-DD). Optional for 'update'."},
                    },
                    "required": ["operation"],
                },
            },
        }
