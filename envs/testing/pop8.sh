#!/bin/bash

# Create get_users.py
cat > get_users.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetUsers(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: Optional[str] = None, username: Optional[str] = None,
               role: Optional[str] = None, email: Optional[str] = None, status: Optional[str] = None) -> str:
        
        users = data.get("users", {})
        result = []
        
        for uid, user in users.items():
            # Apply filters
            if user_id and str(user_id) != uid:
                continue
            if username and user.get("username", "").lower() != username.lower():
                continue
            if role and user.get("role") != role:
                continue
            if email and user.get("email", "").lower() != email.lower():
                continue
            if status and user.get("status") != status:
                continue
            
            result.append({
                "user_id": uid,
                "username": user.get("username"),
                "role": user.get("role"),
                "email": user.get("email"),
                "first_name": user.get("first_name"),
                "last_name": user.get("last_name"),
                "display_name": user.get("display_name"),
                "timezone": user.get("timezone"),
                "status": user.get("status"),
                "created_at": user.get("created_at"),
                "updated_at": user.get("updated_at")
            })
        
        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_users",
                "description": "Get users matching filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "ID of the user"},
                        "username": {"type": "string", "description": "Username of the user"},
                        "role": {"type": "string", "description": "Role of the user (PlatformOwner, WikiProgramManager, User)"},
                        "email": {"type": "string", "description": "Email of the user"},
                        "status": {"type": "string", "description": "Status of the user (active, inactive, suspended)"}
                    },
                    "required": []
                }
            }
        }
EOF

# Create get_spaces.py
cat > get_spaces.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetSpaces(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], space_id: Optional[str] = None, space_key: Optional[str] = None,
               creator_id: Optional[str] = None, type: Optional[str] = None, status: Optional[str] = None) -> str:
        
        spaces = data.get("spaces", {})
        result = []
        
        for sid, space in spaces.items():
            # Apply filters
            if space_id and str(space_id) != sid:
                continue
            if space_key and space.get("space_key") != space_key:
                continue
            if creator_id and space.get("created_by_user_id") != creator_id:
                continue
            if type and space.get("type") != type:
                continue
            if status and space.get("status") != status:
                continue
            
            result.append({
                "space_id": sid,
                "space_key": space.get("space_key"),
                "name": space.get("name"),
                "description": space.get("description"),
                "type": space.get("type"),
                "status": space.get("status"),
                "homepage_id": space.get("homepage_id"),
                "theme": space.get("theme"),
                "logo_url": space.get("logo_url"),
                "anonymous_access": space.get("anonymous_access"),
                "public_signup": space.get("public_signup"),
                "created_at": space.get("created_at"),
                "updated_at": space.get("updated_at"),
                "created_by_user_id": space.get("created_by_user_id")
            })
        
        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_spaces",
                "description": "Get spaces matching filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "space_id": {"type": "string", "description": "ID of the space"},
                        "space_key": {"type": "string", "description": "Key of the space"},
                        "creator_id": {"type": "string", "description": "ID of the user who created the space"},
                        "type": {"type": "string", "description": "Type of space (global, personal, private)"},
                        "status": {"type": "string", "description": "Status of space (current, archived)"}
                    },
                    "required": []
                }
            }
        }
EOF

# Create get_pages.py
cat > get_pages.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetPages(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], page_id: Optional[str] = None, space_id: Optional[str] = None,
               parent_page_id: Optional[str] = None, creator_id: Optional[str] = None,
               status: Optional[str] = None, template_id: Optional[str] = None) -> str:
        
        pages = data.get("pages", {})
        result = []
        
        for pid, page in pages.items():
            # Apply filters
            if page_id and str(page_id) != pid:
                continue
            if space_id and page.get("space_id") != space_id:
                continue
            if parent_page_id and page.get("parent_page_id") != parent_page_id:
                continue
            if creator_id and page.get("created_by_user_id") != creator_id:
                continue
            if status and page.get("status") != status:
                continue
            if template_id and page.get("template_id") != template_id:
                continue
            
            result.append({
                "page_id": pid,
                "space_id": page.get("space_id"),
                "title": page.get("title"),
                "content": page.get("content"),
                "content_format": page.get("content_format"),
                "parent_page_id": page.get("parent_page_id"),
                "position": page.get("position"),
                "status": page.get("status"),
                "version": page.get("version"),
                "template_id": page.get("template_id"),
                "created_at": page.get("created_at"),
                "updated_at": page.get("updated_at"),
                "published_at": page.get("published_at"),
                "created_by_user_id": page.get("created_by_user_id"),
                "last_modified_by_user_id": page.get("last_modified_by_user_id")
            })
        
        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_pages",
                "description": "Get pages matching filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "page_id": {"type": "string", "description": "ID of the page"},
                        "space_id": {"type": "string", "description": "ID of the space containing the page"},
                        "parent_page_id": {"type": "string", "description": "ID of the parent page"},
                        "creator_id": {"type": "string", "description": "ID of the user who created the page"},
                        "status": {"type": "string", "description": "Status of page (current, draft, deleted, historical)"},
                        "template_id": {"type": "string", "description": "ID of the template used for the page"}
                    },
                    "required": []
                }
            }
        }
