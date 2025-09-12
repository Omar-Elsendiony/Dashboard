#!/bin/bash

# Create resolve_comment.py
cat > resolve_comment.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class ResolveComment(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], comment_id: str, requesting_user_id: str,
               resolution_note: Optional[str] = None, content_owner_approval: Optional[bool] = None,
               space_administrator_approval: Optional[bool] = None) -> str:
        
        comments = data.get("comments", {})
        users = data.get("users", {})
        pages = data.get("pages", {})
        spaces = data.get("spaces", {})
        page_permissions = data.get("page_permissions", {})
        space_permissions = data.get("space_permissions", {})
        
        # Validate comment exists
        if str(comment_id) not in comments:
            return json.dumps({"error": f"Comment {comment_id} not found"})
        
        # Validate requesting user exists
        if str(requesting_user_id) not in users:
            return json.dumps({"error": f"User {requesting_user_id} not found"})
        
        comment = comments[str(comment_id)]
        page_id = comment.get("page_id")
        
        # Get page and space info
        if str(page_id) not in pages:
            return json.dumps({"error": f"Page {page_id} not found"})
        
        page = pages[str(page_id)]
        space_id = page.get("space_id")
        user = users[str(requesting_user_id)]
        
        # Check authority
        has_authority = False
        
        # Platform Owner can resolve any comment
        if user.get("role") == "PlatformOwner":
            has_authority = True
        
        # Content Owner (page creator or admin permission) can resolve
        elif page.get("created_by_user_id") == requesting_user_id:
            has_authority = content_owner_approval if content_owner_approval is not None else True
        else:
            # Check if user has admin permission on the page
            for perm in page_permissions.values():
                if (perm.get("page_id") == page_id and 
                    perm.get("user_id") == requesting_user_id and 
                    perm.get("permission_type") == "admin"):
                    has_authority = content_owner_approval if content_owner_approval is not None else True
                    break
        
        # Space Administrator can resolve
        if not has_authority:
            for perm in space_permissions.values():
                if (perm.get("space_id") == space_id and 
                    perm.get("user_id") == requesting_user_id and 
                    perm.get("permission_type") == "moderate"):
                    has_authority = space_administrator_approval if space_administrator_approval is not None else True
                    break
        
        if not has_authority:
            return json.dumps({"error": "Insufficient authority to resolve comment"})
        
        # Update comment status
        comment["status"] = "resolved"
        comment["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps({"success": True, "message": "Comment resolved", "status": "resolved"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "resolve_comment",
                "description": "Resolve a comment on a page",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "comment_id": {"type": "string", "description": "ID of the comment to resolve"},
                        "requesting_user_id": {"type": "string", "description": "ID of the user resolving the comment"},
                        "resolution_note": {"type": "string", "description": "Note about resolution"},
                        "content_owner_approval": {"type": "boolean", "description": "Content Owner approval if user is Content Owner (True/False)"},
                        "space_administrator_approval": {"type": "boolean", "description": "Space Administrator approval if user is Space Admin (True/False)"}
                    },
                    "required": ["comment_id", "requesting_user_id"]
                }
            }
        }
EOF

# Create edit_comment.py
cat > edit_comment.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class EditComment(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], comment_id: str, requesting_user_id: str,
               new_comment_text: str, edit_time_window_valid: bool) -> str:
        
        comments = data.get("comments", {})
        users = data.get("users", {})
        
        # Validate comment exists
        if str(comment_id) not in comments:
            return json.dumps({"error": f"Comment {comment_id} not found"})
        
        # Validate requesting user exists
        if str(requesting_user_id) not in users:
            return json.dumps({"error": f"User {requesting_user_id} not found"})
        
        comment = comments[str(comment_id)]
        
        # Check ownership
        if comment.get("created_by_user_id") != requesting_user_id:
            return json.dumps({"error": "Only comment author can edit comment"})
        
        # Check time window
        if not edit_time_window_valid:
            return json.dumps({"error": "Edit time window has expired"})
        
        # Update comment
        comment["content"] = new_comment_text
        comment["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps({"success": True, "message": "Comment edited", "edited_flag": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "edit_comment",
                "description": "Edit a comment",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "comment_id": {"type": "string", "description": "ID of the comment to edit"},
                        "requesting_user_id": {"type": "string", "description": "ID of the user editing the comment"},
                        "new_comment_text": {"type": "string", "description": "New comment content"},
                        "edit_time_window_valid": {"type": "boolean", "description": "Whether edit is within allowed time window (True/False)"}
                    },
                    "required": ["comment_id", "requesting_user_id", "new_comment_text", "edit_time_window_valid"]
                }
            }
        }
