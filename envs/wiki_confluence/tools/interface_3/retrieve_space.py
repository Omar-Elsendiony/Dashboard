import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class RetrieveSpace(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], identifier: str, identifier_type: Optional[str] = "space_id") -> str:
        """
        Retrieve space details by ID or key.
        """
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format"
            })
        
        spaces = data.get("spaces", {})
        
        if identifier_type == "space_id":
            if identifier in spaces:
                space_data = spaces[identifier].copy()
                return json.dumps({
                    "success": True,
                    "space_data": space_data
                })
            else:
                return json.dumps({
                    "success": False,
                    "error": f"Space {identifier} not found"
                })
        elif identifier_type == "space_key":
            for space_id, space in spaces.items():
                if space.get("space_key") == identifier:
                    space_data = space.copy()
                    return json.dumps({
                        "success": True,
                        "space_data": space_data
                    })
            return json.dumps({
                "success": False,
                "error": f"Space with key '{identifier}' not found"
            })
        else:
            return json.dumps({
                "success": False,
                "error": f"Invalid identifier_type '{identifier_type}'. Must be 'space_id' or 'space_key'"
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "retrieve_space",
                "description": "Retrieve space details by ID or key in the Confluence system. This tool fetches comprehensive space information including space ID, space key, space name, purpose, creator, creation timestamp, and deletion status. Supports lookup by space ID or space key. Essential for space verification, content organization, and validating space existence before performing operations.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "identifier": {
                            "type": "string",
                            "description": "Space identifier - either space_id or space_key (required)"
                        },
                        "identifier_type": {
                            "type": "string",
                            "description": "Type of identifier (optional, defaults to 'space_id')",
                            "enum": ["space_id", "space_key"]
                        }
                    },
                    "required": ["identifier"]
                }
            }
        }
