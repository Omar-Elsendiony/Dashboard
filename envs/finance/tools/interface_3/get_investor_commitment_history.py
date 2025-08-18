import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetInvestorCommitmentHistory(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_id: str, 
               commitment_status: Optional[str] = None, commitment_fund_id: Optional[str] = None) -> str:
        investors = data.get("investors", {})
        commitments = data.get("commitments", {})
        funds = data.get("funds", {})
        
        # Validate investor exists
        if str(investor_id) not in investors:
            raise ValueError(f"Investor {investor_id} not found")
        
        # Get commitments for this investor
        investor_commitments = []
        for commitment in commitments.values():
            if commitment.get("investor_id") == investor_id:
                # Filter by commitment_status if specified
                if commitment_status and commitment.get("commitment_status") != commitment_status:
                    continue
                
                # Filter by fund if specified
                if commitment_fund_id and commitment.get("commitment_fund_id") != commitment_fund_id:
                    continue
                
                # Enrich with fund details
                comm_fund_id = commitment.get("commitment_fund_id")
                fund_details = funds.get(str(comm_fund_id), {})
                
                enriched_commitment = {
                    **commitment,
                    "fund_name": fund_details.get("name"),
                    "fund_type": fund_details.get("fund_type")
                }
                investor_commitments.append(enriched_commitment)
        
        return json.dumps(investor_commitments)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_investor_commitments",
                "description": "Retrieve all capital commitments and their fulfillment commitment_status",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {"type": "string", "description": "ID of the investor"},
                        "commitment_status": {"type": "string", "description": "Filter by commitment commitment_status (pending, fulfilled)"},
                        "commitment_fund_id": {"type": "string", "description": "Filter by fund ID"}
                    },
                    "required": ["investor_id"]
                }
            }
        }
