import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class ExecuteApprovalStep(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], request_id: str, approver_user_id: str,
               decision: str, comment: Optional[str] = None) -> str:
        """
        Approve or reject an approval request.
        """
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format"
            })
        
        approval_requests = data.get("approval_requests", {})
        approval_decisions = data.get("approval_decisions", {})
        users = data.get("users", {})
        
        # Validate user exists
        if approver_user_id not in users:
            return json.dumps({
                "success": False,
                "error": f"User {approver_user_id} not found"
            })
        
        # Validate request exists
        if request_id not in approval_requests:
            return json.dumps({
                "success": False,
                "error": f"Approval request {request_id} not found"
            })
        
        # Validate decision enum
        valid_decisions = ["approve", "reject", "escalate", "cancel"]
        if decision not in valid_decisions:
            return json.dumps({
                "success": False,
                "error": f"Invalid decision. Must be one of: {', '.join(valid_decisions)}"
            })
        
        # Check if request is still pending
        current_request = approval_requests[request_id]
        if current_request.get("status") not in ["pending", "in_review"]:
            return json.dumps({
                "success": False,
                "error": f"Approval request {request_id} is not in a state that can be decided. Current status: {current_request.get('status')}"
            })
        
        # Generate new decision ID
        new_decision_id = generate_id(approval_decisions)
        timestamp = "2025-10-01T12:00:00"
        
        new_decision = {
            "decision_id": str(new_decision_id),
            "step_id": request_id,  # Using request_id as step_id for simplicity
            "approver_user_id": approver_user_id,
            "decision": decision,
            "comment": comment,
            "decided_at": timestamp
        }
        
        approval_decisions[str(new_decision_id)] = new_decision
        
        # Update request status based on decision
        updated_request = current_request.copy()
        if decision == "approve":
            updated_request["status"] = "approved"
        elif decision == "reject":
            updated_request["status"] = "rejected"
        elif decision == "cancel":
            updated_request["status"] = "cancelled"
        elif decision == "escalate":
            updated_request["status"] = "in_review"
        
        updated_request["updated_at"] = timestamp
        approval_requests[request_id] = updated_request
        
        return json.dumps({
            "success": True,
            "decision_id": str(new_decision_id),
            "request_id": request_id,
            "new_status": updated_request["status"],
            "message": f"Approval request {request_id} {decision}d by user {approver_user_id}",
            "decision_data": new_decision,
            "request_data": updated_request
        })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "execute_approval_step",
                "description": "Record a user's formal decision on an approval request in the Confluence system. This tool processes approval workflow decisions by recording approver responses (approve, reject, escalate, cancel) with optional comments and updating request status accordingly. Validates approver authorization and request state before recording decisions. Essential for workflow completion, governance enforcement, collaborative review processes, and maintaining decision audit trails.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "request_id": {
                            "type": "string",
                            "description": "ID of the approval request (required)"
                        },
                        "approver_user_id": {
                            "type": "string",
                            "description": "User ID of the approver making the decision (required)"
                        },
                        "decision": {
                            "type": "string",
                            "description": "Decision on the approval request (required)",
                            "enum": ["approve", "reject", "escalate", "cancel"]
                        },
                        "comment": {
                            "type": "string",
                            "description": "Optional comment explaining the decision"
                        }
                    },
                    "required": ["request_id", "approver_user_id", "decision"]
                }
            }
        }
