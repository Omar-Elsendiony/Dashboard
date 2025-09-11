#!/bin/bash

# Create get_labels.py
cat > get_labels.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetLabels(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], label_id: Optional[str] = None, name: Optional[str] = None,
               space_id: Optional[str] = None, creator_id: Optional[str] = None, color: Optional[str] = None) -> str:
        
        labels = data.get("labels", {})
        result = []
        
        for lid, label in labels.items():
            # Apply filters
            if label_id and str(label_id) != lid:
                continue
            if name and label.get("name").lower() != name.lower():
                continue
            if space_id and label.get("space_id") != space_id:
                continue
            if creator_id and label.get("created_by_user_id") != creator_id:
                continue
            if color and label.get("color") != color:
                continue
            
            result.append({
                "label_id": lid,
                "name": label.get("name"),
                "color": label.get("color"),
                "description": label.get("description"),
                "space_id": label.get("space_id"),
                "created_by_user_id": label.get("created_by_user_id"),
                "usage_count": label.get("usage_count"),
                "created_at": label.get("created_at")
            })
        
        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_labels",
                "description": "Get labels matching filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "label_id": {"type": "string", "description": "ID of the label"},
                        "name": {"type": "string", "description": "Name of the label"},
                        "space_id": {"type": "string", "description": "ID of the space containing the label"},
                        "creator_id": {"type": "string", "description": "ID of the user who created the label"},
                        "color": {"type": "string", "description": "Color of the label"}
                    },
                    "required": []
                }
            }
        }
EOF

# Create get_page_labels.py
cat > get_page_labels.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetPageLabels(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], page_label_id: Optional[str] = None, page_id: Optional[str] = None,
               label_id: Optional[str] = None, added_by_user_id: Optional[str] = None) -> str:
        
        page_labels = data.get("page_labels", {})
        result = []
        
        for plid, page_label in page_labels.items():
            # Apply filters
            if page_label_id and str(page_label_id) != plid:
                continue
            if page_id and page_label.get("page_id") != page_id:
                continue
            if label_id and page_label.get("label_id") != label_id:
                continue
            if added_by_user_id and page_label.get("added_by_user_id") != added_by_user_id:
                continue
            
            result.append({
                "page_label_id": plid,
                "page_id": page_label.get("page_id"),
                "label_id": page_label.get("label_id"),
                "added_at": page_label.get("added_at"),
                "added_by_user_id": page_label.get("added_by_user_id")
            })
        
        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_page_labels",
                "description": "Get page-label relationships matching filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "page_label_id": {"type": "string", "description": "ID of the page-label relationship"},
                        "page_id": {"type": "string", "description": "ID of the page"},
                        "label_id": {"type": "string", "description": "ID of the label"},
                        "added_by_user_id": {"type": "string", "description": "ID of the user who added the label to the page"}
                    },
                    "required": []
                }
            }
        }
EOF

# Create get_notifications.py
cat > get_notifications.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetNotifications(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], notification_id: Optional[str] = None, user_id: Optional[str] = None,
               type: Optional[str] = None, target_type: Optional[str] = None, target_id: Optional[str] = None,
               is_read: Optional[bool] = None) -> str:
        
        notifications = data.get("notifications", {})
        result = []
        
        for nid, notification in notifications.items():
            # Apply filters
            if notification_id and str(notification_id) != nid:
                continue
            if user_id and notification.get("user_id") != user_id:
                continue
            if type and notification.get("type") != type:
                continue
            if target_type and notification.get("target_type") != target_type:
                continue
            if target_id and notification.get("target_id") != target_id:
                continue
            if is_read is not None and notification.get("is_read") != is_read:
                continue
            
            result.append({
                "notification_id": nid,
                "user_id": notification.get("user_id"),
                "type": notification.get("type"),
                "title": notification.get("title"),
                "message": notification.get("message"),
                "target_type": notification.get("target_type"),
                "target_id": notification.get("target_id"),
                "is_read": notification.get("is_read"),
                "read_at": notification.get("read_at"),
                "delivery_method": notification.get("delivery_method"),
                "email_sent": notification.get("email_sent"),
                "created_at": notification.get("created_at"),
                "created_by_user_id": notification.get("created_by_user_id")
            })
        
        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_notifications",
                "description": "Get notifications matching filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "notification_id": {"type": "string", "description": "ID of the notification"},
                        "user_id": {"type": "string", "description": "ID of the user who received the notification"},
                        "type": {"type": "string", "description": "Type of notification (page_created, page_updated, page_deleted, comment_added, comment_replied, comment_resolved, attachment_uploaded, attachment_updated, attachment_deleted, label_added, label_removed, space_created, space_updated, space_archived, space_member_added, space_member_removed, user_mentioned, permission_granted, permission_revoked)"},
                        "target_type": {"type": "string", "description": "Type of target (space, page, comment)"},
                        "target_id": {"type": "string", "description": "ID of the target entity"},
                        "is_read": {"type": "boolean", "description": "Whether notification has been read (True/False)"}
                    },
                    "required": []
                }
            }
        }
EOF

