import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetInvestorDocuments(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_id: str, 
               document_format: Optional[str] = None, confidentiality_level: Optional[str] = None,
               status: Optional[str] = None) -> str:
        investors = data.get("investors", {})
        documents = data.get("documents", {})
        reports = data.get("reports", {})
        users = data.get("users", {})
        
        # Validate investor exists
        if str(investor_id) not in investors:
            raise ValueError(f"Investor {investor_id} not found")
        
        # Get documents related to this investor through reports
        documents = []
        
        # First, find all reports for this investor
        report_ids = []
        for report in reports.values():
            if report.get("investor_id") == investor_id:
                report_ids.append(report.get("report_id"))
        
        # Then find documents associated with these reports
        for document in documents.values():
            report_id = document.get("report_id")
            
            # Include document if it's associated with investor's reports or if no report_id (general docs)
            if report_id in report_ids or not report_id:
                # Filter by format if specified
                if document_format and document.get("format") != document_format:
                    continue
                
                # Filter by confidentiality level if specified
                if confidentiality_level and document.get("confidentiality_level") != confidentiality_level:
                    continue
                
                # Filter by status if specified
                if status and document.get("status") != status:
                    continue
                
                # Enrich with uploader details
                uploaded_by = document.get("uploaded_by")
                uploader = users.get(str(uploaded_by), {})
                
                enriched_document = {
                    **document,
                    "uploader_name": f"{uploader.get('first_name', '')} {uploader.get('last_name', '')}".strip(),
                    "uploader_email": uploader.get("email")
                }
                documents.append(enriched_document)
        
        return json.dumps(documents)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_investor_documents",
                "description": "Retrieve all documents related to the investor (agreements, reports, correspondence)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {
                            "type": "string",
                            "description": "ID of the investor"
                        },
                        "document_format": {
                            "type": "string",
                            "description": "Filter by document format",
                            "enum": ["pdf", "xlsx", "docx", "csv", "other"]
                        },
                        "confidentiality_level": {
                            "type": "string",
                            "description": "Filter by confidentiality level",
                            "enum": ["public", "internal", "confidential", "restricted"]
                        },
                        "status": {
                            "type": "string",
                            "description": "Filter by document status",
                            "enum": ["available", "archived", "deleted"]
                        }
                    },
                    "required": ["investor_id"]
                }
            }
        }
