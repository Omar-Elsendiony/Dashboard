import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class SubmitApprovalRequest(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], target_entity_type: str, target_entity_id: str,
               requested_by_user_id: str, reason: Optional[str] = None,
               due_at: Optional[str] = None, metadata: Optional[str] = None) -> str:
        """
        Create a new approval request workflow.
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
        users = data.get("users", {})
        spaces = data.get("spaces", {})
        pages = data.get("pages", {})
        
        # Validate user exists
        if requested_by_user_id not in users:
            return json.dumps({
                "success": False,
                "error": f"User {requested_by_user_id} not found"
            })
        
        # Validate target entity exists
        if target_entity_type == "space":
            if target_entity_id not in spaces:
                return json.dumps({
                    "success": False,
                    "error": f"Space {target_entity_id} not found"
                })
        elif target_entity_type == "page":
            if target_entity_id not in pages:
                return json.dumps({
                    "success": False,
                    "error": f"Page {target_entity_id} not found"
                })
        
        # Generate new request ID
        new_request_id = generate_id(approval_requests)
        timestamp = "2025-10-01T12:00:00"
        
        new_request = {
            "request_id": str(new_request_id),
            "target_entity_type": target_entity_type,
            "target_entity_id": target_entity_id,
            "requested_by_user_id": requested_by_user_id,
            "status": "pending",
            "reason": reason,
            "created_at": timestamp,
            "updated_at": None,
            "due_at": due_at,
            "metadata": metadata
        }
        
        approval_requests[str(new_request_id)] = new_request
        
        return json.dumps({
            "success": True,
            "request_id": str(new_request_id),
            "message": f"Approval request created for {target_entity_type} {target_entity_id}",
            "request_data": new_request
        })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "submit_approval_request",
                "description": "Create a new approval request workflow in the Confluence system. This tool initiates formal approval processes for content review or system changes requiring authorization. Creates approval request records with target entity specification, requester attribution, optional reasons, due dates, and custom metadata. Sets initial status as pending. Essential for workflow management, content governance, compliance processes, and collaborative review workflows.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "target_entity_type": {
                            "type": "string",
                            "description": "Type of entity requiring approval (required, e.g., 'page', 'space')"
                        },
                        "target_entity_id": {
                            "type": "string",
                            "description": "ID of the entity requiring approval (required)"
                        },
                        "requested_by_user_id": {
                            "type": "string",
                            "description": "User ID of the requester (required)"
                        },
                        "reason": {
                            "type": "string",
                            "description": "Reason for the approval request (optional)"
                        },
                        "due_at": {
                            "type": "string",
                            "description": "Due date for approval decision (optional, format: YYYY-MM-DDTHH:MM:SS)"
                        },
                        "metadata": {
                            "type": "string",
                            "description": "Additional metadata as JSON string (optional)"
                        }
                    },
                    "required": ["target_entity_type", "target_entity_id", "requested_by_user_id"]
                }
            }
        }
