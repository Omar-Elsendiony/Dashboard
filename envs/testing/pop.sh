

# Create directory for tools
mkdir -p wiki_tools

# Tool 1: create_space
cat > wiki_tools/create_space.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class CreateSpace(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], space_name: str, requesting_user_id: str,
               space_type: Optional[str] = None, default_template_id: Optional[str] = None,
               permission_set: Optional[Dict[str, Any]] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        spaces = data.get("spaces", {})
        users = data.get("users", {})
        space_permissions = data.get("space_permissions", {})
        
        # Validate user exists
        if str(requesting_user_id) not in users:
            return json.dumps({"error": "Requesting user not found"})
        
        user = users[str(requesting_user_id)]
        user_role = user.get("role", "User")
        
        # Authority verification - only certain roles can create spaces
        if user_role not in ["PlatformOwner", "WikiProgramManager"]:
            return json.dumps({"error": "Insufficient authority to create space"})
        
        # Check if space name already exists
        for space in spaces.values():
            if space.get("name") == space_name:
                return json.dumps({"error": "Space name already exists"})
        
        # Validate space type
        if space_type and space_type not in ["global", "personal", "private"]:
            return json.dumps({"error": "Invalid space type"})
        
        space_id = generate_id(spaces)
        timestamp = "2025-10-01T00:00:00"
        
        # Generate space key from name (simplified)
        space_key = space_name.lower().replace(" ", "_")[:50]
        
        new_space = {
            "space_id": space_id,
            "space_key": space_key,
            "name": space_name,
            "description": None,
            "type": space_type or "global",
            "status": "current",
            "homepage_id": None,
            "theme": None,
            "logo_url": None,
            "anonymous_access": False,
            "public_signup": False,
            "created_at": timestamp,
            "updated_at": timestamp,
            "created_by_user_id": requesting_user_id
        }
        
        spaces[space_id] = new_space
        
        # Create space administrator permission
        admin_permission_id = generate_id(space_permissions)
        admin_permission = {
            "space_permission_id": admin_permission_id,
            "space_id": space_id,
            "user_id": requesting_user_id,
            "group_id": None,
            "permission_type": "moderate",
            "granted_at": timestamp,
            "granted_by_user_id": requesting_user_id
        }
        
        space_permissions[admin_permission_id] = admin_permission
        
        return json.dumps({
            "space_id": space_id,
            "success": True,
            "space_administrator_id": requesting_user_id
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_space",
                "description": "Create a new wiki space",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "space_name": {"type": "string", "description": "Unique name for the space"},
                        "requesting_user_id": {"type": "string", "description": "ID of the user requesting space creation"},
                        "space_type": {"type": "string", "description": "Type of space (global, personal, private)"},
                        "default_template_id": {"type": "string", "description": "Template to apply to the space"},
                        "permission_set": {"type": "object", "description": "Initial permission configuration"}
                    },
                    "required": ["space_name", "requesting_user_id"]
                }
            }
        }
EOF

