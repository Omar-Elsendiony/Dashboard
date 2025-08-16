import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetInvestorCommitments(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_id: str, 
               status: Optional[str] = None, fund_id: Optional[str] = None) -> str:
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
                # Filter by status if specified
                if status and commitment.get("status") != status:
                    continue
                
                # Filter by fund if specified
                if fund_id and commitment.get("fund_id") != fund_id:
                    continue
                
                # Enrich with fund details
                comm_fund_id = commitment.get("fund_id")
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
                "description": "Retrieve all capital commitments and their fulfillment status",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {"type": "string", "description": "ID of the investor"},
                        "status": {"type": "string", "description": "Filter by commitment status (pending, fulfilled)"},
                        "fund_id": {"type": "string", "description": "Filter by fund ID"}
                    },
                    "required": ["investor_id"]
                }
            }
        }
