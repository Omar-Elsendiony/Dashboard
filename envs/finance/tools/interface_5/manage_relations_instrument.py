import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ManageRelationsInstrument(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], relations_instrument_id: str, relations_action: str,
               fund_manager_approval: bool, compliance_officer_approval: bool) -> str:
        
        if not fund_manager_approval:
            return json.dumps({"error": "Fund Manager approval required. Process halted."})
        
        if not compliance_officer_approval:
            return json.dumps({"error": "Compliance Officer approval required. Process halted."})
        
        instruments = data.get("instruments", {})
        
        # Validate instrument exists
        if str(relations_instrument_id) not in instruments:
            return json.dumps({"error": f"Instrument {relations_instrument_id} not found"})
        
        # Validate relations_action
        if relations_action not in ["deactivate", "reactivate"]:
            return json.dumps({"error": "Action must be 'deactivate' or 'reactivate'"})
        
        instrument = instruments[str(relations_instrument_id)]
        
        # Update instrument status
        if relations_action == "deactivate":
            instrument["status"] = "inactive"
            message = "Instrument Deactivated"
        else:
            instrument["status"] = "active"
            message = "Instrument Reactivated"
        
        return json.dumps({
            "success": True, 
            "message": message,
            "relations_instrument_id": str(relations_instrument_id)
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
                        "relations_instrument_id": {"type": "string", "description": "ID of the instrument"},
                        "relations_action": {"type": "string", "description": "Action to perform (deactivate or reactivate)"},
                        "fund_manager_approval": {"type": "boolean", "description": "Fund Manager approval flag (True/False)"},
                        "compliance_officer_approval": {"type": "boolean", "description": "Compliance Officer approval flag (True/False)"}
                    },
                    "required": ["relations_instrument_id", "relations_action", "fund_manager_approval", "compliance_officer_approval"]
                }
            }
        }
