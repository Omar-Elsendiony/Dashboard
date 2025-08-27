import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UploadDocument(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], document_name: str, document_type: str,
               file_path: str, uploaded_by: str, confidentiality_level: str,
               employee_id: Optional[str] = None, retention_period_years: int = 7,
               expiry_date: Optional[str] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        users = data.get("users", {})
        employees = data.get("employees", {})
        document_storage = data.get("document_storage", {})
        
        # Validate uploaded_by user exists
        if uploaded_by not in users:
            return json.dumps({"success": False, "error": f"User {uploaded_by} not found", "halt": True})
        
        # Validate employee exists if provided
        if employee_id is not None and employee_id not in employees:
            return json.dumps({"success": False, "error": f"Employee {employee_id} not found", "halt": True})
        
        # Validate document_type
        valid_document_types = ['contract', 'policy', 'handbook', 'form', 'certificate', 'report', 'resume', 'offer_letter']
        if document_type not in valid_document_types:
            return json.dumps({"success": False, "error": f"Invalid document_type. Must be one of {valid_document_types}", "halt": True})
        
        # Validate confidentiality_level
        valid_confidentiality_levels = ['public', 'internal', 'confidential', 'restricted']
        if confidentiality_level not in valid_confidentiality_levels:
            return json.dumps({"success": False, "error": f"Invalid confidentiality_level. Must be one of {valid_confidentiality_levels}", "halt": True})
        
        document_id = generate_id(document_storage)
        timestamp = "2025-10-01T00:00:00"
        
        new_document = {
            "document_id": document_id,
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
            "created_at": timestamp
        }
        
        document_storage[document_id] = new_document
        return json.dumps({"document_id": document_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "upload_document",
                "description": "Upload a new document to the system",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "document_name": {"type": "string", "description": "Document name"},
                        "document_type": {"type": "string", "description": "Document type (contract, policy, handbook, form, certificate, report, resume, offer_letter)"},
                        "file_path": {"type": "string", "description": "File path"},
                        "uploaded_by": {"type": "string", "description": "User ID of uploader"},
                        "confidentiality_level": {"type": "string", "description": "Confidentiality level (public, internal, confidential, restricted)"},
                        "employee_id": {"type": "string", "description": "Associated employee ID"},
                        "retention_period_years": {"type": "integer", "description": "Retention period in years, defaults to 7"},
                        "expiry_date": {"type": "string", "description": "Document expiry date"}
                    },
                    "required": ["document_name", "document_type", "file_path", "uploaded_by", "confidentiality_level"]
                }
            }
        }