# Tool 2: modify_space_settings
cat > wiki_tools/modify_space_settings.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class ModifySpaceSettings(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], space_id: str, requesting_user_id: str,
               settings_changes: Dict[str, Any], space_administrator_approval: Optional[bool] = None,
               platform_owner_approval: Optional[bool] = None) -> str:
        
        spaces = data.get("spaces", {})
        users = data.get("users", {})
        space_permissions = data.get("space_permissions", {})
        
        # Validate space exists
        if str(space_id) not in spaces:
            return json.dumps({"error": "Space not found"})
        
        # Validate user exists
        if str(requesting_user_id) not in users:
            return json.dumps({"error": "Requesting user not found"})
        
        user = users[str(requesting_user_id)]
        user_role = user.get("role", "User")
        space = spaces[str(space_id)]
        
        # Check if user has space admin permissions
        has_space_admin = False
        for perm in space_permissions.values():
            if (perm.get("space_id") == space_id and 
                perm.get("user_id") == requesting_user_id and
                perm.get("permission_type") == "moderate"):
                has_space_admin = True
                break
        
        # Authority verification
        if user_role == "PlatformOwner" and platform_owner_approval:
            pass  # Platform owner can modify any space
        elif has_space_admin and space_administrator_approval:
            pass  # Space admin can modify their space
        elif user_role in ["WikiProgramManager"] and space.get("created_by_user_id") == requesting_user_id:
            pass  # Wiki program manager can modify spaces they created
        else:
            return json.dumps({"error": "Insufficient authority to modify space settings"})
        
        # Apply settings changes
        timestamp = "2025-10-01T00:00:00"
        for key, value in settings_changes.items():
            if key in ["name", "description", "theme", "logo_url", "anonymous_access", "public_signup"]:
                space[key] = value
        
        space["updated_at"] = timestamp
        
        return json.dumps({"success": True, "message": "Space settings updated"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "modify_space_settings",
                "description": "Modify space settings with appropriate authority verification",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "space_id": {"type": "string", "description": "ID of the space to modify"},
                        "requesting_user_id": {"type": "string", "description": "ID of the user requesting modification"},
                        "settings_changes": {"type": "object", "description": "Dictionary of settings to modify"},
                        "space_administrator_approval": {"type": "boolean", "description": "Space Administrator approval if user is Space Admin (True/False)"},
                        "platform_owner_approval": {"type": "boolean", "description": "Platform Owner approval if user is Platform Owner (True/False)"}
                    },
                    "required": ["space_id", "requesting_user_id", "settings_changes"]
                }
            }
        }
EOF

# Tool 3: archive_space
cat > wiki_tools/archive_space.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ArchiveSpace(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], space_id: str, requesting_user_id: str, reason: str) -> str:
        
        spaces = data.get("spaces", {})
        users = data.get("users", {})
        space_permissions = data.get("space_permissions", {})
        
        # Validate space exists
        if str(space_id) not in spaces:
            return json.dumps({"error": "Space not found"})
        
        # Validate user exists
        if str(requesting_user_id) not in users:
            return json.dumps({"error": "Requesting user not found"})
        
        user = users[str(requesting_user_id)]
        user_role = user.get("role", "User")
        space = spaces[str(space_id)]
        
        # Check if user has space admin permissions
        has_space_admin = False
        for perm in space_permissions.values():
            if (perm.get("space_id") == space_id and 
                perm.get("user_id") == requesting_user_id and
                perm.get("permission_type") == "moderate"):
                has_space_admin = True
                break
        
        # Authority verification - Platform Owner or Space Administrator
        if user_role not in ["PlatformOwner"] and not has_space_admin:
            return json.dumps({"error": "Insufficient authority to archive space"})
        
        # Archive the space
        timestamp = "2025-10-01T00:00:00"
        space["status"] = "archived"
        space["updated_at"] = timestamp
        
        return json.dumps({"success": True, "message": "Space archived", "status": "read-only"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "archive_space",
                "description": "Archive a space making it read-only",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "space_id": {"type": "string", "description": "ID of the space to archive"},
                        "requesting_user_id": {"type": "string", "description": "ID of the user requesting archival"},
                        "reason": {"type": "string", "description": "Reason for archiving the space"}
                    },
                    "required": ["space_id", "requesting_user_id", "reason"]
                }
            }
        }
EOF

