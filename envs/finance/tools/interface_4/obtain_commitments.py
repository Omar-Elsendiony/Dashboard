import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class ObtainCommitments(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: Optional[str] = None,
               investor_id: Optional[str] = None, status: Optional[str] = None) -> str:
        commitments = data.get("commitments", {})
        results = []
        
        for commitment in commitments.values():
            if fund_id and commitment.get("fund_id") != fund_id:
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
                "name": "obtain_commitments",
                "description": "Obtain commitments with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "Filter by fund ID"},
                        "investor_id": {"type": "string", "description": "Filter by investor ID"},
                        "status": {"type": "string", "description": "Filter by status (pending, fulfilled)"}
                    },
                    "required": []
                }
            }
        }
