import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetRelationsInvestorProfile(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], relations_investor_id: str) -> str:
        investors = data.get("investors", {})
        
        # Validate investor exists
        if str(relations_investor_id) not in investors:
            raise ValueError(f"Investor {relations_investor_id} not found")
        
        investor = investors[str(relations_investor_id)]
        return json.dumps(investor)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_investor_profile",
                "description": "Retrieve complete investor profile information including KYC details, status, and contact information",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "relations_investor_id": {"type": "string", "description": "ID of the investor"}
                    },
                    "required": ["relations_investor_id"]
                }
            }
        }
