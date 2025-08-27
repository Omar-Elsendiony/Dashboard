import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class PostJobOpening(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], position_id: str) -> str:
        
        job_positions = data.get("job_positions", {})
        
        # Validate position exists
        if str(position_id) not in job_positions:
            raise ValueError(f"Position {position_id} not found")
        
        position = job_positions[str(position_id)]
        
        # Check if position is in draft status
        if position.get("status") != "draft":
            raise ValueError(f"Position must be in draft status to be posted. Current status: {position.get('status')}")
        
        # Update position status to open
        position["status"] = "open"
        position["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps({"success": True, "message": "Job posted successfully"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "post_job_opening",
                "description": "Post a job opening by changing status from draft to open",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "position_id": {"type": "string", "description": "Position ID to post"}
                    },
                    "required": ["position_id"]
                }
            }
        }
