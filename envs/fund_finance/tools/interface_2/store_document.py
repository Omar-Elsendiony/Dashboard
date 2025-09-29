import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class StoreDocument(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], name: str, format: str, uploaded_by: str,
               size_bytes: Optional[int] = None, report_id: Optional[str] = None,
               confidentiality_level: str = "internal", status: str = "available") -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        documents = data.get("documents", {})
        users = data.get("users", {})
        reports = data.get("reports", {})
        
        # Validate uploaded_by user exists
        if str(uploaded_by) not in users:
            return json.dumps({"error": f"User {uploaded_by} not found"})
        
        # Validate format
        valid_formats = ["pdf", "xlsx", "docx", "csv", "other"]
        if format not in valid_formats:
            return json.dumps({"error": f"Invalid format. Must be one of {valid_formats}"})
        
        # Validate confidentiality_level
        valid_confidentiality = ["public", "internal", "confidential", "restricted"]
        if confidentiality_level not in valid_confidentiality:
            return json.dumps({"error": f"Invalid confidentiality level. Must be one of {valid_confidentiality}"})
        
        # Validate status
        valid_statuses = ["available", "archived", "deleted"]
        if status not in valid_statuses:
            return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}"})
        
        # Validate report_id if provided
        if report_id and str(report_id) not in reports:
            return json.dumps({"error": f"Report {report_id} not found"})
        
        # Check if document name already exists (file name is unique key)
        for doc in documents.values():
            if doc.get("name") == name:
                return json.dumps({"error": f"Document with name '{name}' already exists"})
        
        document_id = generate_id(documents)
        timestamp = "2025-10-01T00:00:00"
        
        new_document = {
            "document_id": str(document_id),
            "name": name,
            "format": format,
            "uploaded_by": uploaded_by,
            "upload_date": timestamp,
            "report_id": str(report_id),
            "size_bytes": size_bytes,
            "confidentiality_level": confidentiality_level,
            "status": status
        }
        
        documents[str(document_id)] = new_document
        return json.dumps(new_document)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "store_document",
                "description": "Upload a new document to the system",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Name of the document file"},
                        "format": {"type": "string", "description": "Format of document (pdf, xlsx, docx, csv, other)"},
                        "uploaded_by": {"type": "string", "description": "ID of the user uploading the document"},
                        "size_bytes": {"type": "integer", "description": "Size of document in bytes"},
                        "report_id": {"type": "string", "description": "ID of related report if applicable"},
                        "confidentiality_level": {"type": "string", "description": "Confidentiality level (public, internal, confidential, restricted), defaults to internal"},
                        "status": {"type": "string", "description": "Status of document (available, archived, deleted), defaults to available"}
                    },
                    "required": ["name", "format", "uploaded_by"]
                }
            }
        }