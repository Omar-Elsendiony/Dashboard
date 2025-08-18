import json
from typing import Any, Dict, Optional, Union
from tau_bench.envs.tool import Tool

class AdjustInstrument(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], instrument_id: str, field_name: str, field_value: Union[str, int, float, bool], 
               compliance_review_approved: Optional[bool] = None) -> str:
        
        instruments = data.get("instruments", {})
        
        # Validate instrument exists
        if str(instrument_id) not in instruments:
            return json.dumps({"success": False, "message": "Instrument not found"})
        
        # Check if compliance review is required and missing
        if compliance_review_approved is False:
            return json.dumps({"success": False, "message": "Compliance review needed but not approved"})
        
        # Validate field name is provided
        if not field_name:
            return json.dumps({"success": False, "message": "Update failed: Field name is required"})
        
        instrument = instruments[str(instrument_id)]
        
        # Check if field exists in instrument
        if field_name not in instrument:
            return json.dumps({"success": False, "message": f"Update failed: Field '{field_name}' does not exist"})
        
        # Get old value and update with new value
        old_value = instrument[field_name]
        
        # Check if the value is actually changing
        if old_value == field_value:
            return json.dumps({
                "success": True,
                "message": "No update needed: Value is already set to the requested value",
                "instrument_id": instrument_id
            })
        
        # Update the field
        instrument[field_name] = field_value
        
        return json.dumps({
            "success": True,
            "message": "Instrument updated successfully",
            "instrument_id": instrument_id,
            "updated_field": field_name,
            "old_value": old_value,
            "new_value": field_value
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "adjust_instrument",
                "description": "Update a specific field of an instrument",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "instrument_id": {"type": "string", "description": "ID of the instrument"},
                        "field_name": {"type": "string", "description": "Name of the field to update (e.g., 'name', 'ticker', 'status')"},
                        "field_value": {"type": ["string", "number", "boolean"], "description": "New value for the specified field"},
                        "compliance_review_approved": {"type": "boolean", "description": "Whether compliance review is approved for this update (optional)"}
                    },
                    "required": ["instrument_id", "field_name", "field_value"]
                }
            }
        }