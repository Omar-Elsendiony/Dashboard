import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class CreateLabel(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], requesting_user_id: str, label_name: str,
               space_id: str, color: Optional[str] = None, description: Optional[str] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        users = data.get("users", {})
        labels = data.get("labels", {})
        spaces = data.get("spaces", {})
        space_permissions = data.get("space_permissions", {})
        
        # Validate user exists
        if str(requesting_user_id) not in users:
            return json.dumps({"error": "Requesting user not found"})
        
        # Validate space exists
        if str(space_id) not in spaces:
            return json.dumps({"error": "Space not found"})
        
        requesting_user = users[str(requesting_user_id)]
        
        # Check if label name already exists in space
        for label in labels.values():
            if (label.get("name").lower() == label_name.lower() and 
                label.get("space_id") == space_id):
                return json.dumps({"error": f"Label '{label_name}' already exists in this space"})
        
        # Check permissions - need contribute permission in space
        has_permission = False
        
        # Platform Owner can create labels anywhere
        if requesting_user.get("role") == "PlatformOwner":
            has_permission = True
        else:
            # Check space permissions
            for perm in space_permissions.values():
                if (perm.get("space_id") == space_id and 
                    perm.get("user_id") == requesting_user_id and 
                    perm.get("permission_type") in ["contribute", "moderate"]):
                    has_permission = True
                    break
        
        if not has_permission:
            return json.dumps({"error": "Insufficient permissions to create label in space"})
        
        # Create label
        label_id = generate_id(labels)
        timestamp = "2025-10-01T00:00:00"
        
        new_label = {
            "label_id": int(label_id),
            "name": label_name,
            "color": color or "#007acc",
            "description": description,
            "space_id": space_id,
            "created_by_user_id": requesting_user_id,
            "usage_count": 0,
            "created_at": timestamp
        }
        
        labels[label_id] = new_label
        
        return json.dumps({
            "label_id": label_id,
            "success": True
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_label",
                "description": "Create a new label in a space",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "requesting_user_id": {"type": "string", "description": "ID of the user creating the label"},
                        "label_name": {"type": "string", "description": "Name of the label"},
                        "space_id": {"type": "string", "description": "ID of the space"},
                        "color": {"type": "string", "description": "Label color (hex format)"},
                        "description": {"type": "string", "description": "Label description"}
                    },
                    "required": ["requesting_user_id", "label_name", "space_id"]
                }
            }
        }