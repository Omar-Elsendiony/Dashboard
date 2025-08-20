import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateUploadDocument(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: str, confidentiality_level: str, file_name: str,
                file_format: str, report_id: str = None) -> str:

        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        users = data.get("users", {})
        documents = data.get("documents", {})
        
        # Validate user exists
        if str(user_id) not in users:
            return json.dumps({"success": False, "message": "User not found"})
        
        # Validate file format
        valid_formats = ["pdf", "docx", "xlsx", "csv"]
        if file_format.lower() not in valid_formats:
            return json.dumps({"success": False, "message": f"Invalid file format. Must be one of {valid_formats}"})
        
        # Validate confidentiality level
        valid_levels = ["public", "internal", "confidential", "restricted"]
        if confidentiality_level.lower() not in valid_levels:
            return json.dumps({"success": False, "message": f"Invalid confidentiality level. Must be one of {valid_levels}"})
        
        document_id = generate_id(documents)
        timestamp = "2025-10-01T00:00:00"
        
        new_document = {
            "document_id": str(document_id),
            "name": file_name,
            "type": file_format.lower(),
            "uploaded_by": user_id,
            "upload_date": timestamp,
            "report_id": str(report_id),
            "size_bytes": 2560000,
            "status": "available"
        }
        
        documents[str(document_id)] = new_document
        return json.dumps({"doc_id": str(document_id), "status": "available"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_upload_document",
                "description": "Create and upload a document to the system",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "ID of the user uploading the document"},
                        "confidentiality_level": {"type": "string", "description": "Confidentiality levels: 'public', 'internal', 'confidential', 'restricted'"},
                        "file_name": {"type": "string", "description": "Name of the file"},
                        "file_format": {"type": "string", "description": "File format: pdf, docx, xlsx, or csv"},
                        "report_id": {"type": "string", "description": "ID of the related report (optional)"}
                    },
                    "required": ["user_id", "confidentiality_level", "file_name", "file_format"]
                }
            }
        }
