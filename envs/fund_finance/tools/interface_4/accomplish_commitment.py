import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class AccomplishCommitment(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], commitment_id: str) -> str:
        
        commitments = data.get("commitments", {})
        
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
                "name": "accomplish_commitment",
                "description": "Mark a commitment as fulfilled",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "commitment_id": {"type": "string", "description": "ID of the commitment to fulfill"}
                    },
                    "required": ["commitment_id"]
                }
            }
        }