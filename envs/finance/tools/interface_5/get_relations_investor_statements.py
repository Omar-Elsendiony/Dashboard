import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetRelationsInvestorStatements(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], relations_investor_id: str, 
               report_type: Optional[str] = None, start_date: Optional[str] = None, 
               end_date: Optional[str] = None) -> str:
        investors = data.get("investors", {})
        reports = data.get("reports", {})
        documents = data.get("documents", {})
        users = data.get("users", {})
        
        # Validate investor exists
        if str(relations_investor_id) not in investors:
            raise ValueError(f"Investor {relations_investor_id} not found")
        
        # Get reports for this investor
        investor_statements = []
        for report in reports.values():
            if report.get("relations_investor_id") == relations_investor_id:
                # Filter by report type if specified
                if report_type and report.get("report_type") != report_type:
                    continue
                
                # Filter by date range if provided
                report_date = report.get("report_date")
                if start_date and report_date < start_date:
                    continue
                if end_date and report_date > end_date:
                    continue
                
                # Enrich with generator details
                generated_by = report.get("generated_by")
                generator = users.get(str(generated_by), {})
                
                # Find associated documents
                relations_report_id = report.get("relations_report_id")
                associated_docs = []
                for doc in documents.values():
                    if doc.get("relations_report_id") == relations_report_id:
                        associated_docs.append({
                            "relations_document_id": doc.get("relations_document_id"),
                            "name": doc.get("name"),
                            "format": doc.get("format"),
                            "size_bytes": doc.get("size_bytes"),
                            "upload_date": doc.get("upload_date")
                        })
                
                enriched_report = {
                    **report,
                    "generator_name": f"{generator.get('first_name', '')} {generator.get('last_name', '')}".strip(),
                    "documents": associated_docs
                }
                investor_statements.append(enriched_report)
        
        return json.dumps(investor_statements)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_investor_statements",
                "description": "Access periodic statements including performance, holdings, and transaction summaries",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "relations_investor_id": {"type": "string", "description": "ID of the investor"},
                        "report_type": {"type": "string", "description": "Filter by report type (performance, holding, financial)"},
                        "start_date": {"type": "string", "description": "Start date for reports (YYYY-MM-DD format)"},
                        "end_date": {"type": "string", "description": "End date for reports (YYYY-MM-DD format)"}
                    },
                    "required": ["relations_investor_id"]
                }
            }
        }