EOF

# Create attach_file.py
cat > attach_file.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class AttachFile(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], target_type: str, target_id: str, requesting_user_id: str,
               file_name: str, file_content: bytes, file_size_bytes: int) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        users = data.get("users", {})
        pages = data.get("pages", {})
        comments = data.get("comments", {})
        attachments = data.get("attachments", {})
        page_permissions = data.get("page_permissions", {})
        space_permissions = data.get("space_permissions", {})
        
        # Validate user exists
        if str(requesting_user_id) not in users:
            return json.dumps({"error": f"User {requesting_user_id} not found"})
        
        # Validate target type
        if target_type not in ["page", "comment"]:
            return json.dumps({"error": "Target type must be 'page' or 'comment'"})
        
        # Validate target exists and check permissions
        if target_type == "page":
            if str(target_id) not in pages:
                return json.dumps({"error": f"Page {target_id} not found"})
            
            page = pages[str(target_id)]
            space_id = page.get("space_id")
            
            # Check if user can edit the page
            has_permission = False
            
            # Check page permissions
            for perm in page_permissions.values():
                if (perm.get("page_id") == target_id and 
                    perm.get("user_id") == requesting_user_id and 
                    perm.get("permission_type") in ["edit", "admin"]):
                    has_permission = True
                    break
            
            # Check space permissions
            if not has_permission:
                for perm in space_permissions.values():
                    if (perm.get("space_id") == space_id and 
                        perm.get("user_id") == requesting_user_id and 
                        perm.get("permission_type") in ["contribute", "moderate"]):
                        has_permission = True
                        break
            
            if not has_permission:
                return json.dumps({"error": "Insufficient permissions to attach file to page"})
        
        elif target_type == "comment":
            if str(target_id) not in comments:
                return json.dumps({"error": f"Comment {target_id} not found"})
            
            comment = comments[str(target_id)]
            if comment.get("created_by_user_id") != requesting_user_id:
                return json.dumps({"error": "Can only attach files to your own comments"})
        
        # Create attachment
        attachment_id = generate_id(attachments)
        timestamp = "2025-10-01T00:00:00"
        
        new_attachment = {
            "attachment_id": attachment_id,
            "page_id": target_id if target_type == "page" else None,
            "comment_id": target_id if target_type == "comment" else None,
            "filename": file_name,
            "original_filename": file_name,
            "mime_type": "application/octet-stream",
            "file_size": file_size_bytes,
            "storage_path": f"/attachments/{attachment_id}/{file_name}",
            "storage_type": "local",
            "version": 1,
            "created_at": timestamp,
            "uploaded_by_user_id": requesting_user_id
        }
        
        attachments[str(attachment_id)] = new_attachment
        
        return json.dumps({"attachment_id": str(attachment_id), "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "attach_file",
                "description": "Attach a file to a page or comment",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "target_type": {"type": "string", "description": "Type of target (page or comment)"},
                        "target_id": {"type": "string", "description": "ID of the page or comment"},
                        "requesting_user_id": {"type": "string", "description": "ID of the user attaching the file"},
                        "file_name": {"type": "string", "description": "Name of the file"},
                        "file_content": {"type": "string", "description": "File content"},
                        "file_size_bytes": {"type": "integer", "description": "Size of file in bytes"}
                    },
                    "required": ["target_type", "target_id", "requesting_user_id", "file_name", "file_content", "file_size_bytes"]
                }
            }
        }
EOF

