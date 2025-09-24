import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class FulfillCommitment(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], commitment_id: str, compliance_officer_approval: bool = False) -> str:
        
        commitments = data.get("commitments", {})
        
        # Validate required approvals first
        if not compliance_officer_approval:
            return json.dumps({
                "success": False,
                "error": "Compliance Officer approval is required for commitment fulfillment"
            })
        
        # Validate commitment exists
        if str(commitment_id) not in commitments:
            return json.dumps({"error": f"Commitment {commitment_id} not found"})
        
        commitment = commitments[str(commitment_id)]
        
        # Check if already fulfilled
        if commitment.get("status") == "fulfilled":
            return json.dumps({"error": "Commitment is already fulfilled"})
        
        # Update commitment status
        timestamp = "2025-10-01T00:00:00"
        commitment["status"] = "fulfilled"
        commitment["updated_at"] = timestamp
        
        return json.dumps(commitment)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "fulfill_commitment",
                "description": "Mark a commitment as fulfilled. This tool updates commitment status to fulfilled with comprehensive validation and regulatory compliance checks. Validates commitment existence and current status to prevent duplicate fulfillment. Requires Compliance Officer approval as mandated by regulatory procedures for commitment status changes. Essential for accurate investment tracking, capital call processing, and regulatory compliance in fund operations. Ensures proper audit trail and status management throughout the investment lifecycle.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "commitment_id": {
                            "type": "string", 
                            "description": "ID of the commitment to fulfill"
                        },
                        "compliance_officer_approval": {
                            "type": "boolean",
                            "description": "Compliance Officer approval presence (True/False) (required for commitment fulfillment as mandated by regulatory procedures)"
                        }
                    },
                    "required": ["commitment_id", "compliance_officer_approval"]
                }
            }
        }