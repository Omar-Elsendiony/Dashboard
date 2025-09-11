#!/bin/bash

# Create get_comment_by_id.py
cat > get_comment_by_id.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetCommentById(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], comment_id: str) -> str:
        
        comments = data.get("comments", {})
        
        # Validate comment exists
        if str(comment_id) not in comments:
            return json.dumps({"error": f"Comment {comment_id} not found"})
        
        comment = comments[str(comment_id)]
        
        return json.dumps(comment)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_comment_by_id",
                "description": "Get a comment by its ID",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "comment_id": {"type": "string", "description": "ID of the comment to retrieve"}
                    },
                    "required": ["comment_id"]
                }
            }
        }
EOF

# Create get_comments_by_page.py
cat > get_comments_by_page.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetCommentsByPage(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], page_id: str) -> str:
        
        comments = data.get("comments", {})
        pages = data.get("pages", {})
        
        # Validate page exists
        if str(page_id) not in pages:
            return json.dumps({"error": f"Page {page_id} not found"})
        
        # Find comments for the page
        page_comments = []
        for comment in comments.values():
            if comment.get("page_id") == page_id:
                page_comments.append(comment)
        
        return json.dumps(page_comments)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_comments_by_page",
                "description": "Get all comments on a specific page",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "page_id": {"type": "string", "description": "ID of the page to get comments for"}
                    },
                    "required": ["page_id"]
                }
            }
        }
EOF

# Create get_comments_by_user.py
cat > get_comments_by_user.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetCommentsByUser(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], created_by_user_id: str) -> str:
        
        comments = data.get("comments", {})
        users = data.get("users", {})
        
        # Validate user exists
        if str(created_by_user_id) not in users:
            return json.dumps({"error": f"User {created_by_user_id} not found"})
        
        # Find comments by the user
        user_comments = []
        for comment in comments.values():
            if comment.get("created_by_user_id") == created_by_user_id:
                user_comments.append(comment)
        
        return json.dumps(user_comments)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_comments_by_user",
                "description": "Get all comments created by a specific user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "created_by_user_id": {"type": "string", "description": "ID of the user to get comments for"}
                    },
                    "required": ["created_by_user_id"]
                }
            }
        }
EOF

# Create get_comments_by_parent.py
cat > get_comments_by_parent.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetCommentsByParent(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], parent_comment_id: str) -> str:
        
        comments = data.get("comments", {})
        
        # Validate parent comment exists
        if str(parent_comment_id) not in comments:
            return json.dumps({"error": f"Parent comment {parent_comment_id} not found"})
        
        # Find reply comments
        reply_comments = []
        for comment in comments.values():
            if comment.get("parent_comment_id") == parent_comment_id:
                reply_comments.append(comment)
        
        return json.dumps(reply_comments)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_comments_by_parent",
                "description": "Get all reply comments to a parent comment",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "parent_comment_id": {"type": "string", "description": "ID of the parent comment to get replies for"}
                    },
                    "required": ["parent_comment_id"]
                }
            }
        }
EOF

# Create get_comments_by_status.py
cat > get_comments_by_status.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetCommentsByStatus(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], status: str) -> str:
        
        comments = data.get("comments", {})
        
        # Validate status
        valid_statuses = ['active', 'deleted', 'resolved']
        if status not in valid_statuses:
            return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}"})
        
        # Find comments with the specified status
        status_comments = []
        for comment in comments.values():
            if comment.get("status") == status:
                status_comments.append(comment)
        
        return json.dumps(status_comments)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_comments_by_status",
                "description": "Get all comments with a specific status",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string", "description": "Status of comments to retrieve (active, deleted, resolved)"}
                    },
                    "required": ["status"]
                }
            }
        }
EOF

# Create get_attachment_by_id.py
cat > get_attachment_by_id.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetAttachmentById(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], attachment_id: str) -> str:
        
        attachments = data.get("attachments", {})
        
        # Validate attachment exists
        if str(attachment_id) not in attachments:
            return json.dumps({"error": f"Attachment {attachment_id} not found"})
        
        attachment = attachments[str(attachment_id)]
        
        return json.dumps(attachment)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_attachment_by_id",
                "description": "Get an attachment by its ID",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "attachment_id": {"type": "string", "description": "ID of the attachment to retrieve"}
                    },
                    "required": ["attachment_id"]
                }
            }
        }