# Create delete_file.py
cat > delete_file.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class DeleteFile(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], attachment_id: str, requesting_user_id: str,
               target_type: str, target_id: str) -> str:
        
        users = data.get("users", {})
        attachments = data.get("attachments", {})
        pages = data.get("pages", {})
        comments = data.get("comments", {})
        page_permissions = data.get("page_permissions", {})
        space_permissions = data.get("space_permissions", {})
        
        # Validate user exists
        if str(requesting_user_id) not in users:
            return json.dumps({"error": f"User {requesting_user_id} not found"})
        
        # Validate attachment exists
        if str(attachment_id) not in attachments:
            return json.dumps({"error": f"Attachment {attachment_id} not found"})
        
        attachment = attachments[str(attachment_id)]
        user = users[str(requesting_user_id)]
        
        # Check authority
        has_authority = False
        
        # Platform Owner can delete any file
        if user.get("role") == "PlatformOwner":
            has_authority = True
        
        # File uploader can delete their own file
        elif attachment.get("uploaded_by_user_id") == requesting_user_id:
            has_authority = True
        
        # Page owner or admin can delete files on their page
        elif target_type == "page" and str(target_id) in pages:
            page = pages[str(target_id)]
            space_id = page.get("space_id")
            
            # Check if user created the page
            if page.get("created_by_user_id") == requesting_user_id:
                has_authority = True
            
            # Check page admin permissions
            if not has_authority:
                for perm in page_permissions.values():
                    if (perm.get("page_id") == target_id and 
                        perm.get("user_id") == requesting_user_id and 
                        perm.get("permission_type") == "admin"):
                        has_authority = True
                        break
            
            # Check space admin permissions
            if not has_authority:
                for perm in space_permissions.values():
                    if (perm.get("space_id") == space_id and 
                        perm.get("user_id") == requesting_user_id and 
                        perm.get("permission_type") == "moderate"):
                        has_authority = True
                        break
        
        # Comment owner can delete files on their comment
        elif target_type == "comment" and str(target_id) in comments:
            comment = comments[str(target_id)]
            if comment.get("created_by_user_id") == requesting_user_id:
                has_authority = True
        
        if not has_authority:
            return json.dumps({"error": "Insufficient authority to delete file"})
        
        # Delete attachment
        del attachments[str(attachment_id)]
        
        return json.dumps({"success": True, "message": "File deleted"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "delete_file",
                "description": "Delete an attachment file",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "attachment_id": {"type": "string", "description": "ID of the attachment to delete"},
                        "requesting_user_id": {"type": "string", "description": "ID of the user deleting the file"},
                        "target_type": {"type": "string", "description": "Type of target (page or comment)"},
                        "target_id": {"type": "string", "description": "ID of the page or comment"}
                    },
                    "required": ["attachment_id", "requesting_user_id", "target_type", "target_id"]
                }
            }
        }
EOF

# Create create_user_group.py
cat > create_user_group.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class CreateUserGroup(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], group_name: str, requesting_user_id: str,
               group_description: Optional[str] = None, platform_owner_approval: bool = False) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        users = data.get("users", {})
        groups = data.get("groups", {})
        
        # Validate user exists
        if str(requesting_user_id) not in users:
            return json.dumps({"error": f"User {requesting_user_id} not found"})
        
        user = users[str(requesting_user_id)]
        
        # Check authority - only Platform Owner can create user groups
        if user.get("role") != "PlatformOwner" or not platform_owner_approval:
            return json.dumps({"error": "Only Platform Owner can create user groups"})
        
        # Check if group name already exists
        for group in groups.values():
            if group.get("name").lower() == group_name.lower():
                return json.dumps({"error": f"Group with name '{group_name}' already exists"})
        
        # Create group
        group_id = generate_id(groups)
        timestamp = "2025-10-01T00:00:00"
        
        new_group = {
            "group_id": group_id,
            "name": group_name,
            "description": group_description,
            "type": "custom",
            "created_at": timestamp,
            "created_by_user_id": requesting_user_id
        }
        
        groups[str(group_id)] = new_group
        
        return json.dumps({"group_id": str(group_id), "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_user_group",
                "description": "Create a new user group",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "group_name": {"type": "string", "description": "Name of the user group"},
                        "requesting_user_id": {"type": "string", "description": "ID of the user creating the group"},
                        "group_description": {"type": "string", "description": "Description of the group"},
                        "platform_owner_approval": {"type": "boolean", "description": "Platform Owner approval flag (True/False)"}
                    },
                    "required": ["group_name", "requesting_user_id", "platform_owner_approval"]
                }
            }
        }
EOF

