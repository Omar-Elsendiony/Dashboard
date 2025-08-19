import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdateNavRecordValue(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], nav_id: str, nav_value: str) -> str:
        nav_records = data.get("nav_records", {})
        
        # Validate NAV record exists
        if str(nav_id) not in nav_records:
            raise ValueError(f"NAV record {nav_id} not found")
        
        nav_record = nav_records[str(nav_id)]
        old_value = nav_record.get("nav_value")
        
        # Update NAV value and timestamp
        nav_record["nav_value"] = nav_value
        nav_record["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps({
            "nav_id": str(nav_id),
            "fund_id": nav_record.get("fund_id"),
            "nav_date": nav_record.get("nav_date"),
            "old_nav_value": old_value,
            "new_nav_value": nav_value,
            "updated_at": nav_record.get("updated_at")
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_nav_record_value",
                "description": "Update NAV record value for valuation adjustments",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "nav_id": {"type": "string", "description": "ID of the NAV record to update"},
                        "nav_value": {"type": "string", "description": "New NAV value"}
                    },
                    "required": ["nav_id", "nav_value"]
                }
            }
        }