EOF

# Create get_attachments_by_page.py
cat > get_attachments_by_page.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetAttachmentsByPage(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], page_id: str) -> str:
        
        attachments = data.get("attachments", {})
        pages = data.get("pages", {})
        
        # Validate page exists
        if str(page_id) not in pages:
            return json.dumps({"error": f"Page {page_id} not found"})
        
        # Find attachments for the page
        page_attachments = []
        for attachment in attachments.values():
            if attachment.get("page_id") == page_id:
                page_attachments.append(attachment)
        
        return json.dumps(page_attachments)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_attachments_by_page",
                "description": "Get all attachments on a specific page",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "page_id": {"type": "string", "description": "ID of the page to get attachments for"}
                    },
                    "required": ["page_id"]
                }
            }
        }
EOF

# Create get_attachments_by_comment.py
cat > get_attachments_by_comment.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetAttachmentsByComment(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], comment_id: str) -> str:
        
        attachments = data.get("attachments", {})
        comments = data.get("comments", {})
        
        # Validate comment exists
        if str(comment_id) not in comments:
            return json.dumps({"error": f"Comment {comment_id} not found"})
        
        # Find attachments for the comment
        comment_attachments = []
        for attachment in attachments.values():
            if attachment.get("comment_id") == comment_id:
                comment_attachments.append(attachment)
        
        return json.dumps(comment_attachments)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_attachments_by_comment",
                "description": "Get all attachments on a specific comment",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "comment_id": {"type": "string", "description": "ID of the comment to get attachments for"}
                    },
                    "required": ["comment_id"]
                }
            }
        }
EOF

# Create get_attachments_by_uploader.py
cat > get_attachments_by_uploader.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetAttachmentsByUploader(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], uploaded_by_user_id: str) -> str:
        
        attachments = data.get("attachments", {})
        users = data.get("users", {})
        
        # Validate user exists
        if str(uploaded_by_user_id) not in users:
            return json.dumps({"error": f"User {uploaded_by_user_id} not found"})
        
        # Find attachments uploaded by the user
        user_attachments = []
        for attachment in attachments.values():
            if attachment.get("uploaded_by_user_id") == uploaded_by_user_id:
                user_attachments.append(attachment)
        
        return json.dumps(user_attachments)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_attachments_by_uploader",
                "description": "Get all attachments uploaded by a specific user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "uploaded_by_user_id": {"type": "string", "description": "ID of the user to get attachments for"}
                    },
                    "required": ["uploaded_by_user_id"]
                }
            }
        }
EOF

# Create get_group_by_id.py
cat > get_group_by_id.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetGroupById(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], group_id: str) -> str:
        
        groups = data.get("groups", {})
        
        # Validate group exists
        if str(group_id) not in groups:
            return json.dumps({"error": f"Group {group_id} not found"})
        
        group = groups[str(group_id)]
        
        return json.dumps(group)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_group_by_id",
                "description": "Get a group by its ID",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "group_id": {"type": "string", "description": "ID of the group to retrieve"}
                    },
                    "required": ["group_id"]
                }
            }
        }
EOF

# Create get_groups_by_type.py
cat > get_groups_by_type.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetGroupsByType(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], type: str) -> str:
        
        groups = data.get("groups", {})
        
        # Validate type
        valid_types = ['system', 'custom']
        if type not in valid_types:
            return json.dumps({"error": f"Invalid type. Must be one of {valid_types}"})
        
        # Find groups with the specified type
        type_groups = []
        for group in groups.values():
            if group.get("type") == type:
                type_groups.append(group)
        
        return json.dumps(type_groups)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_groups_by_type",
                "description": "Get all groups with a specific type",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "type": {"type": "string", "description": "Type of groups to retrieve (system, custom)"}
                    },
                    "required": ["type"]
                }
            }
        }
