#!/bin/bash

# Create create_subscription.py
cat > create_subscription.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class CreateSubscription(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], requesting_user_id: str, target_type: str, 
               target_id: str, notification_preferences: Optional[Dict[str, Any]] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        users = data.get("users", {})
        spaces = data.get("spaces", {})
        pages = data.get("pages", {})
        watchers = data.get("watchers", {})
        
        # Validate requesting user exists
        if str(requesting_user_id) not in users:
            return json.dumps({"error": f"Requesting user {requesting_user_id} not found"})
        
        # Validate target_type
        valid_target_types = ["space", "page", "user"]
        if target_type not in valid_target_types:
            return json.dumps({"error": f"Invalid target_type. Must be one of {valid_target_types}"})
        
        # Validate target exists based on type
        if target_type == "space" and str(target_id) not in spaces:
            return json.dumps({"error": f"Space {target_id} not found"})
        elif target_type == "page" and str(target_id) not in pages:
            return json.dumps({"error": f"Page {target_id} not found"})
        elif target_type == "user" and str(target_id) not in users:
            return json.dumps({"error": f"User {target_id} not found"})
        
        # Check if subscription already exists
        for watcher in watchers.values():
            if (watcher.get("user_id") == requesting_user_id and 
                watcher.get("target_type") == target_type and
                str(watcher.get("target_id")) == str(target_id) and
                watcher.get("watch_type") == "watching"):
                return json.dumps({"error": "Subscription already exists"})
        
        subscription_id = generate_id(watchers)
        timestamp = "2025-10-01T00:00:00"
        
        notifications_enabled = True
        if notification_preferences:
            notifications_enabled = notification_preferences.get("notifications_enabled", True)
        
        new_subscription = {
            "watcher_id": subscription_id,
            "user_id": requesting_user_id,
            "target_type": target_type,
            "target_id": target_id,
            "watch_type": "watching",
            "notifications_enabled": notifications_enabled,
            "created_at": timestamp
        }
        
        watchers[str(subscription_id)] = new_subscription
        return json.dumps({"subscription_id": str(subscription_id), "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_subscription",
                "description": "Create a subscription for a user to watch a space, page, or user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "requesting_user_id": {"type": "string", "description": "ID of the user creating the subscription"},
                        "target_type": {"type": "string", "description": "Type of target (space, page, user)"},
                        "target_id": {"type": "string", "description": "ID of the space, page, or user to watch"},
                        "notification_preferences": {"type": "object", "description": "Notification settings with notifications_enabled (True/False)"}
                    },
                    "required": ["requesting_user_id", "target_type", "target_id"]
                }
            }
        }
EOF

# Create remove_subscription.py
cat > remove_subscription.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class RemoveSubscription(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], subscription_id: str, requesting_user_id: str) -> str:
        
        users = data.get("users", {})
        watchers = data.get("watchers", {})
        
        # Validate requesting user exists
        if str(requesting_user_id) not in users:
            return json.dumps({"error": f"Requesting user {requesting_user_id} not found"})
        
        # Validate subscription exists
        if str(subscription_id) not in watchers:
            return json.dumps({"error": f"Subscription {subscription_id} not found"})
        
        subscription = watchers[str(subscription_id)]
        
        # Verify ownership - user can only remove their own subscriptions
        if subscription.get("user_id") != requesting_user_id:
            return json.dumps({"error": "Permission denied: User can only remove their own subscriptions"})
        
        # Remove the subscription
        del watchers[str(subscription_id)]
        
        return json.dumps({"success": True, "message": "Subscription removed"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "remove_subscription",
                "description": "Remove a subscription for a user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "subscription_id": {"type": "string", "description": "ID of the subscription to remove"},
                        "requesting_user_id": {"type": "string", "description": "ID of the user removing the subscription"}
                    },
                    "required": ["subscription_id", "requesting_user_id"]
                }
            }
        }
EOF

