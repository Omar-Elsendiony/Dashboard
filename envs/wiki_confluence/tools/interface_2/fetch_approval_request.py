import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class FetchApprovalRequest(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], request_id: str) -> str:
        """
        Retrieve an approval request by ID.
        """
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format"
            })
        
        approval_requests = data.get("approval_requests", {})
        approval_decisions = data.get("approval_decisions", {})
        
        if request_id not in approval_requests:
            return json.dumps({
                "success": False,
                "error": f"Approval request {request_id} not found"
            })
        
        request_data = approval_requests[request_id].copy()
        
        # Find all decisions for this request
        related_decisions = []
        for decision_id, decision in approval_decisions.items():
            if decision.get("step_id") == request_id:
                related_decisions.append(decision.copy())
        
        # Sort decisions by decided_at
        related_decisions.sort(key=lambda x: x.get("decided_at", ""))
        
        return json.dumps({
            "success": True,
            "request_data": request_data,
            "decisions": related_decisions,
            "decision_count": len(related_decisions)
        })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "fetch_approval_request",
                "description": "Retrieve an approval request by ID in the Confluence system. This tool fetches comprehensive approval request details including request ID, target entity information, requester, status, reason, timestamps, due dates, metadata, and all associated approval decisions. Returns complete workflow state with decision history sorted chronologically. Essential for workflow tracking, approval status monitoring, and understanding approval request outcomes.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "request_id": {
                            "type": "string",
                            "description": "Unique identifier of the approval request (required)"
                        }
                    },
                    "required": ["request_id"]
                }
            }
        }
