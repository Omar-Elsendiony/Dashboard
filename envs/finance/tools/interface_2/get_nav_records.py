import json
from datetime import datetime
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class get_nav_records(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        nav_id: Optional[str] = None,
        fund_id: Optional[str] = None,
        period_start: Optional[str] = None,
        period_end: Optional[str] = None
    ) -> str:
        nav_records = data.get("nav_records", {})
        results = []
        
        # Parse date bounds if provided
        start_dt = datetime.fromisoformat(period_start) if period_start else None
        end_dt = datetime.fromisoformat(period_end) if period_end else None

        for nav in nav_records.values():
            # Filter by nav_id
            if nav_id and str(nav.get("nav_id")) != str(nav_id):
                continue
            # Filter by fund_id
            if fund_id and str(nav.get("fund_id")) != str(fund_id):
                continue
            # Filter by date range
            nav_date = datetime.fromisoformat(str(nav.get("nav_date")))
            if start_dt and nav_date < start_dt:
                continue
            if end_dt and nav_date > end_dt:
                continue
            
            results.append(nav)

        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_nav_records",
                "description": (
                    "Fetch NAV records filtered by nav_id, fund_id, "
                    "and/or date range (period_start to period_end)."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "nav_id": {"type": "string", "description": "Exact NAV record ID"},
                        "fund_id": {"type": "string", "description": "Fund ID to filter by"},
                        "period_start": {"type": "string", "description": "Inclusive start date (YYYY-MM-DD)"},
                        "period_end": {"type": "string", "description": "Inclusive end date (YYYY-MM-DD)"}
                    },
                    "required": []
                }
            }
        }