EOF

# Create get_groups_by_creator.py
cat > get_groups_by_creator.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetGroupsByCreator(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], created_by_user_id: str) -> str:
        
        groups = data.get("groups", {})
        users = data.get("users", {})
        
        # Validate user exists
        if str(created_by_user_id) not in users:
            return json.dumps({"error": f"User {created_by_user_id} not found"})
        
        # Find groups created by the user
        user_groups = []
        for group in groups.values():
            if group.get("created_by_user_id") == created_by_user_id:
                user_groups.append(group)
        
        return json.dumps(user_groups)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_groups_by_creator",
                "description": "Get all groups created by a specific user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "created_by_user_id": {"type": "string", "description": "ID of the user to get groups for"}
                    },
                    "required": ["created_by_user_id"]
                }
            }
        }
EOF

# Create get_space_permissions_by_space.py
cat > get_space_permissions_by_space.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetSpacePermissionsBySpace(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], space_id: str) -> str:
        
        space_permissions = data.get("space_permissions", {})
        spaces = data.get("spaces", {})
        
        # Validate space exists
        if str(space_id) not in spaces:
            return json.dumps({"error": f"Space {space_id} not found"})
        
        # Find permissions for the space
        space_permission_records = []
        for permission in space_permissions.values():
            if permission.get("space_id") == space_id:
                space_permission_records.append(permission)
        
        return json.dumps(space_permission_records)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_space_permissions_by_space",
                "description": "Get all space permission records for a specific space",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "space_id": {"type": "string", "description": "ID of the space to get permissions for"}
                    },
                    "required": ["space_id"]
                }
            }
        }
EOF

# Create get_page_permissions_by_page.py
cat > get_page_permissions_by_page.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetPagePermissionsByPage(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], page_id: str) -> str:
        
        page_permissions = data.get("page_permissions", {})
        pages = data.get("pages", {})
        
        # Validate page exists
        if str(page_id) not in pages:
            return json.dumps({"error": f"Page {page_id} not found"})
        
        # Find permissions for the page
        page_permission_records = []
        for permission in page_permissions.values():
            if permission.get("page_id") == page_id:
                page_permission_records.append(permission)
        
        return json.dumps(page_permission_records)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_page_permissions_by_page",
                "description": "Get all page permission records for a specific page",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "page_id": {"type": "string", "description": "ID of the page to get permissions for"}
                    },
                    "required": ["page_id"]
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
        spaces = data.get("spaces", {})
        pages = data.get("pages", {})
        
        # Validate space if provided
        if space_id and str(space_id) not in spaces:
            return json.dumps({"error": f"Space {space_id} not found"})
        
        # Find broken links
        broken_links = []
        
        for link in page_links.values():
            # Check if link is marked as broken
            if link.get("is_broken", False):
                # If space_id is specified, filter by space
                if space_id:
                    source_page_id = link.get("source_page_id")
                    if str(source_page_id) in pages:
                        source_page = pages[str(source_page_id)]
                        if source_page.get("space_id") == space_id:
                            broken_links.append(link)
                else:
                    broken_links.append(link)
        
        return json.dumps(broken_links)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "find_broken_links",
                "description": "Find all broken links, optionally filtered by space",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "space_id": {"type": "string", "description": "ID of the space to filter broken links (optional)"}
                    },
                    "required": []
                }
            }
        }
EOF


echo "All tool files have been created successfully!"
echo "Files created:"
echo "- get_comment_by_id.py"
echo "- get_comments_by_page.py"
echo "- get_comments_by_user.py"
echo "- get_comments_by_parent.py"
echo "- get_comments_by_status.py"
echo "- get_attachment_by_id.py"
echo "- get_attachments_by_page.py"
echo "- get_attachments_by_comment.py"
echo "- get_attachments_by_uploader.py"
echo "- get_group_by_id.py"
echo "- get_groups_by_type.py"
echo "- get_groups_by_creator.py"
echo "- get_space_permissions_by_space.py"
echo "- get_page_permissions_by_page.py"
echo "- find_broken_links.py"