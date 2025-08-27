import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class AdjustDocument(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], document_id: str, document_name: Optional[str] = None,
               confidentiality_level: Optional[str] = None, retention_period_years: Optional[int] = None,
               expiry_date: Optional[str] = None, status: Optional[str] = None) -> str:
        
        document_storage = data.get("document_storage", {})
        
        # Validate document exists
        if document_id not in document_storage:
            return json.dumps({"success": False, "error": f"Document {document_id} not found", "halt": True})
        
        document = document_storage[document_id]
        
        # Validate confidentiality_level if provided
        if confidentiality_level is not None:
            valid_confidentiality_levels = ['public', 'internal', 'confidential', 'restricted']
            if confidentiality_level not in valid_confidentiality_levels:
                return json.dumps({"success": False, "error": f"Invalid confidentiality_level. Must be one of {valid_confidentiality_levels}", "halt": True})
        
        # Validate status if provided
        if status is not None:
            valid_statuses = ['active', 'archived', 'deleted']
            if status not in valid_statuses:
                return json.dumps({"success": False, "error": f"Invalid status. Must be one of {valid_statuses}", "halt": True})
        
        # Update fields
        if document_name is not None:
            document["document_name"] = document_name
        if confidentiality_level is not None:
            document["confidentiality_level"] = confidentiality_level
        if retention_period_years is not None:
            document["retention_period_years"] = retention_period_years
        if expiry_date is not None:
            document["expiry_date"] = expiry_date
        if status is not None:
            document["status"] = status
        
        return json.dumps({"success": True, "message": "Document updated"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "adjust_document",
                "description": "Update an existing document",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "document_id": {"type": "string", "description": "Document ID"},
                        "document_name": {"type": "string", "description": "Updated document name"},
                        "confidentiality_level": {"type": "string", "description": "Updated confidentiality level (public, internal, confidential, restricted)"},
                        "retention_period_years": {"type": "integer", "description": "Updated retention period"},
                        "expiry_date": {"type": "string", "description": "Updated expiry date"},
                        "status": {"type": "string", "description": "Updated status (active, archived, deleted)"}
                    },
                    "required": ["document_id"]
                }
            }
        }
