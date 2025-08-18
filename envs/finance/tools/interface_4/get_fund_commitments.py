import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetFundCommitments(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], analysis_fund_id: Optional[str] = None,
               investor_id: Optional[str] = None, status: Optional[str] = None) -> str:
        commitments = data.get("commitments", {})
        results = []
        
        for commitment in commitments.values():
            if analysis_fund_id and commitment.get("analysis_fund_id") != analysis_fund_id:
                continue
            if investor_id and commitment.get("investor_id") != investor_id:
                continue
            if status and commitment.get("status") != status:
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
                        "analysis_fund_id": {"type": "string", "description": "Filter by fund ID"},
                        "investor_id": {"type": "string", "description": "Filter by investor ID"},
                        "status": {"type": "string", "description": "Filter by status (pending, fulfilled)"}
                    },
                    "required": []
                }
            }
        }