# Create get_watchers.py
cat > get_watchers.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetWatchers(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], watcher_id: Optional[str] = None, user_id: Optional[str] = None,
               target_type: Optional[str] = None, target_id: Optional[str] = None, watch_type: Optional[str] = None) -> str:
        
        watchers = data.get("watchers", {})
        result = []
        
        for wid, watcher in watchers.items():
            # Apply filters
            if watcher_id and str(watcher_id) != wid:
                continue
            if user_id and watcher.get("user_id") != user_id:
                continue
            if target_type and watcher.get("target_type") != target_type:
                continue
            if target_id and watcher.get("target_id") != target_id:
                continue
            if watch_type and watcher.get("watch_type") != watch_type:
                continue
            
            result.append({
                "watcher_id": wid,
                "user_id": watcher.get("user_id"),
                "target_type": watcher.get("target_type"),
                "target_id": watcher.get("target_id"),
                "watch_type": watcher.get("watch_type"),
                "notifications_enabled": watcher.get("notifications_enabled"),
                "created_at": watcher.get("created_at")
            })
        
        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_watchers",
                "description": "Get watchers matching filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "watcher_id": {"type": "string", "description": "ID of the watcher"},
                        "user_id": {"type": "string", "description": "ID of the user who is watching"},
                        "target_type": {"type": "string", "description": "Type of target being watched (space, page, user)"},
                        "target_id": {"type": "string", "description": "ID of the target being watched"},
                        "watch_type": {"type": "string", "description": "Type of watch (watching, not_watching)"}
                    },
                    "required": []
                }
            }
        }
EOF

# Create get_audit_logs.py
cat > get_audit_logs.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetAuditLogs(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], log_id: Optional[str] = None, user_id: Optional[str] = None,
               action: Optional[str] = None, reference_type: Optional[str] = None, reference_id: Optional[str] = None) -> str:
        
        audit_logs = data.get("audit_logs", {})
        result = []
        
        for alid, log in audit_logs.items():
            # Apply filters
            if log_id and str(log_id) != alid:
                continue
            if user_id and log.get("user_id") != user_id:
                continue
            if action and log.get("action") != action:
                continue
            if reference_type and log.get("reference_type") != reference_type:
                continue
            if reference_id and log.get("reference_id") != reference_id:
                continue
            
            result.append({
                "log_id": alid,
                "user_id": log.get("user_id"),
                "action": log.get("action"),
                "reference_type": log.get("reference_type"),
                "reference_id": log.get("reference_id"),
                "field_name": log.get("field_name"),
                "old_value": log.get("old_value"),
                "new_value": log.get("new_value"),
                "timestamp": log.get("timestamp")
            })
        
        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_audit_logs",
                "description": "Get audit logs matching filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "log_id": {"type": "string", "description": "ID of the audit log"},
                        "user_id": {"type": "string", "description": "ID of the user who performed the action"},
                        "action": {"type": "string", "description": "Action performed (create, update, delete)"},
                        "reference_type": {"type": "string", "description": "Type of entity that was modified"},
                        "reference_id": {"type": "string", "description": "ID of the entity that was modified"}
                    },
                    "required": []
                }
            }
        }
EOF

# Create get_page_links.py
cat > get_page_links.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetPageLinks(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], link_id: Optional[str] = None, source_page_id: Optional[str] = None,
               target_url: Optional[str] = None, link_type: Optional[str] = None, is_broken: Optional[bool] = None) -> str:
        
        page_links = data.get("page_links", {})
        result = []
        
        for plid, link in page_links.items():
            # Apply filters
            if link_id and str(link_id) != plid:
                continue
            if source_page_id and link.get("source_page_id") != source_page_id:
                continue
            if target_url and link.get("target_url") != target_url:
                continue
            if link_type and link.get("link_type") != link_type:
                continue
            if is_broken is not None and link.get("is_broken") != is_broken:
                continue
            
            result.append({
                "link_id": plid,
                "source_page_id": link.get("source_page_id"),
                "target_url": link.get("target_url"),
                "link_text": link.get("link_text"),
                "link_type": link.get("link_type"),
                "is_broken": link.get("is_broken"),
                "last_checked_at": link.get("last_checked_at"),
                "created_at": link.get("created_at")
            })
        
        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_page_links",
                "description": "Get page links matching filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "link_id": {"type": "string", "description": "ID of the link"},
                        "source_page_id": {"type": "string", "description": "ID of the page containing the link"},
                        "target_url": {"type": "string", "description": "URL that the link points to"},
                        "link_type": {"type": "string", "description": "Type of link (internal, external)"},
                        "is_broken": {"type": "boolean", "description": "Whether the link is broken (True/False)"}
                    },
                    "required": []
                }
            }
        }
EOF

# Create find_broken_links.py
cat > find_broken_links.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class FindBrokenLinks(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], space_id: Optional[str] = None) -> str:
        
        page_links = data.get("page_links", {})
        pages = data.get("pages", {})
        result = []
        
        for link_id, link in page_links.items():
            # Only return broken links
            if not link.get("is_broken", False):
                continue
            
            # If space_id filter is provided, check if source page is in that space
            if space_id:
                source_page_id = link.get("source_page_id")
                if source_page_id and str(source_page_id) in pages:
                    page = pages[str(source_page_id)]
                    if page.get("space_id") != space_id:
                        continue
                else:
                    continue
            
            result.append({
                "link_id": link_id,
                "source_page_id": link.get("source_page_id"),
                "target_url": link.get("target_url"),
                "link_text": link.get("link_text"),
                "link_type": link.get("link_type"),
                "is_broken": link.get("is_broken"),
                "last_checked_at": link.get("last_checked_at"),
                "created_at": link.get("created_at")
            })
        
        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "find_broken_links",
                "description": "Find broken links, optionally filtered by space",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "space_id": {"type": "string", "description": "ID of the space to search for broken links (optional)"}
                    },
                    "required": []
                }
            }
        }
EOF

echo "Additional tool files have been generated successfully!"
echo "Files created:"
echo "- get_labels.py"
echo "- get_page_labels.py"
echo "- get_notifications.py"
echo "- get_watchers.py"
echo "- get_audit_logs.py"
echo "- get_page_links.py"
echo "- find_broken_links.py"