import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateAnalysisInstrument(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], analysis_instrument_id: str, analysis_field_name: str, field_value: Any, 
               compliance_review_approved: Optional[bool] = None) -> str:
        
        instruments = data.get("instruments", {})
        
        # Validate instrument exists
        if str(analysis_instrument_id) not in instruments:
            return json.dumps({"success": False, "message": "Instrument not found"})
        
        # Check if compliance review is required and missing
        if compliance_review_approved is False:
            return json.dumps({"success": False, "message": "Compliance review needed but not approved"})
        
        # Validate field name is provided
        if not analysis_field_name:
            return json.dumps({"success": False, "message": "Update failed: Field name is required"})
        
        instrument = instruments[str(analysis_instrument_id)]
        
        # Check if field exists in instrument
        if analysis_field_name not in instrument:
            return json.dumps({"success": False, "message": f"Update failed: Field '{analysis_field_name}' does not exist"})
        
        # Get old analysis_value and update with new analysis_value
        analysis_old_value = instrument[analysis_field_name]
        
        # Check if the analysis_value is actually changing
        if analysis_old_value == field_value:
            return json.dumps({
                "success": True,
                "message": "No update needed: Value is already set to the requested analysis_value",
                "analysis_instrument_id": analysis_instrument_id
            })
        
        # Update the field
        instrument[analysis_field_name] = field_value
        
        return json.dumps({
            "success": True,
            "message": "Instrument updated successfully",
            "analysis_instrument_id": analysis_instrument_id,
            "updated_field": analysis_field_name,
            "analysis_old_value": analysis_old_value,
            "analysis_new_value": field_value
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_instrument",
                "description": "Update a specific field of an instrument",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "analysis_instrument_id": {"type": "string", "description": "ID of the instrument"},
                        "analysis_field_name": {"type": "string", "description": "Name of the field to update (e.g., 'name', 'ticker', 'status')"},
                        "field_value": {"type": ["string", "number", "boolean"], "description": "New analysis_value for the specified field"},
                        "compliance_review_approved": {"type": "boolean", "description": "Whether compliance review is approved for this update (optional)"}
                    },
                    "required": ["analysis_instrument_id", "analysis_field_name", "field_value"]
                }
            }
        }