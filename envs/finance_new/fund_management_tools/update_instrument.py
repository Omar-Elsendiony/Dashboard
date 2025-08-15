import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateInstrument(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], instrument_id: str, proposed_changes: Dict[str, Any], 
               user_authorization: bool, compliance_review_required: Optional[bool] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        instruments = data.get("instruments", {})
        users = data.get("users", {})
        audit_trails = data.get("audit_trails", {})
        
        # Validate instrument exists
        if str(instrument_id) not in instruments:
            return json.dumps({"success": False, "message": "Instrument not found", "halt": True})
        
        # Validate user authorization
        if not user_authorization:
            return json.dumps({"success": False, "message": "User authorization required", "halt": True})
        
        # Validate proposed changes
        if not proposed_changes or not isinstance(proposed_changes, dict):
            return json.dumps({"success": False, "message": "Valid proposed changes required", "halt": True})
        
        instrument = instruments[str(instrument_id)]
        
        # Check current status and validate action
        current_status = instrument.get("status", "active")
        if action.lower() == "deactivate" and current_status == "inactive":
            return json.dumps({"success": False, "message": "Instrument is already inactive", "halt": True})
        elif action.lower() == "reactivate" and current_status == "active":
            return json.dumps({"success": False, "message": "Instrument is already active", "halt": True})
        
        # Find an admin user to perform the action
        admin_user = None
        for user_id, user in users.items():
            if user.get("role") == "admin":
                admin_user = user_id
                break
        
        if not admin_user:
            return json.dumps({"success": False, "message": "No authorized user found to perform action", "halt": True})
        
        # Update instrument status
        old_status = instrument.get("status")
        new_status = "inactive" if action.lower() == "deactivate" else "active"
        instrument["status"] = new_status
        
        # Create audit trail entry
        audit_id = generate_id(audit_trails)
        timestamp = "2025-10-01T00:00:00"
        
        audit_entry = {
            "audit_trail_id": audit_id,
            "reference_id": instrument_id,
            "reference_type": "instrument",
            "action": action.lower(),
            "user_id": admin_user,
            "field_name": "status",
            "old_value": old_status,
            "new_value": new_status,
            "created_at": timestamp
        }
        audit_trails[str(audit_id)] = audit_entry
        
        action_past = "Deactivated" if action.lower() == "deactivate" else "Reactivated"
        return json.dumps({
            "success": True, 
            "message": f"Instrument {action_past}", 
            "instrument_id": instrument_id
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "deactivate_reactivate_instrument",
                "description": "Deactivate or reactivate an instrument",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "instrument_id": {"type": "string", "description": "ID of the instrument"},
                        "action": {"type": "string", "description": "Action to perform: deactivate or reactivate"},
                        "reason": {"type": "string", "description": "Reason for the action"},
                        "fund_manager_approval": {"type": "boolean", "description": "Fund Manager approval flag"},
                        "compliance_officer_approval": {"type": "boolean", "description": "Compliance Officer approval flag"}
                    },
                    "required": ["instrument_id", "action", "reason", "fund_manager_approval", "compliance_officer_approval"]
                }
            }
        }