# Create add_user_to_group.py
cat > add_user_to_group.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class AddUserToGroup(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], group_id: str, target_user_id: str, requesting_user_id: str,
               space_id: Optional[str] = None, platform_owner_approval: Optional[bool] = None,
               wiki_program_manager_approval: Optional[bool] = None,
               space_administrator_approval: Optional[bool] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        users = data.get("users", {})
        groups = data.get("groups", {})
        user_groups = data.get("user_groups", {})
        space_permissions = data.get("space_permissions", {})
        
        # Validate entities exist
        if str(requesting_user_id) not in users:
            return json.dumps({"error": f"Requesting user {requesting_user_id} not found"})
        
        if str(target_user_id) not in users:
            return json.dumps({"error": f"Target user {target_user_id} not found"})
        
        if str(group_id) not in groups:
            return json.dumps({"error": f"Group {group_id} not found"})
        
        user = users[str(requesting_user_id)]
        
        # Check if user is already in group
        for ug in user_groups.values():
            if ug.get("user_id") == target_user_id and ug.get("group_id") == group_id:
                return json.dumps({"error": "User is already in the group"})
        
        # Check authority
        has_authority = False
        
        # Platform Owner can add any user to any group
        if user.get("role") == "PlatformOwner" and platform_owner_approval:
            has_authority = True
        
        # Wiki Program Manager can add users to groups
        elif user.get("role") == "WikiProgramManager" and wiki_program_manager_approval:
            has_authority = True
        
        # Space Administrator can add users to groups in their space
        elif space_id:
            for perm in space_permissions.values():
                if (perm.get("space_id") == space_id and 
                    perm.get("user_id") == requesting_user_id and 
                    perm.get("permission_type") == "moderate" and
                    space_administrator_approval):
                    has_authority = True
                    break
        
        if not has_authority:
            return json.dumps({"error": "Insufficient authority to add user to group"})
        
        # Add user to group
        user_group_id = generate_id(user_groups)
        timestamp = "2025-10-01T00:00:00"
        
        new_user_group = {
            "user_group_id": user_group_id,
            "user_id": target_user_id,
            "group_id": group_id,
            "added_at": timestamp,
            "added_by_user_id": requesting_user_id
        }
        
        user_groups[str(user_group_id)] = new_user_group
        
        return json.dumps({"success": True, "message": "User added to group"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_user_to_group",
                "description": "Add a user to a group",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "group_id": {"type": "string", "description": "ID of the group"},
                        "target_user_id": {"type": "string", "description": "ID of the user to add"},
                        "requesting_user_id": {"type": "string", "description": "ID of the user making the request"},
                        "space_id": {"type": "string", "description": "Space ID if Space Administrator is making the request"},
                        "platform_owner_approval": {"type": "boolean", "description": "Platform Owner approval if user is Platform Owner (True/False)"},
                        "wiki_program_manager_approval": {"type": "boolean", "description": "Wiki Program Manager approval if user is Program Manager (True/False)"},
                        "space_administrator_approval": {"type": "boolean", "description": "Space Administrator approval if user is Space Admin (True/False)"}
                    },
                    "required": ["group_id", "target_user_id", "requesting_user_id"]
                }
            }
        }
EOF

