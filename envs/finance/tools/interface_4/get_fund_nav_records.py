import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetFundNavRecords(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], analysis_fund_id: Optional[str] = None,
               start_date: Optional[str] = None, end_date: Optional[str] = None,
               nav_date: Optional[str] = None) -> str:
        nav_records = data.get("nav_records", {})
        results = []
        
        for nav_record in nav_records.values():
            if analysis_fund_id and nav_record.get("analysis_fund_id") != analysis_fund_id:
                continue
            if nav_date and nav_record.get("nav_date") != nav_date:
                continue
            if start_date and nav_record.get("nav_date", "") < start_date:
                continue
            if end_date and nav_record.get("nav_date", "") > end_date:
                continue
            results.append(nav_record)
        
        # Sort by nav_date descending (most recent first)
        results.sort(key=lambda x: x.get("nav_date", ""), reverse=True)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_nav_records",
                "description": "Get NAV records for analysis_performance tracking and reporting",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "analysis_fund_id": {"type": "string", "description": "Filter by fund ID"},
                        "start_date": {"type": "string", "description": "Filter NAV records from this date onwards"},
                        "end_date": {"type": "string", "description": "Filter NAV records up to this date"},
                        "nav_date": {"type": "string", "description": "Filter by specific NAV date"}
                    },
                    "required": []
                }
            }
        }
