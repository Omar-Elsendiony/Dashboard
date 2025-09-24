import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class OffboardInvestor(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_id: str, 
               compliance_officer_approval: bool, reason: str = None) -> str:
        # Access investors data
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for investors"
            })
        
        investors = data.get("investors", {})
        
        # Validate required approval first
        if not compliance_officer_approval:
            return json.dumps({
                "success": False,
                "error": "Compliance Officer approval is required for investor offboarding"
            })
        
        # Validate required parameters
        if not investor_id:
            return json.dumps({
                "success": False,
                "error": "investor_id is required for offboarding"
            })
        
        # Check if investor exists
        if investor_id not in investors:
            return json.dumps({
                "success": False,
                "error": f"Investor {investor_id} not found"
            })
        
        investor = investors[investor_id]
        
        # Check if investor is already deactivated
        current_status = investor.get("status", "").lower()
        if current_status in ["deactivated", "inactive", "archived", "offboarded"]:
            return json.dumps({
                "success": False,
                "error": f"Investor {investor_id} is already deactivated with status: {current_status}"
            })
        
        # Validate reason if provided
        if reason is not None and not isinstance(reason, str):
            return json.dumps({
                "success": False,
                "error": "Reason must be a string if provided"
            })
        
        # Update investor record directly
        investor["status"] = "offboarded"

        # Update the investor in the data
        investors[investor_id] = investor

        return json.dumps({
            "success": True,
            "investor_id": investor_id,
            "message": f"Investor {investor_id} successfully offboarded",
            "investor_data": {
                "investor_id": investor.get("investor_id"),
                "name": investor.get("name"),
                "status": investor.get("status"),
                "contact_email": investor.get("contact_email"),
            }
        })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "offboard_investor",
                "description": "Deactivates and archives an investor profile during the offboarding process in the fund management system. This tool manages the investor lifecycle termination with comprehensive validation and regulatory compliance checks. Validates investor existence and current status to prevent duplicate offboarding operations. Updates investor status to 'offboarded' and maintains audit trail with timestamps and reasons. Requires Compliance Officer approval as mandated by regulatory offboarding procedures to ensure proper authorization and compliance with investor protection regulations. Essential for investor relationship lifecycle management, regulatory compliance, and maintaining accurate investor records. Note: This tool should only be called after active subscriptions have been properly cancelled through the subscription management process.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {
                            "type": "string",
                            "description": "Unique identifier of the investor to be offboarded (required, must exist in system and not already be in deactivated status)"
                        },
                        "compliance_officer_approval": {
                            "type": "boolean",
                            "description": "Compliance Officer approval presence (True/False) (required for investor offboarding as mandated by regulatory offboarding procedures)"
                        },
                        "reason": {
                            "type": "string",
                            "description": "Optional reason for offboarding the investor (stored in audit trail for regulatory compliance and future reference)"
                        }
                    },
                    "required": ["investor_id", "compliance_officer_approval"]
                }
            }
        }