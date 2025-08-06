import json
from datetime import datetime
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class update_commitment_details(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        commitment_id: str,
        commitment_amount: Optional[str] = None,
        status: Optional[str] = None
    ) -> str:
        commitments = data.get("commitments", {})

        # Ensure the record exists
        if str(commitment_id) not in commitments:
            raise ValueError(f"Commitment {commitment_id} not found")
        commitment = commitments[str(commitment_id)]

        # Update amount if provided
        if commitment_amount is not None:
            # Optionally validate numeric format here
            commitment["commitment_amount"] = commitment_amount

        # Update status if provided
        if status is not None:
            valid_statuses = ["pending", "fulfilled"]
            if status not in valid_statuses:
                raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
            commitment["status"] = status

        # Only bump the timestamp if we actually updated something
        if commitment_amount is not None or status is not None:
            commitment["updated_at"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

        return json.dumps(commitment)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_commitment_details",
                "description": (
                    "Update an existing commitment; only the provided fields "
                    "(commitment_amount and/or status) will change."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "commitment_id": {
                            "type": "string",
                            "description": "ID of the commitment to update"
                        },
                        "commitment_amount": {
                            "type": "string",
                            "description": "New commitment amount (optional)"
                        },
                        "status": {
                            "type": "string",
                            "description": "New status (pending or fulfilled; optional)"
                        }
                    },
                    "required": ["commitment_id"]
                }
            }
        }