EOF

# Create get_page_versions.py
cat > get_page_versions.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetPageVersions(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], page_version_id: Optional[str] = None, page_id: Optional[str] = None,
               creator_id: Optional[str] = None, change_type: Optional[str] = None) -> str:
        
        page_versions = data.get("page_versions", {})
        result = []
        
        for pvid, version in page_versions.items():
            # Apply filters
            if page_version_id and str(page_version_id) != pvid:
                continue
            if page_id and version.get("page_id") != page_id:
                continue
            if creator_id and version.get("created_by_user_id") != creator_id:
                continue
            if change_type and version.get("change_type") != change_type:
                continue
            
            result.append({
                "page_version_id": pvid,
                "page_id": version.get("page_id"),
                "version_number": version.get("version_number"),
                "title": version.get("title"),
                "content": version.get("content"),
                "content_format": version.get("content_format"),
                "change_type": version.get("change_type"),
                "created_at": version.get("created_at"),
                "created_by_user_id": version.get("created_by_user_id")
            })
        
        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_page_versions",
                "description": "Get page versions matching filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "page_version_id": {"type": "string", "description": "ID of the page version"},
                        "page_id": {"type": "string", "description": "ID of the page"},
                        "creator_id": {"type": "string", "description": "ID of the user who created the version"},
                        "change_type": {"type": "string", "description": "Type of change (major, minor)"}
                    },
                    "required": []
                }
            }
        }
EOF

# Create get_templates.py
cat > get_templates.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetTemplates(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], template_id: Optional[str] = None, space_id: Optional[str] = None,
               creator_id: Optional[str] = None, is_global: Optional[bool] = None, category: Optional[str] = None) -> str:
        
        templates = data.get("page_templates", {})
        result = []
        
        for tid, template in templates.items():
            # Apply filters
            if template_id and str(template_id) != tid:
                continue
            if space_id and template.get("space_id") != space_id:
                continue
            if creator_id and template.get("created_by_user_id") != creator_id:
                continue
            if is_global is not None and template.get("is_global") != is_global:
                continue
            if category and template.get("category") != category:
                continue
            
            result.append({
                "template_id": tid,
                "name": template.get("name"),
                "description": template.get("description"),
                "content": template.get("content"),
                "content_format": template.get("content_format"),
                "space_id": template.get("space_id"),
                "is_global": template.get("is_global"),
                "category": template.get("category"),
                "usage_count": template.get("usage_count"),
                "created_at": template.get("created_at"),
                "updated_at": template.get("updated_at"),
                "created_by_user_id": template.get("created_by_user_id")
            })
        
        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_templates",
                "description": "Get templates matching filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "template_id": {"type": "string", "description": "ID of the template"},
                        "space_id": {"type": "string", "description": "ID of the space containing the template"},
                        "creator_id": {"type": "string", "description": "ID of the user who created the template"},
                        "is_global": {"type": "boolean", "description": "Whether template is global (True/False)"},
                        "category": {"type": "string", "description": "Category of the template"}
                    },
                    "required": []
                }
            }
        }
EOF