# Create log_audit_action.py
cat > log_audit_action.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class LogAuditAction(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action_type: str, user_id: str, 
               target_type: str, target_id: str, timestamp: str,
               old_values: Optional[Dict[str, Any]] = None, 
               new_values: Optional[Dict[str, Any]] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            max_id = max(int(k) for k in table.keys() if k.isdigit())
            return str(max_id + 1)
        
        users = data.get("users", {})
        audit_logs = data.get("audit_logs", {})
        
        # Validate user exists
        if str(user_id) not in users:
            return json.dumps({"error": f"User {user_id} not found"})
        
        # Validate action_type
        valid_actions = ["create", "update", "delete"]
        if action_type not in valid_actions:
            return json.dumps({"error": f"Invalid action_type. Must be one of {valid_actions}"})
        
        # Validate required fields
        if not target_type:
            return json.dumps({"error": "target_type is required"})
        
        if not target_id:
            return json.dumps({"error": "target_id is required"})
        
        if not timestamp:
            return json.dumps({"error": "timestamp is required"})
        
        log_id = generate_id(audit_logs)
        
        new_audit_log = {
            "log_id": log_id,
            "user_id": user_id,
            "action": action_type,
            "reference_type": target_type,
            "reference_id": target_id,
            "field_name": None,
            "old_value": json.dumps(old_values) if old_values else None,
            "new_value": json.dumps(new_values) if new_values else None,
            "timestamp": timestamp
        }
        
        audit_logs[log_id] = new_audit_log
        return json.dumps({"audit_log_id": log_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "log_audit_action",
                "description": "Log an audit action performed by a user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action_type": {"type": "string", "description": "Type of action performed (create, update, delete)"},
                        "user_id": {"type": "string", "description": "ID of the user who performed the action"},
                        "target_type": {"type": "string", "description": "Type of target (space, page, comment, etc.)"},
                        "target_id": {"type": "string", "description": "ID of the target"},
                        "timestamp": {"type": "string", "description": "Timestamp of the action"},
                        "old_values": {"type": "object", "description": "Previous values before change"},
                        "new_values": {"type": "object", "description": "New values after change"}
                    },
                    "required": ["action_type", "user_id", "target_type", "target_id", "timestamp"]
                }
            }
        }
EOF