# Tool 4: toggle_anonymous_access
cat > wiki_tools/toggle_anonymous_access.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ToggleAnonymousAccess(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], space_id: str, requesting_user_id: str,
               enable_anonymous: bool, platform_owner_approval: bool) -> str:
        
        spaces = data.get("spaces", {})
        users = data.get("users", {})
        
        # Validate space exists
        if str(space_id) not in spaces:
            return json.dumps({"error": "Space not found"})
        
        # Validate user exists
        if str(requesting_user_id) not in users:
            return json.dumps({"error": "Requesting user not found"})
        
        user = users[str(requesting_user_id)]
        user_role = user.get("role", "User")
        space = spaces[str(space_id)]
        
        # Authority verification - only Platform Owner can toggle anonymous access
        if user_role != "PlatformOwner" or not platform_owner_approval:
            return json.dumps({"error": "Insufficient authority to toggle anonymous access"})
        
        # Toggle anonymous access
        timestamp = "2025-10-01T00:00:00"
        space["anonymous_access"] = enable_anonymous
        space["updated_at"] = timestamp
        
        status = "enabled" if enable_anonymous else "disabled"
        return json.dumps({"success": True, "message": f"Anonymous access {status}"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "toggle_anonymous_access",
                "description": "Toggle anonymous access for a space",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "space_id": {"type": "string", "description": "ID of the space"},
                        "requesting_user_id": {"type": "string", "description": "ID of the user requesting toggle"},
                        "enable_anonymous": {"type": "boolean", "description": "True to enable, False to disable anonymous access (True/False)"},
                        "platform_owner_approval": {"type": "boolean", "description": "Platform Owner approval flag (True/False)"}
                    },
                    "required": ["space_id", "requesting_user_id", "enable_anonymous", "platform_owner_approval"]
                }
            }
        }
EOF

# Tool 5: create_page
cat > wiki_tools/create_page.py << 'EOF'
import json
from typing import Any, Dict, Optional, List
from tau_bench.envs.tool import Tool

class CreatePage(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], page_title: str, space_id: str, requesting_user_id: str,
               parent_page_id: Optional[str] = None, content: Optional[str] = None,
               labels: Optional[List[str]] = None, template_id: Optional[str] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        pages = data.get("pages", {})
        spaces = data.get("spaces", {})
        users = data.get("users", {})
        space_permissions = data.get("space_permissions", {})
        page_permissions = data.get("page_permissions", {})
        page_labels = data.get("page_labels", {})
        labels_table = data.get("labels", {})
        
        # Validate space exists
        if str(space_id) not in spaces:
            return json.dumps({"error": "Space not found"})
        
        # Validate user exists
        if str(requesting_user_id) not in users:
            return json.dumps({"error": "Requesting user not found"})
        
        # Validate parent page if specified
        if parent_page_id and str(parent_page_id) not in pages:
            return json.dumps({"error": "Parent page not found"})
        
        # Check user permissions - need contribute permission in space or create permission on parent page
        has_permission = False
        
        # Check space permissions
        for perm in space_permissions.values():
            if (perm.get("space_id") == space_id and 
                perm.get("user_id") == requesting_user_id and
                perm.get("permission_type") in ["contribute", "moderate"]):
                has_permission = True
                break
        
        # Check parent page permissions if creating subpage
        if parent_page_id and not has_permission:
            for perm in page_permissions.values():
                if (perm.get("page_id") == parent_page_id and 
                    perm.get("user_id") == requesting_user_id and
                    perm.get("permission_type") in ["create", "admin"]):
                    has_permission = True
                    break
        
        if not has_permission:
            return json.dumps({"error": "Insufficient permissions to create page"})
        
        page_id = generate_id(pages)
        timestamp = "2025-10-01T00:00:00"
        
        new_page = {
            "page_id": page_id,
            "space_id": space_id,
            "title": page_title,
            "content": content,
            "content_format": "wiki",
            "parent_page_id": parent_page_id,
            "position": 0,
            "status": "current",
            "version": 1,
            "template_id": template_id,
            "created_at": timestamp,
            "updated_at": timestamp,
            "published_at": timestamp,
            "created_by_user_id": requesting_user_id,
            "last_modified_by_user_id": requesting_user_id
        }
        
        pages[page_id] = new_page
        
        # Create content owner permission
        owner_permission_id = generate_id(page_permissions)
        owner_permission = {
            "page_permission_id": owner_permission_id,
            "page_id": page_id,
            "user_id": requesting_user_id,
            "group_id": None,
            "permission_type": "admin",
            "granted_at": timestamp,
            "granted_by_user_id": requesting_user_id
        }
        
        page_permissions[owner_permission_id] = owner_permission
        
        # Add labels if specified
        if labels:
            for label_name in labels:
                # Find or create label
                label_id = None
                for lid, label in labels_table.items():
                    if label.get("name") == label_name and label.get("space_id") == space_id:
                        label_id = lid
                        break
                
                if label_id:
                    page_label_id = generate_id(page_labels)
                    page_label = {
                        "page_label_id": page_label_id,
                        "page_id": page_id,
                        "label_id": label_id,
                        "added_at": timestamp,
                        "added_by_user_id": requesting_user_id
                    }
                    page_labels[str(page_label_id)] = page_label
        
        return json.dumps({
            "page_id": page_id,
            "success": True,
            "content_owner_id": requesting_user_id
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_page",
                "description": "Create a new wiki page",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "page_title": {"type": "string", "description": "Title of the page"},
                        "space_id": {"type": "string", "description": "ID of the target space"},
                        "requesting_user_id": {"type": "string", "description": "ID of the user creating the page"},
                        "parent_page_id": {"type": "string", "description": "ID of parent page if creating subpage"},
                        "content": {"type": "string", "description": "Initial page content"},
                        "labels": {"type": "array", "items": {"type": "string"}, "description": "Initial labels for the page"},
                        "template_id": {"type": "string", "description": "Template to use for page creation"}
                    },
                    "required": ["page_title", "space_id", "requesting_user_id"]
                }
            }
        }
