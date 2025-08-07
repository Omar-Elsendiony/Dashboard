import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class update_nav_record_value(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], nav_id: str, nav_value: float) -> str:
        nav_records = data.get("nav_records", {})
        
        # Validate NAV record exists
        if str(nav_id) not in nav_records:
            raise ValueError(f"NAV record with ID {nav_id} not found")
        
        # Update NAV record
        nav_records[str(nav_id)]["nav_value"] = nav_value
        nav_records[str(nav_id)]["updated_at"] = "2025-08-07T00:00:00Z"
        
        return json.dumps(nav_records[str(nav_id)])

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_nav_record_value",
                "description": "Update an existing NAV record",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "nav_id": {"type": "string", "description": "NAV record ID"},
                        "nav_value": {"type": "number", "description": "New NAV value"},
                    },
                    "required": ["nav_id", "nav_value"]
                }
            }
        }
