import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CloseJobOpening(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], position_id: str) -> str:
        
        job_positions = data.get("job_positions", {})
        
        # Validate position exists
        if str(position_id) not in job_positions:
            raise ValueError(f"Position {position_id} not found")
        
        position = job_positions[str(position_id)]
        
        # Check if position is in open status
        if position.get("status") != "open":
            raise ValueError(f"Position must be in open status to be closed. Current status: {position.get('status')}")
        
        # Update position status to closed
        position["status"] = "closed"
        position["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps({"success": True, "message": "Job closed successfully"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "close_job_opening",
                "description": "Close a job opening by changing status from open to closed",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "position_id": {"type": "string", "description": "Position ID to close"}
                    },
                    "required": ["position_id"]
                }
            }
        }
