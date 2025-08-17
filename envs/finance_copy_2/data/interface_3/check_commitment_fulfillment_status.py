import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CheckCommitmentFulfillmentStatus(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], commitment_id: str) -> str:
        commitments = data.get("commitments", {})
        subscriptions = data.get("subscriptions", {})
        
        # Validate commitment exists
        if str(commitment_id) not in commitments:
            raise ValueError(f"Commitment {commitment_id} not found")
        
        commitment = commitments[str(commitment_id)]
        commitment_amount = float(commitment.get("commitment_amount", 0))
        fund_id = commitment.get("fund_id")
        investor_id = commitment.get("investor_id")
        
        # Calculate fulfilled amount from approved subscriptions
        fulfilled_amount = 0
        related_subscriptions = []
        
        for subscription in subscriptions.values():
            if (subscription.get("fund_id") == fund_id and 
                subscription.get("investor_id") == investor_id and
                subscription.get("status") == "approved"):
                fulfilled_amount += float(subscription.get("amount", 0))
                related_subscriptions.append(subscription["subscription_id"])
        
        # Calculate fulfillment percentage
        fulfillment_percentage = (fulfilled_amount / commitment_amount * 100) if commitment_amount > 0 else 0
        
        # Determine if fully fulfilled
        is_fully_fulfilled = fulfillment_percentage >= 100
        
        result = {
            "commitment_id": commitment_id,
            "commitment_amount": commitment_amount,
            "fulfilled_amount": fulfilled_amount,
            "remaining_amount": commitment_amount - fulfilled_amount,
            "fulfillment_percentage": round(fulfillment_percentage, 2),
            "is_fully_fulfilled": is_fully_fulfilled,
            "status": commitment.get("status"),
            "related_subscriptions": related_subscriptions
        }
        
        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "check_commitment_fulfillment_status",
                "description": "Check the fulfillment status of a commitment including calculation of fulfilled amounts",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "commitment_id": {"type": "string", "description": "ID of the commitment to check"}
                    },
                    "required": ["commitment_id"]
                }
            }
        }