# Create get_comments.py
cat > get_comments.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetComments(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], comment_id: Optional[str] = None, page_id: Optional[str] = None,
               parent_comment_id: Optional[str] = None, creator_id: Optional[str] = None,
               status: Optional[str] = None) -> str:
        
        comments = data.get("comments", {})
        result = []
        
        for cid, comment in comments.items():
            # Apply filters
            if comment_id and str(comment_id) != cid:
                continue
            if page_id and comment.get("page_id") != page_id:
                continue
            if parent_comment_id and comment.get("parent_comment_id") != parent_comment_id:
                continue
            if creator_id and comment.get("created_by_user_id") != creator_id:
                continue
            if status and comment.get("status") != status:
                continue
            
            result.append({
                "comment_id": cid,
                "page_id": comment.get("page_id"),
                "parent_comment_id": comment.get("parent_comment_id"),
                "content": comment.get("content"),
                "content_format": comment.get("content_format"),
                "status": comment.get("status"),
                "thread_level": comment.get("thread_level"),
                "created_at": comment.get("created_at"),
                "updated_at": comment.get("updated_at"),
                "created_by_user_id": comment.get("created_by_user_id")
            })
        
        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_comments",
                "description": "Get comments matching filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "comment_id": {"type": "string", "description": "ID of the comment"},
                        "page_id": {"type": "string", "description": "ID of the page containing the comment"},
                        "parent_comment_id": {"type": "string", "description": "ID of the parent comment"},
                        "creator_id": {"type": "string", "description": "ID of the user who created the comment"},
                        "status": {"type": "string", "description": "Status of comment (active, deleted, resolved)"}
                    },
                    "required": []
                }
            }
        }
EOF

# Create get_attachments.py
cat > get_attachments.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetAttachments(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], attachment_id: Optional[str] = None, page_id: Optional[str] = None,
               comment_id: Optional[str] = None, uploader_id: Optional[str] = None,
               mime_type: Optional[str] = None) -> str:
        
        attachments = data.get("attachments", {})
        result = []
        
        for aid, attachment in attachments.items():
            # Apply filters
            if attachment_id and str(attachment_id) != aid:
                continue
            if page_id and attachment.get("page_id") != page_id:
                continue
            if comment_id and attachment.get("comment_id") != comment_id:
                continue
            if uploader_id and attachment.get("uploaded_by_user_id") != uploader_id:
                continue
            if mime_type and attachment.get("mime_type") != mime_type:
                continue
            
            result.append({
                "attachment_id": aid,
                "page_id": attachment.get("page_id"),
                "comment_id": attachment.get("comment_id"),
                "filename": attachment.get("filename"),
                "original_filename": attachment.get("original_filename"),
                "mime_type": attachment.get("mime_type"),
                "file_size": attachment.get("file_size"),
                "storage_path": attachment.get("storage_path"),
                "storage_type": attachment.get("storage_type"),
                "image_width": attachment.get("image_width"),
                "image_height": attachment.get("image_height"),
                "version": attachment.get("version"),
                "created_at": attachment.get("created_at"),
                "uploaded_by_user_id": attachment.get("uploaded_by_user_id")
            })
        
        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_attachments",
                "description": "Get attachments matching filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "attachment_id": {"type": "string", "description": "ID of the attachment"},
                        "page_id": {"type": "string", "description": "ID of the page containing the attachment"},
                        "comment_id": {"type": "string", "description": "ID of the comment containing the attachment"},
                        "uploader_id": {"type": "string", "description": "ID of the user who uploaded the attachment"},
                        "mime_type": {"type": "string", "description": "MIME type of the attachment"}
                    },
                    "required": []
                }
            }
        }
EOF

# Create get_groups.py
cat > get_groups.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetGroups(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], group_id: Optional[str] = None, name: Optional[str] = None,
               type: Optional[str] = None, creator_id: Optional[str] = None) -> str:
        
        groups = data.get("groups", {})
        result = []
        
        for gid, group in groups.items():
            # Apply filters
            if group_id and str(group_id) != gid:
                continue
            if name and group.get("name").lower() != name.lower():
                continue
            if type and group.get("type") != type:
                continue
            if creator_id and group.get("created_by_user_id") != creator_id:
                continue
            
            result.append({
                "group_id": gid,
                "name": group.get("name"),
                "description": group.get("description"),
                "type": group.get("type"),
                "created_at": group.get("created_at"),
                "created_by_user_id": group.get("created_by_user_id")
            })
        
        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_groups",
                "description": "Get groups matching filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "group_id": {"type": "string", "description": "ID of the group"},
                        "name": {"type": "string", "description": "Name of the group"},
                        "type": {"type": "string", "description": "Type of group (system, custom)"},
                        "creator_id": {"type": "string", "description": "ID of the user who created the group"}
                    },
                    "required": []
                }
            }
        }
EOF

echo "All tool files have been generated successfully!"
echo "Files created:"
echo "- get_users.py"
echo "- get_spaces.py" 
echo "- get_pages.py"
echo "- get_page_versions.py"
echo "- get_templates.py"
echo "- get_comments.py"
echo "- get_attachments.py"
echo "- get_groups.py"