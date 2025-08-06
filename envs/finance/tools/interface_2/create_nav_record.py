import json
from datetime import datetime
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class create_nav_record(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str, nav_date: str, 
               nav_value: float) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return '1'
            return str(max(int(k) for k in table.keys()) + 1)
        
        nav_records = data.get("nav_records", {})
        funds = data.get("funds", {})
        
        # Validate fund exists
        if str(fund_id) not in funds:
            raise ValueError(f"Fund with ID {fund_id} not found")
        
        nav_id = generate_id(nav_records)
        timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        
        new_nav = {
            "nav_id": str(nav_id),
            "fund_id": str(fund_id),
            "nav_date": nav_date,
            "nav_value": nav_value,
            "updated_at": timestamp
        }
        
        nav_records[str(nav_id)] = new_nav
        return json.dumps(new_nav)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_nav_record",
                "description": "Create a new NAV record for a fund",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "Fund ID"},
                        "nav_date": {"type": "string", "description": "NAV date in YYYY-MM-DD format"},
                        "nav_value": {"type": "number", "description": "NAV value"},
                    },
                    "required": ["fund_id", "nav_date", "nav_value"]
                }
            }
        }
