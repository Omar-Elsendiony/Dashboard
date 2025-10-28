import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class HandleApprovalStep(Tool):
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
        
        # Generate timestamp that's always after the request creation and any existing decisions
        def _parse_timestamp(ts: str) -> datetime:
            """Parse timestamp in various formats."""
            if not ts:
                return datetime(2025, 10, 1, 12, 0, 0)
            try:
                # Handle timestamps with microseconds
                if '.' in ts:
                    return datetime.strptime(ts.split('.')[0], '%Y-%m-%dT%H:%M:%S')
                # Handle timestamps with timezone info
                elif '+' in ts or ts.endswith('Z'):
                    return datetime.strptime(ts.split('+')[0].split('Z')[0], '%Y-%m-%dT%H:%M:%S')
                else:
                    return datetime.strptime(ts, '%Y-%m-%dT%H:%M:%S')
            except:
                return datetime(2025, 10, 1, 12, 0, 0)
        
        # Start with request creation time as baseline
        base_timestamp = current_request.get("created_at", "2025-10-01T12:00:00")
        max_decision_time = _parse_timestamp(base_timestamp)
        
        # Find the latest decision for this request
        existing_decisions_for_request = [d for d in approval_decisions.values() 
                                           if isinstance(d, dict) and d.get("step_id") == request_id]
        
        for decision in existing_decisions_for_request:
            decided_at = decision.get("decided_at")
            if decided_at:
                decision_dt = _parse_timestamp(decided_at)
                if decision_dt > max_decision_time:
                    max_decision_time = decision_dt
        
        # New decision is always at least 1 second after the latest decision
        # Format to match existing data format: 2025-10-07T20:10:58.170905
        new_dt = max_decision_time + timedelta(seconds=1)
        decision_timestamp = new_dt.strftime('%Y-%m-%dT%H:%M:%S.%f')[:26]  # Keep 6 digits after decimal
        
        new_decision = {
            "decision_id": str(new_decision_id),
            "step_id": request_id,  # Using request_id as step_id for simplicity
            "approver_user_id": approver_user_id,
            "decision": decision,
            "comment": comment,
            "decided_at": decision_timestamp
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
        
        updated_request["updated_at"] = decision_timestamp
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
                "name": "handle_approval_step",
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
