import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class ObtainInvestorProfile(Tool):
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
                "name": "obtain_investor_profile",
                                "description": "Obtain detailed profile information for a specific investor",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {"type": "string", "description": "ID of the investor"}
                    },
                    "required": ["investor_id"]
                }
            }
        }
