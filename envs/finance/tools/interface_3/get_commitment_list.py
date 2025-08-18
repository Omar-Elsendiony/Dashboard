import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetCommitmentList(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], commitment_fund_id: Optional[str] = None,
               investor_id: Optional[str] = None, commitment_status: Optional[str] = None) -> str:
        commitments = data.get("commitments", {})
        results = []
        
        for commitment in commitments.values():
            if commitment_fund_id and commitment.get("commitment_fund_id") != commitment_fund_id:
                continue
            if investor_id and commitment.get("investor_id") != investor_id:
                continue
            if commitment_status and commitment.get("commitment_status") != commitment_status:
                continue
            results.append(commitment)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_commitments",
                "description": "Get commitments with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "commitment_fund_id": {"type": "string", "description": "Filter by fund ID"},
                        "investor_id": {"type": "string", "description": "Filter by investor ID"},
                        "commitment_status": {"type": "string", "description": "Filter by commitment_status (pending, fulfilled)"}
                    },
                    "required": []
                }
            }
        }
