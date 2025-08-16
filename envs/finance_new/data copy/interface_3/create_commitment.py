import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateCommitment(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str, investor_id: str,
               commitment_amount: str, commitment_date: str, 
               status: str = "pending") -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        funds = data.get("funds", {})
        investors = data.get("investors", {})
        commitments = data.get("commitments", {})
        
        # Validate fund exists
        if str(fund_id) not in funds:
            raise ValueError(f"Fund {fund_id} not found")
        
        # Validate investor exists
        if str(investor_id) not in investors:
            raise ValueError(f"Investor {investor_id} not found")
        
        # Validate status
        valid_statuses = ["pending", "fulfilled"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        commitment_id = generate_id(commitments)
        timestamp = "2025-10-01T00:00:00"
        
        new_commitment = {
            "commitment_id": commitment_id,
            "fund_id": fund_id,
            "investor_id": investor_id,
            "commitment_amount": commitment_amount,
            "commitment_date": commitment_date,
            "status": status,
            "updated_at": timestamp
        }
        
        commitments[str(commitment_id)] = new_commitment
        return json.dumps({"commitment_id": commitment_id})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_commitment",
                "description": "Create a new commitment for capital raising",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "ID of the fund"},
                        "investor_id": {"type": "string", "description": "ID of the investor"},
                        "commitment_amount": {"type": "string", "description": "Amount of the commitment"},
                        "commitment_date": {"type": "string", "description": "Date of the commitment"},
                        "status": {"type": "string", "description": "Status of commitment (pending, fulfilled), defaults to pending"}
                    },
                    "required": ["fund_id", "investor_id", "commitment_amount", "commitment_date"]
                }
            }
        }
