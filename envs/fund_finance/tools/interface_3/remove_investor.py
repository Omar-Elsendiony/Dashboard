import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class RemoveInvestor(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_id: str, reason: str = None) -> str:
        # Access investors data
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for investors"
            })
        
        investors = data.get("investors", {})
        
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
                "created_at": investor.get("created_at")
            }
        })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "remove_investor",
                "description": "Deactivates and archives an investor profile during the offboarding process. This tool should only be used after active subscriptions have been cancelled.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {
                            "type": "string",
                            "description": "investor ID to be offboarded"
                        },
                        "reason": {
                            "type": "string",
                            "description": "Optional reason for offboarding the investor"
                        }
                    },
                    "required": ["investor_id"]
                }
            }
        }