# Create get_user_permissions.py
cat > get_user_permissions.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetUserPermissions(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: str, space_id: Optional[str] = None, 
               page_id: Optional[str] = None) -> str:
        
        users = data.get("users", {})
        spaces = data.get("spaces", {})
        pages = data.get("pages", {})
        space_permissions = data.get("space_permissions", {})
        page_permissions = data.get("page_permissions", {})
        groups = data.get("groups", {})
        user_groups = data.get("user_groups", {})
        
        # Validate user exists
        if str(user_id) not in users:
            return json.dumps({"error": f"User {user_id} not found"})
        
        user = users[str(user_id)]
        permissions = {
            "user_id": user_id,
            "user_role": user.get("role"),
            "space_permissions": [],
            "page_permissions": [],
            "inherited_permissions": []
        }
        
        # Get user's groups
        user_group_ids = []
        for ug in user_groups.values():
            if ug.get("user_id") == user_id:
                user_group_ids.append(ug.get("group_id"))
        
        # Get space permissions
        if space_id:
            if str(space_id) not in spaces:
                return json.dumps({"error": f"Space {space_id} not found"})
            
            # Direct user space permissions
            for sp in space_permissions.values():
                if (sp.get("space_id") == space_id and 
                    sp.get("user_id") == user_id):
                    permissions["space_permissions"].append({
                        "permission_id": sp.get("space_permission_id"),
                        "permission_type": sp.get("permission_type"),
                        "granted_at": sp.get("granted_at"),
                        "granted_by_user_id": sp.get("granted_by_user_id")
                    })
            
            # Group-based space permissions
            for sp in space_permissions.values():
                if (sp.get("space_id") == space_id and 
                    sp.get("group_id") in user_group_ids):
                    group_name = groups.get(str(sp.get("group_id")), {}).get("name", "Unknown")
                    permissions["inherited_permissions"].append({
                        "permission_type": sp.get("permission_type"),
                        "source": "group",
                        "source_name": group_name,
                        "granted_at": sp.get("granted_at")
                    })
        
        # Get page permissions
        if page_id:
            if str(page_id) not in pages:
                return json.dumps({"error": f"Page {page_id} not found"})
            
            # Direct user page permissions
            for pp in page_permissions.values():
                if (pp.get("page_id") == page_id and 
                    pp.get("user_id") == user_id):
                    permissions["page_permissions"].append({
                        "permission_id": pp.get("page_permission_id"),
                        "permission_type": pp.get("permission_type"),
                        "granted_at": pp.get("granted_at"),
                        "granted_by_user_id": pp.get("granted_by_user_id")
                    })
            
            # Group-based page permissions
            for pp in page_permissions.values():
                if (pp.get("page_id") == page_id and 
                    pp.get("group_id") in user_group_ids):
                    group_name = groups.get(str(pp.get("group_id")), {}).get("name", "Unknown")
                    permissions["inherited_permissions"].append({
                        "permission_type": pp.get("permission_type"),
                        "source": "group",
                        "source_name": group_name,
                        "granted_at": pp.get("granted_at")
                    })
        
        # If neither space_id nor page_id provided, get all permissions
        if not space_id and not page_id:
            # All space permissions for user
            for sp in space_permissions.values():
                if sp.get("user_id") == user_id:
                    space_name = spaces.get(str(sp.get("space_id")), {}).get("name", "Unknown")
                    permissions["space_permissions"].append({
                        "space_id": sp.get("space_id"),
                        "space_name": space_name,
                        "permission_type": sp.get("permission_type"),
                        "granted_at": sp.get("granted_at")
                    })
            
            # All page permissions for user
            for pp in page_permissions.values():
                if pp.get("user_id") == user_id:
                    page_title = pages.get(str(pp.get("page_id")), {}).get("title", "Unknown")
                    permissions["page_permissions"].append({
                        "page_id": pp.get("page_id"),
                        "page_title": page_title,
                        "permission_type": pp.get("permission_type"),
                        "granted_at": pp.get("granted_at")
                    })
        
        return json.dumps(permissions)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_user_permissions",
                "description": "Get user permissions with inherited and explicit permissions",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "ID of the user to check permissions for"},
                        "space_id": {"type": "string", "description": "Space ID to check space-specific permissions"},
                        "page_id": {"type": "string", "description": "Page ID to check page-specific permissions"}
                    },
                    "required": ["user_id"]
                }
            }
        }
EOF

# Create get_page_dependencies.py
cat > get_page_dependencies.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetPageDependencies(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], page_id: str) -> str:
        
        pages = data.get("pages", {})
        page_links = data.get("page_links", {})
        attachments = data.get("attachments", {})
        comments = data.get("comments", {})
        
        # Validate page exists
        if str(page_id) not in pages:
            return json.dumps({"error": f"Page {page_id} not found"})
        
        page = pages[str(page_id)]
        dependencies = {
            "page_id": page_id,
            "page_title": page.get("title"),
            "child_pages": [],
            "parent_page": None,
            "linked_from": [],
            "links_to": [],
            "attachments": [],
            "comments_count": 0
        }
        
        # Get parent page
        if page.get("parent_page_id"):
            parent_page = pages.get(str(page.get("parent_page_id")))
            if parent_page:
                dependencies["parent_page"] = {
                    "page_id": page.get("parent_page_id"),
                    "title": parent_page.get("title")
                }
        
        # Get child pages
        for child_page in pages.values():
            if str(child_page.get("parent_page_id")) == str(page_id):
                dependencies["child_pages"].append({
                    "page_id": child_page.get("page_id"),
                    "title": child_page.get("title"),
                    "status": child_page.get("status")
                })
        
        # Get outgoing links from this page
        for link in page_links.values():
            if str(link.get("source_page_id")) == str(page_id):
                dependencies["links_to"].append({
                    "link_id": link.get("link_id"),
                    "target_url": link.get("target_url"),
                    "link_text": link.get("link_text"),
                    "link_type": link.get("link_type"),
                    "is_broken": link.get("is_broken")
                })
        
        # Get incoming links to this page (internal links only)
        for link in page_links.values():
            if (link.get("link_type") == "internal" and 
                str(page_id) in str(link.get("target_url"))):
                source_page = pages.get(str(link.get("source_page_id")))
                if source_page:
                    dependencies["linked_from"].append({
                        "link_id": link.get("link_id"),
                        "source_page_id": link.get("source_page_id"),
                        "source_page_title": source_page.get("title"),
                        "link_text": link.get("link_text")
                    })
        
        # Get attachments
        for attachment in attachments.values():
            if str(attachment.get("page_id")) == str(page_id):
                dependencies["attachments"].append({
                    "attachment_id": attachment.get("attachment_id"),
                    "filename": attachment.get("filename"),
                    "original_filename": attachment.get("original_filename"),
                    "mime_type": attachment.get("mime_type"),
                    "file_size": attachment.get("file_size"),
                    "created_at": attachment.get("created_at")
                })
        
        # Count comments
        comment_count = 0
        for comment in comments.values():
            if str(comment.get("page_id")) == str(page_id) and comment.get("status") == "active":
                comment_count += 1
        dependencies["comments_count"] = comment_count
        
        return json.dumps(dependencies)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_page_dependencies",
                "description": "Get page dependencies and their relationships",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "page_id": {"type": "string", "description": "ID of the page to check dependencies for"}
                    },
                    "required": ["page_id"]
                }
            }
        }