# Create modify_user_permissions.py
cat > modify_user_permissions.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class ModifyUserPermissions(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], target_user_id: str, requesting_user_id: str,
               permission_changes: Dict[str, Any], space_id: Optional[str] = None,
               page_id: Optional[str] = None, platform_owner_approval: Optional[bool] = None,
               space_administrator_approval: Optional[bool] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        users = data.get("users", {})
        page_permissions = data.get("page_permissions", {})
        space_permissions = data.get("space_permissions", {})
        pages = data.get("pages", {})
        spaces = data.get("spaces", {})
        
        # Validate entities exist
        if str(requesting_user_id) not in users:
            return json.dumps({"error": f"Requesting user {requesting_user_id} not found"})
        
        if str(target_user_id) not in users:
            return json.dumps({"error": f"Target user {target_user_id} not found"})
        
        user = users[str(requesting_user_id)]
        
        # Check authority
        has_authority = False
        
        # Platform Owner can modify any permissions
        if user.get("role") == "PlatformOwner" and platform_owner_approval:
            has_authority = True
        
        # Space Administrator can modify permissions in their space
        elif space_id:
            for perm in space_permissions.values():
                if (perm.get("space_id") == space_id and 
                    perm.get("user_id") == requesting_user_id and 
                    perm.get("permission_type") == "moderate" and
                    space_administrator_approval):
                    has_authority = True
                    break
        
        if not has_authority:
            return json.dumps({"error": "Insufficient authority to modify user permissions"})
        
        timestamp = "2025-10-01T00:00:00"
        
        # Apply permission changes
        if page_id and "page_permissions" in permission_changes:
            if str(page_id) not in pages:
                return json.dumps({"error": f"Page {page_id} not found"})
            
            for permission_type, action in permission_changes["page_permissions"].items():
                if permission_type not in ["view", "create", "edit", "delete", "admin"]:
                    return json.dumps({"error": f"Invalid page permission type: {permission_type}"})
                
                if action == "grant":
                    # Check if permission already exists
                    exists = False
                    for perm in page_permissions.values():
                        if (perm.get("page_id") == page_id and 
                            perm.get("user_id") == target_user_id and 
                            perm.get("permission_type") == permission_type):
                            exists = True
                            break
                    
                    if not exists:
                        perm_id = generate_id(page_permissions)
                        new_permission = {
                            "page_permission_id": perm_id,
                            "page_id": page_id,
                            "user_id": target_user_id,
                            "group_id": None,
                            "permission_type": permission_type,
                            "granted_at": timestamp,
                            "granted_by_user_id": requesting_user_id
                        }
                        page_permissions[str(perm_id)] = new_permission
                
                elif action == "revoke":
                    # Find and remove permission
                    to_remove = []
                    for perm_id, perm in page_permissions.items():
                        if (perm.get("page_id") == page_id and 
                            perm.get("user_id") == target_user_id and 
                            perm.get("permission_type") == permission_type):
                            to_remove.append(perm_id)
                    
                    for perm_id in to_remove:
                        del page_permissions[perm_id]
        
        if space_id and "space_permissions" in permission_changes:
            if str(space_id) not in spaces:
                return json.dumps({"error": f"Space {space_id} not found"})
            
            for permission_type, action in permission_changes["space_permissions"].items():
                if permission_type not in ["view", "contribute", "moderate"]:
                    return json.dumps({"error": f"Invalid space permission type: {permission_type}"})
                
                if action == "grant":
                    # Check if permission already exists
                    exists = False
                    for perm in space_permissions.values():
                        if (perm.get("space_id") == space_id and 
                            perm.get("user_id") == target_user_id and 
                            perm.get("permission_type") == permission_type):
                            exists = True
                            break
                    
                    if not exists:
                        perm_id = generate_id(space_permissions)
                        new_permission = {
                            "space_permission_id": perm_id,
                            "space_id": space_id,
                            "user_id": target_user_id,
                            "group_id": None,
                            "permission_type": permission_type,
                            "granted_at": timestamp,
                            "granted_by_user_id": requesting_user_id
                        }
                        space_permissions[str(perm_id)] = new_permission
                
                elif action == "revoke":
                    # Find and remove permission
                    to_remove = []
                    for perm_id, perm in space_permissions.items():
                        if (perm.get("space_id") == space_id and 
                            perm.get("user_id") == target_user_id and 
                            perm.get("permission_type") == permission_type):
                            to_remove.append(perm_id)
                    
                    for perm_id in to_remove:
                        del space_permissions[perm_id]
        
        return json.dumps({"success": True, "message": "User permissions updated"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "modify_user_permissions",
                "description": "Modify user permissions for spaces or pages",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "target_user_id": {"type": "string", "description": "ID of the user whose permissions to modify"},
                        "requesting_user_id": {"type": "string", "description": "ID of the user making the request"},
                        "permission_changes": {"type": "object", "description": "Dictionary of permission modifications"},
                        "space_id": {"type": "string", "description": "Space ID if modifying space-specific permissions"},
                        "page_id": {"type": "string", "description": "Page ID if modifying page-specific permissions"},
                        "platform_owner_approval": {"type": "boolean", "description": "Platform Owner approval if user is Platform Owner (True/False)"}
                    },
                    "required": ["target_user_id", "requesting_user_id"]
                }
            }
        }
EOF