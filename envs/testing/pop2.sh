#!/bin/bash

# Create manage_labels.py
cat > manage_labels.py << 'EOF'
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
EOF

# Create publish_draft_page.py
cat > publish_draft_page.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class PublishDraftPage(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], draft_page_id: str, requesting_user_id: str,
               publish_confirmation: bool) -> str:
        
        pages = data.get("pages", {})
        users = data.get("users", {})
        spaces = data.get("spaces", {})
        space_permissions = data.get("space_permissions", {})
        page_permissions = data.get("page_permissions", {})
        
        # Validate page exists
        if str(draft_page_id) not in pages:
            return json.dumps({"success": False, "error": f"Draft page {draft_page_id} not found"})
        
        # Validate user exists
        if str(requesting_user_id) not in users:
            return json.dumps({"success": False, "error": f"User {requesting_user_id} not found"})
        
        draft_page = pages[str(draft_page_id)]
        user = users[str(requesting_user_id)]
        
        # Check if page is actually a draft
        if draft_page.get("status") != "draft":
            return json.dumps({"success": False, "error": "Page is not a draft"})
        
        # Validate confirmation
        if not publish_confirmation:
            return json.dumps({"success": False, "error": "Publish confirmation required"})
        
        space_id = draft_page.get("space_id")
        
        # Check permissions
        has_permission = False
        
        # Check if user is Platform Owner
        if user.get("role") == "PlatformOwner":
            has_permission = True
        
        # Check if user is the page creator
        elif draft_page.get("created_by_user_id") == requesting_user_id:
            has_permission = True
        
        # Check if user has edit permission on the page
        else:
            for perm in page_permissions.values():
                if (perm.get("page_id") == draft_page_id and 
                    perm.get("user_id") == requesting_user_id and 
                    perm.get("permission_type") in ["edit", "admin"]):
                    has_permission = True
                    break
        
        # Check space-level permissions if no page-level permissions
        if not has_permission and space_id:
            for perm in space_permissions.values():
                if (perm.get("space_id") == space_id and 
                    perm.get("user_id") == requesting_user_id and 
                    perm.get("permission_type") in ["contribute", "moderate"]):
                    has_permission = True
                    break
        
        if not has_permission:
            return json.dumps({"success": False, "error": "Insufficient permissions to publish page"})
        
        # Update page status
        timestamp = "2025-10-01T00:00:00"
        draft_page["status"] = "current"
        draft_page["updated_at"] = timestamp
        draft_page["published_at"] = timestamp
        draft_page["last_modified_by_user_id"] = requesting_user_id
        
        return json.dumps({
            "success": True,
            "message": "Draft published",
            "page_id": draft_page_id,
            "status": "current"
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "publish_draft_page",
                "description": "Publish a draft page to make it current",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "draft_page_id": {"type": "string", "description": "ID of the draft page to publish"},
                        "requesting_user_id": {"type": "string", "description": "ID of the user publishing the page"},
                        "publish_confirmation": {"type": "boolean", "description": "Confirmation flag for publishing intent (True/False)"}
                    },
                    "required": ["draft_page_id", "requesting_user_id", "publish_confirmation"]
                }
            }
        }
EOF

# Create create_template.py
cat > create_template.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class CreateTemplate(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], template_name: str, template_content: str,
               requesting_user_id: str, is_global: bool, space_id: Optional[str] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        users = data.get("users", {})
        spaces = data.get("spaces", {})
        templates = data.get("page_templates", {})
        space_permissions = data.get("space_permissions", {})
        
        # Validate user exists
        if str(requesting_user_id) not in users:
            return json.dumps({"success": False, "error": f"User {requesting_user_id} not found"})
        
        user = users[str(requesting_user_id)]
        
        # Check permissions based on template type
        has_permission = False
        
        if is_global:
            # Only Platform Owner can create global templates
            if user.get("role") == "PlatformOwner":
                has_permission = True
        else:
            # For space-specific templates, validate space exists
            if not space_id:
                return json.dumps({"success": False, "error": "Space ID required for space-specific templates"})
            
            if str(space_id) not in spaces:
                return json.dumps({"success": False, "error": f"Space {space_id} not found"})
            
            # Check if user is Platform Owner, WikiProgramManager, or Space Administrator
            if user.get("role") in ["PlatformOwner", "WikiProgramManager"]:
                has_permission = True
            else:
                # Check if user is Space Administrator
                for perm in space_permissions.values():
                    if (perm.get("space_id") == space_id and 
                        perm.get("user_id") == requesting_user_id and 
                        perm.get("permission_type") == "moderate"):
                        has_permission = True
                        break
        
        if not has_permission:
            return json.dumps({"success": False, "error": "Insufficient permissions to create template"})
        
        # Create template
        template_id = str(generate_id(templates))
        timestamp = "2025-10-01T00:00:00"
        
        new_template = {
            "template_id": int(template_id),
            "name": template_name,
            "description": None,
            "content": template_content,
            "content_format": "wiki",
            "space_id": space_id if not is_global else None,
            "is_global": is_global,
            "category": None,
            "usage_count": 0,
            "created_at": timestamp,
            "updated_at": timestamp,
            "created_by_user_id": requesting_user_id
        }
        
        templates[template_id] = new_template
        
        scope = "global" if is_global else "space-specific"
        
        return json.dumps({
            "template_id": template_id,
            "success": True,
            "scope": scope
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_template",
                "description": "Create a new page template",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "template_name": {"type": "string", "description": "Name of the template"},
                        "template_content": {"type": "string", "description": "Content of the template"},
                        "requesting_user_id": {"type": "string", "description": "ID of the user creating the template"},
                        "is_global": {"type": "boolean", "description": "True for global template, False for space-specific (True/False)"},
                        "space_id": {"type": "string", "description": "Space ID if creating space-specific template (optional)"}
                    },
                    "required": ["template_name", "template_content", "requesting_user_id", "is_global"]
                }
            }
        }
