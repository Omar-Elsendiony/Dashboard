import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class ProcessRedemption(Tool):
    """
    A tool to process and update the status of a redemption request.
    """

    @staticmethod
    def invoke(data: Dict[str, Any], redemption_id: str, status: str, 
               compliance_officer_approval: bool, finance_officer_approval: bool,
               processed_date: Optional[str] = None) -> str:
        """
        Processes a redemption request by updating its status.

        Args:
            data: The database json.
            redemption_id: The ID of the redemption to process.
            status: The new status for the redemption.
            compliance_officer_approval: Compliance Officer approval (required).
            finance_officer_approval: Finance Officer approval (required).
            processed_date: The date the redemption was processed.

        Returns:
            A json string representing the updated redemption record or an error.
        """
        redemptions = data.get("redemptions", {})

        # Validate required approvals first
        if not compliance_officer_approval:
            return json.dumps({
                "success": False,
                "error": "Compliance Officer approval is required for redemption processing"
            })
        
        if not finance_officer_approval:
            return json.dumps({
                "success": False,
                "error": "Finance Officer approval is required for redemption processing"
            })

        if redemption_id not in redemptions:
            return json.dumps({
                "success": False,
                "error": f"Redemption {redemption_id} not found"
            })

        valid_statuses = ["pending", "approved", "processed", "cancelled"]
        if status not in valid_statuses:
            return json.dumps({
                "success": False,
                "error": f"Invalid status. Must be one of {valid_statuses}"
            })

        if status == "processed" and not processed_date:
            return json.dumps({
                "success": False,
                "error": "processed_date is required when status is 'processed'"
            })

        redemption = redemptions[redemption_id]
        current_status = redemption.get("status", "").lower()
        
        # Validate status transitions
        if current_status == "processed" and status != "processed":
            return json.dumps({
                "success": False,
                "error": "Cannot change status of already processed redemption"
            })
        
        if current_status == "cancelled" and status != "cancelled":
            return json.dumps({
                "success": False,
                "error": "Cannot change status of cancelled redemption"
            })

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
                "name": "process_redemption",
                "description": "Processes a redemption request by updating its status in the fund management system. This tool manages the redemption lifecycle with comprehensive validation and regulatory compliance checks. Validates redemption existence, status transitions, and ensures proper authorization controls. Requires both Compliance Officer and Finance Officer approvals as mandated by regulatory redemption processing procedures to ensure proper dual authorization and compliance with investor protection regulations. Supports status updates including pending, approved, processed, and cancelled states with appropriate business logic validation. Essential for investor redemption lifecycle management, regulatory compliance, and maintaining accurate redemption records with complete audit trails.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "redemption_id": {
                            "type": "string",
                            "description": "Unique identifier of the redemption request to process (required, must exist in system)"
                        },
                        "status": {
                            "type": "string",
                            "description": "The new status of the redemption (required). Allowed values: 'pending', 'approved', 'processed', 'cancelled'. Status transitions are validated to prevent invalid state changes."
                        },
                        "compliance_officer_approval": {
                            "type": "boolean",
                            "description": "Compliance Officer approval presence (True/False) (required for redemption processing as mandated by regulatory procedures)"
                        },
                        "finance_officer_approval": {
                            "type": "boolean",
                            "description": "Finance Officer approval presence (True/False) (required for redemption processing as mandated by regulatory procedures)"
                        },
                        "processed_date": {
                            "type": "string",
                            "description": "The date the redemption was processed in YYYY-MM-DD format (required when status is 'processed', optional for other statuses)"
                        }
                    },
                    "required": ["redemption_id", "status", "compliance_officer_approval", "finance_officer_approval"]
                }
            }
        }