EOF

# Create get_space_info.py
cat > get_space_info.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetSpaceInfo(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], space_id: Optional[str] = None, 
               space_name: Optional[str] = None, owner_id: Optional[str] = None) -> str:
        
        spaces = data.get("spaces", {})
        users = data.get("users", {})
        pages = data.get("pages", {})
        space_permissions = data.get("space_permissions", {})
        results = []
        
        # Filter spaces based on criteria
        for space in spaces.values():
            if space_id and str(space.get("space_id")) != str(space_id):
                continue
            if space_name and space_name.lower() not in space.get("name", "").lower():
                continue
            if owner_id and str(space.get("created_by_user_id")) != str(owner_id):
                continue
            
            # Get space owner info
            owner = users.get(str(space.get("created_by_user_id")), {})
            
            # Count pages in space
            page_count = 0
            for page in pages.values():
                if (str(page.get("space_id")) == str(space.get("space_id")) and 
                    page.get("status") == "current"):
                    page_count += 1
            
            # Get homepage info
            homepage_info = None
            if space.get("homepage_id"):
                homepage = pages.get(str(space.get("homepage_id")))
                if homepage:
                    homepage_info = {
                        "page_id": space.get("homepage_id"),
                        "title": homepage.get("title")
                    }
            
            # Get space permissions summary
            permissions_summary = {
                "view_permissions": 0,
                "contribute_permissions": 0,
                "moderate_permissions": 0
            }
            
            for perm in space_permissions.values():
                if str(perm.get("space_id")) == str(space.get("space_id")):
                    perm_type = perm.get("permission_type")
                    if perm_type == "view":
                        permissions_summary["view_permissions"] += 1
                    elif perm_type == "contribute":
                        permissions_summary["contribute_permissions"] += 1
                    elif perm_type == "moderate":
                        permissions_summary["moderate_permissions"] += 1
            
            space_info = {
                "space_id": space.get("space_id"),
                "space_key": space.get("space_key"),
                "name": space.get("name"),
                "description": space.get("description"),
                "type": space.get("type"),
                "status": space.get("status"),
                "anonymous_access": space.get("anonymous_access"),
                "public_signup": space.get("public_signup"),
                "theme": space.get("theme"),
                "logo_url": space.get("logo_url"),
                "homepage": homepage_info,
                "page_count": page_count,
                "owner": {
                    "user_id": space.get("created_by_user_id"),
                    "username": owner.get("username", "Unknown"),
                    "display_name": owner.get("display_name", "Unknown")
                },
                "permissions_summary": permissions_summary,
                "created_at": space.get("created_at"),
                "updated_at": space.get("updated_at")
            }
            
            results.append(space_info)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_space_info",
                "description": "Get space information with configuration and permissions",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "space_id": {"type": "string", "description": "Filter by space ID"},
                        "space_name": {"type": "string", "description": "Filter by space name"},
                        "owner_id": {"type": "string", "description": "Filter by space owner ID"}
                    },
                    "required": []
                }
            }
        }
EOF
