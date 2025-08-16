import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetFilteredInvestors(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], accreditation_status: Optional[str] = None,
               status: Optional[str] = None, country: Optional[str] = None,
               source_of_funds: Optional[str] = None) -> str:
        
        investors = data.get("investors", {})
        results = []
        
        for investor in investors.values():
            if accreditation_status and investor.get("accreditation_status") != accreditation_status:
                continue
            if status and investor.get("status") != status:
                continue
            if country and investor.get("country") != country:
                continue
            if source_of_funds and investor.get("source_of_funds") != source_of_funds:
                continue
            results.append(investor)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_filtered_investors",
                "description": "Get filtered investors for CRM and marketing segmentation",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "accreditation_status": {"type": "string", "description": "Filter by accreditation status"},
                        "status": {"type": "string", "description": "Filter by status"},
                        "country": {"type": "string", "description": "Filter by country"},
                        "source_of_funds": {"type": "string", "description": "Filter by source of funds"}
                    },
                    "required": []
                }
            }
        }