EOF

# Tool 6: update_page
cat > wiki_tools/update_page.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdatePage(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], page_id: str, requesting_user_id: str,
               content_changes: Optional[Dict[str, Any]] = None,
               label_changes: Optional[Dict[str, Any]] = None,
               ownership_changes: Optional[Dict[str, Any]] = None,
               title_change: Optional[str] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        pages = data.get("pages", {})
        users = data.get("users", {})
        page_permissions = data.get("page_permissions", {})
        page_versions = data.get("page_versions", {})
        
        # Validate page exists
        if str(page_id) not in pages:
            return json.dumps({"error": "Page not found"})
        
        # Validate user exists
        if str(requesting_user_id) not in users:
            return json.dumps({"error": "Requesting user not found"})
        
        page = pages[str(page_id)]
        
        # Check user permissions - need edit or admin permission
        has_permission = False
        for perm in page_permissions.values():
            if (perm.get("page_id") == page_id and 
                perm.get("user_id") == requesting_user_id and
                perm.get("permission_type") in ["edit", "admin"]):
                has_permission = True
                break
        
        if not has_permission:
            return json.dumps({"error": "Insufficient permissions to update page"})
        
        timestamp = "2025-10-01T00:00:00"
        
        # Create version history entry
        version_id = generate_id(page_versions)
        page_version = {
            "page_version_id": version_id,
            "page_id": page_id,
            "version_number": page.get("version", 1),
            "title": page.get("title"),
            "content": page.get("content"),
            "content_format": page.get("content_format", "wiki"),
            "change_type": "major",
            "created_at": timestamp,
            "created_by_user_id": requesting_user_id
        }
        page_versions[version_id] = page_version
        
        # Apply content changes
        if content_changes:
            for key, value in content_changes.items():
                if key in ["content", "content_format"]:
                    page[key] = value
        
        # Apply title change
        if title_change:
            page["title"] = title_change
        
        # Update metadata
        page["version"] = page.get("version", 1) + 1
        page["updated_at"] = timestamp
        page["last_modified_by_user_id"] = requesting_user_id
        
        return json.dumps({"success": True, "message": "Page updated", "page_id": page_id})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_page",
                "description": "Update page content, labels, ownership, or title",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "page_id": {"type": "string", "description": "ID of the page to update"},
                        "requesting_user_id": {"type": "string", "description": "ID of the user updating the page"},
                        "content_changes": {"type": "object", "description": "Content updates"},
                        "label_changes": {"type": "object", "description": "Label additions/removals"},
                        "ownership_changes": {"type": "object", "description": "Ownership modifications"},
                        "title_change": {"type": "string", "description": "New page title"}
                    },
                    "required": ["page_id", "requesting_user_id"]
                }
            }
        }
