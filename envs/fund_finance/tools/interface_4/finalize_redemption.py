import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class FinalizeRedemption(Tool):
    """
    A tool to process and update the status of a redemption request.
    """

    @staticmethod
    def invoke(data: Dict[str, Any], redemption_id: str, status: str, processed_date: Optional[str] = None) -> str:
        """
        Processes a redemption request by updating its status.

        Args:
            data: The database json.
            redemption_id: The ID of the redemption to process.
            status: The new status for the redemption.
            processed_date: The date the redemption was processed.

        Returns:
            A json string representing the updated redemption record or an error.
        """
        redemptions = data.get("redemptions", {})

        if redemption_id not in redemptions:
            return json.dumps({"error": f"Redemption {redemption_id} not found"})

        valid_statuses = ["pending", "approved", "processed", "cancelled"]
        if status not in valid_statuses:
            return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}"})

        if status == "processed" and not processed_date:
            return json.dumps({"error": "processed_date is required when status is 'processed'"})

        redemption = redemptions[redemption_id]
        redemption["status"] = status
        if processed_date:
            redemption["processed_date"] = processed_date
        redemption["updated_at"] = "2025-10-01T00:00:00"

        return json.dumps(redemption)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        """
        Returns the schema for the ProcessRedemption tool.
        """
        return {
            "type": "function",
            "function": {
                "name": "finalize_redemption",
                "description": "Processes a redemption request by updating its status.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "redemption_id": {
                            "type": "string",
                            "description": "ID of the redemption to process."
                        },
                        "status": {
                            "type": "string",
                            "description": "The new status of the redemption. Allowed values: pending, approved, processed, cancelled."
                        },
                        "processed_date": {
                            "type": "string",
                            "description": "The date the redemption was processed (YYYY-MM-DD). Required if status is 'processed'."
                        }
                    },
                    "required": ["redemption_id", "status"]
                }
            }
        }
