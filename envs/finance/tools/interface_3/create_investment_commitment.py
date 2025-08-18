import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateInvestmentCommitment(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_id: str, commitment_fund_id: str, 
               commitment_amount: float, commitment_due_date: str, compliance_officer_approval: bool) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        investors = data.get("investors", {})
        funds = data.get("funds", {})
        commitments = data.get("commitments", {})
        
        # Validate investor exists
        if str(investor_id) not in investors:
            return json.dumps({"success": False, "message": "Investor not found"})
        
        # Validate fund exists
        if str(commitment_fund_id) not in funds:
            return json.dumps({"success": False, "message": "Fund not found"})
        
        # Validate compliance approval
        if not compliance_officer_approval:
            return json.dumps({"success": False, "message": "Compliance officer approval required"})
        
        # Validate commitment_amount
        if commitment_amount <= 0:
            return json.dumps({"success": False, "message": "Amount must be positive"})
        
        commitment_id = generate_id(commitments)
        timestamp = "2025-10-01T00:00:00"
        
        new_commitment = {
            "commitment_id": commitment_id,
            "commitment_fund_id": commitment_fund_id,
            "investor_id": investor_id,
            "commitment_amount": commitment_amount,
            "commitment_date": commitment_due_date,
            "commitment_status": "pending", # Initial commitment_status and the commitment_status can be updated later to fulfilled
            "updated_at": timestamp
        }
        
        commitments[str(commitment_id)] = new_commitment
        return json.dumps({"commitment_id": str(commitment_id), "success": True, "commitment_status": "Pending"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_commitment",
                "description": "Create a new commitment for an investor to a fund",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {"type": "string", "description": "ID of the investor"},
                        "commitment_fund_id": {"type": "string", "description": "ID of the fund"},
                        "commitment_amount": {"type": "number", "description": "Commitment commitment_amount"},
                        "commitment_due_date": {"type": "string", "description": "Due date for the commitment"},
                        "compliance_officer_approval": {"type": "boolean", "description": "Compliance Officer approval flag (True/False)"}
                    },
                    "required": ["investor_id", "commitment_fund_id", "commitment_amount", "commitment_due_date", "compliance_officer_approval"]
                }
            }
        }