EOF

# Tool 7: delete_page
cat > wiki_tools/delete_page.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class DeletePage(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], page_id: str, requesting_user_id: str,
               content_owner_approval: Optional[bool] = None,
               space_administrator_approval: Optional[bool] = None,
               force_delete: bool = False) -> str:
        
        pages = data.get("pages", {})
        users = data.get("users", {})
        page_permissions = data.get("page_permissions", {})
        space_permissions = data.get("space_permissions", {})
        
        # Validate page exists
        if str(page_id) not in pages:
            return json.dumps({"error": "Page not found"})
        
        # Validate user exists
        if str(requesting_user_id) not in users:
            return json.dumps({"error": "Requesting user not found"})
        
        page = pages[str(page_id)]
        space_id = page.get("space_id")
        
        # Check for child pages (dependencies)
        child_pages = []
        for p in pages.values():
            if p.get("parent_page_id") == page_id:
                child_pages.append(p)
        
        if child_pages and not force_delete:
            return json.dumps({"error": "Cannot delete page with child pages. Use force_delete or remove child pages first"})
        
        # Check user permissions
        has_delete_permission = False
        is_content_owner = False
        is_space_admin = False
        
        # Check if user is content owner (has admin permission on page)
        for perm in page_permissions.values():
            if (perm.get("page_id") == page_id and 
                perm.get("user_id") == requesting_user_id and
                perm.get("permission_type") == "admin"):
                is_content_owner = True
                break
        
        # Check if user is space administrator
        for perm in space_permissions.values():
            if (perm.get("space_id") == space_id and 
                perm.get("user_id") == requesting_user_id and
                perm.get("permission_type") == "moderate"):
                is_space_admin = True
                break
        
        # Check if user has delete permission
        for perm in page_permissions.values():
            if (perm.get("page_id") == page_id and 
                perm.get("user_id") == requesting_user_id and
                perm.get("permission_type") in ["delete", "admin"]):
                has_delete_permission = True
                break
        
        # Authority verification
        if is_content_owner and content_owner_approval:
            pass
        elif is_space_admin and space_administrator_approval:
            pass
        elif has_delete_permission:
            pass
        else:
            return json.dumps({"error": "Insufficient authority to delete page"})
        
        # Delete the page (mark as deleted)
        timestamp = "2025-10-01T00:00:00"
        page["status"] = "deleted"
        page["updated_at"] = timestamp
        
        # Delete child pages if force_delete is True
        if force_delete:
            for child in child_pages:
                child["status"] = "deleted"
                child["updated_at"] = timestamp
        
        return json.dumps({"success": True, "message": "Page deleted"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "delete_page",
                "description": "Delete a wiki page with dependency checking",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "page_id": {"type": "string", "description": "ID of the page to delete"},
                        "requesting_user_id": {"type": "string", "description": "ID of the user requesting deletion"},
                        "content_owner_approval": {"type": "boolean", "description": "Content Owner approval if user is Content Owner (True/False)"},
                        "space_administrator_approval": {"type": "boolean", "description": "Space Administrator approval if user is Space Admin (True/False)"},
                        "force_delete": {"type": "boolean", "description": "Force deletion despite dependencies (True/False)"}
                    },
                    "required": ["page_id", "requesting_user_id"]
                }
            }
        }
EOF
