import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GenerateCommitment(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str, investor_id: str, 
               commitment_amount: float, commitment_date: str, 
               status: str = "pending", compliance_officer_approval: bool = False) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        funds = data.get("funds", {})
        investors = data.get("investors", {})
        commitments = data.get("commitments", {})
        
        # Validate required approvals first
        if not compliance_officer_approval:
            return json.dumps({
                "success": False,
                "error": "Compliance Officer approval is required for commitment creation"
            })
        
        # Validate fund exists
        if str(fund_id) not in funds:
            return json.dumps({"error": f"Fund {fund_id} not found"})
        
        # Validate investor exists  
        if str(investor_id) not in investors:
            return json.dumps({"error": f"Investor {investor_id} not found"})
        
        # Validate status
        valid_statuses = ["pending", "fulfilled"]
        if status not in valid_statuses:
            return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}"})
        
        # Check if commitment already exists for this investor-fund combination
        for commitment in commitments.values():
            if (commitment.get("fund_id") == fund_id and 
                commitment.get("investor_id") == investor_id):
                return json.dumps({"error": "An investor can have only one commitment per fund"})
        
        commitment_id = generate_id(commitments)
        timestamp = "2025-10-01T00:00:00"
        
        new_commitment = {
            "commitment_id": str(commitment_id) if commitment_id is not None else None,
            "fund_id": str(fund_id) if fund_id is not None else None,
            "investor_id": str(investor_id) if investor_id is not None else None,
            "commitment_amount": commitment_amount,
            "commitment_date": commitment_date,
            "status": status,
            "updated_at": timestamp
        }
        
        commitments[str(commitment_id)] = new_commitment
        return json.dumps(new_commitment)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "generate_commitment",
                "description": "Create a new commitment for an investor to a fund. This tool establishes investment commitments with comprehensive validation and regulatory compliance checks. Validates fund and investor existence, ensures unique investor-fund combinations, and checks commitment status according to regulatory requirements. Prevents duplicate commitment creation by checking existing investor-fund combinations. Requires Compliance Officer approval as mandated by regulatory procedures for commitment creation. Essential for investment tracking, capital call management, and regulatory compliance in fund operations.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "ID of the fund"},
                        "investor_id": {"type": "string", "description": "ID of the investor"},
                        "commitment_amount": {"type": "number", "description": "Amount of the commitment"},
                        "commitment_date": {"type": "string", "description": "Date of commitment (YYYY-MM-DD)"},
                        "status": {"type": "string", "description": "Status of commitment (pending, fulfilled), defaults to pending"},
                        "compliance_officer_approval": {
                            "type": "boolean",
                            "description": "Compliance Officer approval presence (True/False) (required for commitment creation as mandated by regulatory procedures)"
                        }
                    },
                    "required": ["fund_id", "investor_id", "commitment_amount", "commitment_date", "compliance_officer_approval"]
                }
            }
        }