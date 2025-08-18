import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetInvestorProfile(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_id: str) -> str:
        investors = data.get("investors", {})
        
        # Validate investor exists
        if str(investor_id) not in investors:
            raise ValueError(f"Investor {investor_id} not found")
        
        investor = investors[str(investor_id)]
        return json.dumps(investor)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_investor_profile",
                "description": "Retrieve complete investor profile information including KYC details, investor_status, and contact information",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {"type": "string", "description": "ID of the investor"}
                    },
                    "required": ["investor_id"]
                }
            }
        }
