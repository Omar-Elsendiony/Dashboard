import json
from typing import Any, Dict, List, Optional
from tau_bench.envs.tool import Tool

class ManageLabels(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], page_id: str, requesting_user_id: str,
               add_labels: Optional[List[str]] = None, remove_labels: Optional[List[str]] = None,
               content_owner_approval: Optional[bool] = None, 
               space_administrator_approval: Optional[bool] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        pages = data.get("pages", {})
        users = data.get("users", {})
        labels = data.get("labels", {})
        page_labels = data.get("page_labels", {})
        spaces = data.get("spaces", {})
        space_permissions = data.get("space_permissions", {})
        page_permissions = data.get("page_permissions", {})
        
        # Validate page exists
        if str(page_id) not in pages:
            return json.dumps({"success": False, "error": f"Page {page_id} not found"})
        
        # Validate user exists
        if str(requesting_user_id) not in users:
            return json.dumps({"success": False, "error": f"User {requesting_user_id} not found"})
        
        page = pages[str(page_id)]
        user = users[str(requesting_user_id)]
        space_id = page.get("space_id")
        
        # Check permissions
        has_permission = False
        
        # Check if user is Platform Owner
        if user.get("role") == "PlatformOwner":
            has_permission = True
        
        # Check if user is Content Owner (created the page)
        elif page.get("created_by_user_id") == requesting_user_id:
            if content_owner_approval is True:
                has_permission = True
        
        # Check if user is Space Administrator
        elif space_id:
            for perm in space_permissions.values():
                if (perm.get("space_id") == space_id and 
                    perm.get("user_id") == requesting_user_id and 
                    perm.get("permission_type") == "moderate"):
                    if space_administrator_approval is True:
                        has_permission = True
                    break
        
        if not has_permission:
            return json.dumps({"success": False, "error": "Insufficient permissions to manage labels"})
        
        # Get current labels for the page
        current_label_ids = []
        for page_label in page_labels.values():
            if page_label.get("page_id") == page_id:
                current_label_ids.append(page_label.get("label_id"))
        
        timestamp = "2025-10-01T00:00:00"
        
        # Remove labels
        if remove_labels:
            for label_name in remove_labels:
                label_id = None
                for lid, label in labels.items():
                    if label.get("name") == label_name:
                        label_id = lid
                        break
                
                if label_id and label_id in current_label_ids:
                    # Remove the page_label entry
                    to_remove = []
                    for pl_id, page_label in page_labels.items():
                        if (page_label.get("page_id") == page_id and 
                            page_label.get("label_id") == label_id):
                            to_remove.append(pl_id)
                    
                    for pl_id in to_remove:
                        del page_labels[pl_id]
                    
                    current_label_ids.remove(label_id)
        
        # Add labels
        if add_labels:
            for label_name in add_labels:
                label_id = None
                for lid, label in labels.items():
                    if label.get("name") == label_name:
                        label_id = lid
                        break
                
                if not label_id:
                    # Create new label
                    label_id = str(generate_id(labels))
                    labels[label_id] = {
                        "label_id": int(label_id),
                        "name": label_name,
                        "color": "#000000",
                        "description": None,
                        "space_id": space_id,
                        "created_by_user_id": requesting_user_id,
                        "usage_count": 0,
                        "created_at": timestamp
                    }
                
                if label_id not in current_label_ids:
                    # Add page_label entry
                    page_label_id = generate_id(page_labels)
                    page_labels[str(page_label_id)] = {
                        "page_label_id": page_label_id,
                        "page_id": page_id,
                        "label_id": label_id,
                        "added_at": timestamp,
                        "added_by_user_id": requesting_user_id
                    }
                    current_label_ids.append(label_id)
        
        # Get current label names
        current_label_names = []
        for label_id in current_label_ids:
            if str(label_id) in labels:
                current_label_names.append(labels[str(label_id)].get("name"))
        
        return json.dumps({
            "success": True,
            "message": "Labels updated",
            "current_labels": current_label_names
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manage_labels",
                "description": "Add or remove labels from a page",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "page_id": {"type": "string", "description": "ID of the page"},
                        "requesting_user_id": {"type": "string", "description": "ID of the user managing labels"},
                        "add_labels": {"type": "array", "items": {"type": "string"}, "description": "Labels to add (optional)"},
                        "remove_labels": {"type": "array", "items": {"type": "string"}, "description": "Labels to remove (optional)"},
                        "content_owner_approval": {"type": "boolean", "description": "Content Owner approval if user is Content Owner (True/False)"},
                        "space_administrator_approval": {"type": "boolean", "description": "Space Administrator approval if user is Space Admin (True/False)"}
                    },
                    "required": ["page_id", "requesting_user_id"]
                }
            }
        }
