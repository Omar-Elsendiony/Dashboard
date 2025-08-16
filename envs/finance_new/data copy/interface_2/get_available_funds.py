import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetAvailableFunds(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_id: Optional[str] = None, 
               fund_type: Optional[str] = None, status: Optional[str] = None) -> str:
        funds = data.get("funds", {})
        investors = data.get("investors", {})
        results = []
        
        # If investor_id is provided, validate it exists
        if investor_id and str(investor_id) not in investors:
            raise ValueError(f"Investor {investor_id} not found")
        
        for fund in funds.values():
            # Filter by fund type if specified
            if fund_type and fund.get("fund_type") != fund_type:
                continue
            
            # Filter by status if specified (default to "open" if not specified)
            if status and fund.get("status") != status:
                continue
            elif not status and fund.get("status") != "open":
                continue
            
            results.append(fund)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_available_funds",
                "description": "List all funds available for investment based on investor's accreditation and eligibility",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {"type": "string", "description": "ID of the investor (optional)"},
                        "fund_type": {"type": "string", "description": "Filter by fund type"},
                        "status": {"type": "string", "description": "Filter by fund status (open, closed)"}
                    },
                    "required": []
                }
            }
        }
