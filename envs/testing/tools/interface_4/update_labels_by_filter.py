import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateLabelsByFilter(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], requesting_user_id: str,
               filter_space_id: Optional[str] = None, filter_name: Optional[str] = None,
               filter_color: Optional[str] = None, update_color: Optional[str] = None,
               update_description: Optional[str] = None) -> str:
        
        users = data.get("users", {})
        labels = data.get("labels", {})
        space_permissions = data.get("space_permissions", {})
        
        # Validate requesting user exists
        if str(requesting_user_id) not in users:
            return json.dumps({"error": "Requesting user not found"})
        
        requesting_user = users[str(requesting_user_id)]
        
        updated_labels = []
        timestamp = "2025-10-01T00:00:00"
        
        for label_id, label in labels.items():
            # Apply filters
            if filter_space_id and label.get("space_id") != filter_space_id:
                continue
            if filter_name and label.get("name") != filter_name:
                continue
            if filter_color and label.get("color") != filter_color:
                continue
            
            # Check permissions for this label
            has_permission = False
            space_id = label.get("space_id")
            
            # Platform Owner can update any label
            if requesting_user.get("role") == "PlatformOwner":
                has_permission = True
            # Label creator can update their own label
            elif label.get("created_by_user_id") == requesting_user_id:
                has_permission = True
            # Space admin can update labels in their space
            elif space_id:
                for perm in space_permissions.values():
                    if (perm.get("space_id") == space_id and 
                        perm.get("user_id") == requesting_user_id and 
                        perm.get("permission_type") == "moderate"):
                        has_permission = True
                        break
            
            if not has_permission:
                continue
            
            # Apply updates
            if update_color is not None:
                label["color"] = update_color
            if update_description is not None:
                label["description"] = update_description
            
            label["created_at"] = timestamp
            updated_labels.append(label)
        
        return json.dumps(updated_labels)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_labels_by_filter",
                "description": "Update labels based on filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "requesting_user_id": {"type": "string", "description": "ID of the user making the request"},
                        "filter_space_id": {"type": "string", "description": "Filter by space ID"},
                        "filter_name": {"type": "string", "description": "Filter by label name"},
                        "filter_color": {"type": "string", "description": "Filter by label color"},
                        "update_color": {"type": "string", "description": "New color to set"},
                        "update_description": {"type": "string", "description": "New description to set"}
                    },
                    "required": ["requesting_user_id"]
                }
            }
        }