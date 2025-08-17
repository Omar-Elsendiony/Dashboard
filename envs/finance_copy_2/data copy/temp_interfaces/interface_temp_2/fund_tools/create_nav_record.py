import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateNavRecord(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str, nav_date: str, nav_value: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        funds = data.get("funds", {})
        nav_records = data.get("nav_records", {})
        
        # Validate fund exists
        if str(fund_id) not in funds:
            raise ValueError(f"Fund {fund_id} not found")
        
        # Check if NAV record already exists for this fund and date
        for nav_record in nav_records.values():
            if (nav_record.get("fund_id") == fund_id and 
                nav_record.get("nav_date") == nav_date):
                raise ValueError(f"NAV record already exists for fund {fund_id} on date {nav_date}")
        
        nav_id = generate_id(nav_records)
        timestamp = "2025-10-01T00:00:00"
        
        new_nav_record = {
            "nav_id": nav_id,
            "fund_id": fund_id,
            "nav_date": nav_date,
            "nav_value": nav_value,
            "updated_at": timestamp
        }
        
        nav_records[str(nav_id)] = new_nav_record
        return json.dumps({"nav_id": nav_id})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_nav_record",
                "description": "Create a new NAV record for daily valuation (regulatory requirement)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "ID of the fund"},
                        "nav_date": {"type": "string", "description": "Date of NAV calculation"},
                        "nav_value": {"type": "string", "description": "Net Asset Value"}
                    },
                    "required": ["fund_id", "nav_date", "nav_value"]
                }
            }
        }
