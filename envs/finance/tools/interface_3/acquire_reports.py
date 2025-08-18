import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class AcquireReports(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: Optional[str] = None, 
               investor_id: Optional[str] = None, report_type: Optional[str] = None,
               status: Optional[str] = None) -> str:
        reports = data.get("reports", {})
        results = []
        
        for report in reports.values():
            if fund_id and report.get("fund_id") != fund_id:
                continue
            if investor_id and report.get("investor_id") != investor_id:
                continue
            if report_type and report.get("report_type") != report_type:
                continue
            if status and report.get("status") != status:
                continue
            results.append(report)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "acquire_reports",
                "description": "Acquire reports with optional filters for distribution and access",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "Filter by fund ID"},
                        "investor_id": {"type": "string", "description": "Filter by investor ID"},
                        "report_type": {"type": "string", "description": "Filter by report type (performance, holding, financial)"},
                        "status": {"type": "string", "description": "Filter by status (pending, completed, failed)"}
                    },
                    "required": []
                }
            }
        }
