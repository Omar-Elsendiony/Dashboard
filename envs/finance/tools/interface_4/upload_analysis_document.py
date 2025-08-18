import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UploadAnalysisDocument(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], analysis_user_id: str, 
               size_bytes: int, confidentiality_level: str, file_name: str, 
               file_format: str, analysis_report_id: str = None) -> str:

        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        users = data.get("users", {})
        documents = data.get("documents", {})
        
        # Validate user exists
        if str(analysis_user_id) not in users:
            return json.dumps({"success": False, "message": "User not found"})
        
        # Validate file format
        valid_formats = ["pdf", "docx", "xlsx", "csv"]
        if file_format.lower() not in valid_formats:
            return json.dumps({"success": False, "message": f"Invalid file format. Must be one of {valid_formats}"})
        
        # Validate confidentiality level
        valid_levels = ["public", "internal", "confidential", "restricted"]
        if confidentiality_level.lower() not in valid_levels:
            return json.dumps({"success": False, "message": f"Invalid confidentiality level. Must be one of {valid_levels}"})
        
        analysis_document_id = generate_id(documents)
        timestamp = "2025-10-01T00:00:00"
        
        new_document = {
            "analysis_document_id": analysis_document_id,
            "name": file_name,
            "type": file_format.lower(),
            "uploaded_by": analysis_user_id,
            "upload_date": timestamp,
            "analysis_report_id": analysis_report_id,
            "size_bytes": size_bytes,
            "status": "available"
        }
        
        documents[str(analysis_document_id)] = new_document
        return json.dumps({"doc_id": str(analysis_document_id), "status": "available"})

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
                        "analysis_user_id": {"type": "string", "description": "ID of the user uploading the document"},
                        "size_bytes": {"type": "integer", "description": "Size of document in bytes"},
                        "confidentiality_level": {"type": "string", "description": "Confidentiality levels: 'public', 'internal', 'confidential', 'restricted'"},
                        "file_name": {"type": "string", "description": "Name of the file"},
                        "file_format": {"type": "string", "description": "File format: pdf, docx, xlsx, or csv"}
                    },
                    "required": ["analysis_user_id", "size_bytes", "confidentiality_level", "file_name", "file_format"]
                }
            }
        }
