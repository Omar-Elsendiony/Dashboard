import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class AccessGroup(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], identifier: str, identifier_type: Optional[str] = "group_id") -> str:
        """
        Retrieve group details by ID or name.
        """
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format"
            })
        
        groups = data.get("groups", {})
        
        if identifier_type == "group_id":
            if identifier in groups:
                group_data = groups[identifier].copy()
                return json.dumps({
                    "success": True,
                    "group_data": group_data
                })
            else:
                return json.dumps({
                    "success": False,
                    "error": f"Group {identifier} not found"
                })
        elif identifier_type == "group_name":
            for group_id, group in groups.items():
                if group.get("group_name") == identifier:
                    group_data = group.copy()
                    return json.dumps({
                        "success": True,
                        "group_data": group_data
                    })
            return json.dumps({
                "success": False,
                "error": f"Group with name '{identifier}' not found"
            })
        else:
            return json.dumps({
                "success": False,
                "error": f"Invalid identifier_type '{identifier_type}'. Must be 'group_id' or 'group_name'"
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "access_group",
                "description": "Retrieve group details by ID or name in the Confluence system. This tool fetches comprehensive group information including group ID, group name, and creation timestamp. Supports lookup by group ID or group name. Essential for group verification, permission management, and validating group existence before performing operations.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "identifier": {
                            "type": "string",
                            "description": "Group identifier - either group_id or group_name (required)"
                        },
                        "identifier_type": {
                            "type": "string",
                            "description": "Type of identifier (optional, defaults to 'group_id')",
                            "enum": ["group_id", "group_name"]
                        }
                    },
                    "required": ["identifier"]
                }
            }
        }