EOF

# Create modify_template.py
cat > modify_template.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class ModifyTemplate(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], template_id: str, requesting_user_id: str,
               updated_content: str, template_name: Optional[str] = None,
               space_administrator_approval: Optional[bool] = None,
               platform_owner_approval: Optional[bool] = None) -> str:
        
        users = data.get("users", {})
        templates = data.get("page_templates", {})
        space_permissions = data.get("space_permissions", {})
        
        # Validate template exists
        if str(template_id) not in templates:
            return json.dumps({"success": False, "error": f"Template {template_id} not found"})
        
        # Validate user exists
        if str(requesting_user_id) not in users:
            return json.dumps({"success": False, "error": f"User {requesting_user_id} not found"})
        
        template = templates[str(template_id)]
        user = users[str(requesting_user_id)]
        
        # Check permissions
        has_permission = False
        
        if template.get("is_global"):
            # For global templates, only Platform Owner can modify
            if user.get("role") == "PlatformOwner":
                if platform_owner_approval is True:
                    has_permission = True
        else:
            # For space-specific templates
            space_id = template.get("space_id")
            
            # Check if user is Platform Owner or WikiProgramManager
            if user.get("role") in ["PlatformOwner", "WikiProgramManager"]:
                has_permission = True
            
            # Check if user is template creator
            elif template.get("created_by_user_id") == requesting_user_id:
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
            return json.dumps({"success": False, "error": "Insufficient permissions to modify template"})
        
        # Update template
        timestamp = "2025-10-01T00:00:00"
        template["content"] = updated_content
        template["updated_at"] = timestamp
        
        if template_name:
            template["name"] = template_name
        
        return json.dumps({
            "success": True,
            "message": "Template modified"
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "modify_template",
                "description": "Modify an existing template",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "template_id": {"type": "string", "description": "ID of the template to modify"},
                        "requesting_user_id": {"type": "string", "description": "ID of the user modifying the template"},
                        "updated_content": {"type": "string", "description": "New template content"},
                        "template_name": {"type": "string", "description": "New template name (optional)"},
                        "space_administrator_approval": {"type": "boolean", "description": "Space Administrator approval for space templates (True/False)"},
                        "platform_owner_approval": {"type": "boolean", "description": "Platform Owner approval for global templates (True/False)"}
                    },
                    "required": ["template_id", "requesting_user_id", "updated_content"]
                }
            }
        }
EOF

# Create delete_template.py
cat > delete_template.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class DeleteTemplate(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], template_id: str, requesting_user_id: str,
               deletion_confirmation: bool, space_administrator_approval: Optional[bool] = None,
               platform_owner_approval: Optional[bool] = None) -> str:
        
        users = data.get("users", {})
        templates = data.get("page_templates", {})
        space_permissions = data.get("space_permissions", {})
        
        # Validate template exists
        if str(template_id) not in templates:
            return json.dumps({"success": False, "error": f"Template {template_id} not found"})
        
        # Validate user exists
        if str(requesting_user_id) not in users:
            return json.dumps({"success": False, "error": f"User {requesting_user_id} not found"})
        
        # Validate confirmation
        if not deletion_confirmation:
            return json.dumps({"success": False, "error": "Deletion confirmation required"})
        
        template = templates[str(template_id)]
        user = users[str(requesting_user_id)]
        
        # Check permissions
        has_permission = False
        
        if template.get("is_global"):
            # For global templates, only Platform Owner can delete
            if user.get("role") == "PlatformOwner":
                if platform_owner_approval is True:
                    has_permission = True
        else:
            # For space-specific templates
            space_id = template.get("space_id")
            
            # Check if user is Platform Owner or WikiProgramManager
            if user.get("role") in ["PlatformOwner", "WikiProgramManager"]:
                has_permission = True
            
            # Check if user is template creator
            elif template.get("created_by_user_id") == requesting_user_id:
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
            return json.dumps({"success": False, "error": "Insufficient permissions to delete template"})
        
        # Delete template
        del templates[str(template_id)]
        
        return json.dumps({
            "success": True,
            "message": "Template deleted"
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "delete_template",
                "description": "Delete a template",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "template_id": {"type": "string", "description": "ID of the template to delete"},
                        "requesting_user_id": {"type": "string", "description": "ID of the user deleting the template"},
                        "deletion_confirmation": {"type": "boolean", "description": "Confirmation flag for deletion intent (True/False)"},
                        "space_administrator_approval": {"type": "boolean", "description": "Space Administrator approval for space templates (True/False)"},
                        "platform_owner_approval": {"type": "boolean", "description": "Platform Owner approval for global templates (True/False)"}
                    },
                    "required": ["template_id", "requesting_user_id", "deletion_confirmation"]
                }
            }
        }
EOF

# Create add_comment.py
cat > add_comment.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class AddComment(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], page_id: str, requesting_user_id: str,
               comment_text: str, parent_comment_id: Optional[str] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        pages = data.get("pages", {})
        users = data.get("users", {})
        comments = data.get("comments", {})
        spaces = data.get("spaces", {})
        space_permissions = data.get("space_permissions", {})
        page_permissions = data.get("page_permissions", {})
        
        # Validate page exists
        if str(page_id) not in pages:
            return json.dumps({"success": False, "error": f"Page {page_id} not found"})
        
        # Validate user exists
        if str(requesting_user_id) not in users:
            return json.dumps({"success": False, "error": f"User {requesting_user_id} not found"})
        
        # Validate parent comment if provided
        if parent_comment_id and str(parent_comment_id) not in comments:
            return json.dumps({"success": False, "error": f"Parent comment {parent_comment_id} not found"})
        
        page = pages[str(page_id)]
        user = users[str(requesting_user_id)]
        space_id = page.get("space_id")
        
        # Check permissions - user needs view permission to comment
        has_permission = False
        
        # Check if user is Platform Owner
        if user.get("role") == "PlatformOwner":
            has_permission = True
        
        # Check page-level permissions
        else:
            for perm in page_permissions.values():
                if (perm.get("page_id") == page_id and 
                    perm.get("user_id") == requesting_user_id and 
                    perm.get("permission_type") in ["view", "edit", "admin"]):
                    has_permission = True
                    break
        
        # Check space-level permissions if no page-level permissions
        if not has_permission and space_id:
            for perm in space_permissions.values():
                if (perm.get("space_id") == space_id and 
                    perm.get("user_id") == requesting_user_id and 
                    perm.get("permission_type") in ["view", "contribute", "moderate"]):
                    has_permission = True
                    break
        
        if not has_permission:
            return json.dumps({"success": False, "error": "Insufficient permissions to comment on page"})
        
        # Calculate thread level
        thread_level = 0
        if parent_comment_id:
            parent_comment = comments[str(parent_comment_id)]
            thread_level = parent_comment.get("thread_level", 0) + 1
        
        # Create comment
        comment_id = str(generate_id(comments))
        timestamp = "2025-10-01T00:00:00"
        
        new_comment = {
            "comment_id": int(comment_id),
            "page_id": page_id,
            "parent_comment_id": parent_comment_id,
            "content": comment_text,
            "content_format": "wiki",
            "status": "active",
            "thread_level": thread_level,
            "created_at": timestamp,
            "updated_at": timestamp,
            "created_by_user_id": requesting_user_id
        }
        
        comments[comment_id] = new_comment
        
        return json.dumps({
            "comment_id": comment_id,
            "success": True
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_comment",
                "description": "Add a comment to a page",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "page_id": {"type": "string", "description": "ID of the page to comment on"},
                        "requesting_user_id": {"type": "string", "description": "ID of the user adding the comment"},
                        "comment_text": {"type": "string", "description": "Content of the comment"},
                        "parent_comment_id": {"type": "string", "description": "ID of parent comment if replying (optional)"}
                    },
                    "required": ["page_id", "requesting_user_id", "comment_text"]
                }
            }
        }
EOF
