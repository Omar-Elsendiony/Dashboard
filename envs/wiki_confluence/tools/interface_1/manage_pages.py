import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class ManagePages(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, page_id: Optional[str] = None,
               space_id: Optional[str] = None, title: Optional[str] = None,
               content_format: Optional[str] = None, created_by_user_id: Optional[str] = None,
               updated_by_user_id: Optional[str] = None, parent_page_id: Optional[str] = None,
               updates: Optional[Dict[str, Any]] = None, mode: Optional[str] = None) -> str:
        """
        Create, update, delete, publish, or unpublish pages.
        
        Actions:
        - create: Create new page (requires space_id, title, content_format, created_by_user_id)
        - update: Update existing page (requires page_id, updated_by_user_id, and updates dict)
        - publish: Publish a draft page (requires page_id, updated_by_user_id)
        - unpublish: Unpublish a published page (requires page_id, updated_by_user_id)
        - delete: Delete page (requires page_id and mode: 'soft_delete' or 'hard_delete')
        - restore: Restore soft-deleted page (requires page_id)
        """
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        valid_actions = ["create", "update", "publish", "unpublish", "delete", "restore"]
        if action not in valid_actions:
            return json.dumps({
                "success": False,
                "error": f"Invalid action '{action}'. Must be one of: {', '.join(valid_actions)}"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format"
            })
        
        pages = data.get("pages", {})
        spaces = data.get("spaces", {})
        users = data.get("users", {})
        
        if action == "create":
            # Validate required fields
            if not space_id:
                return json.dumps({
                    "success": False,
                    "error": "space_id is required for create action"
                })
            
            if not title or not title.strip():
                return json.dumps({
                    "success": False,
                    "error": "title is required and cannot be empty"
                })
            
            if not content_format:
                return json.dumps({
                    "success": False,
                    "error": "content_format is required"
                })
            
            if not created_by_user_id:
                return json.dumps({
                    "success": False,
                    "error": "created_by_user_id is required"
                })
            
            # Validate space exists
            if space_id not in spaces:
                return json.dumps({
                    "success": False,
                    "error": f"Space {space_id} not found"
                })
            
            # Validate user exists
            if created_by_user_id not in users:
                return json.dumps({
                    "success": False,
                    "error": f"User {created_by_user_id} not found"
                })
            
            # Validate content_format enum
            valid_formats = ["markdown", "html", "richtext"]
            if content_format not in valid_formats:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid content_format. Must be one of: {', '.join(valid_formats)}"
                })
            
            # Validate parent page if provided
            if parent_page_id and parent_page_id not in pages:
                return json.dumps({
                    "success": False,
                    "error": f"Parent page {parent_page_id} not found"
                })
            
            # Generate new page ID
            new_page_id = generate_id(pages)
            timestamp = "2025-10-01T12:00:00"
            
            new_page = {
                "page_id": str(new_page_id),
                "space_id": space_id,
                "parent_page_id": parent_page_id,
                "title": title,
                "content_format": content_format,
                "current_version": 1,
                "state": "draft",
                "created_by_user_id": created_by_user_id,
                "updated_by_user_id": None,
                "created_at": timestamp,
                "updated_at": None,
                "is_trashed": False,
                "is_published": False
            }
            
            pages[str(new_page_id)] = new_page
            
            return json.dumps({
                "success": True,
                "action": "create",
                "page_id": str(new_page_id),
                "message": f"Page created successfully with title '{title}'",
                "page_data": new_page
            })
        
        elif action == "update":
            if not page_id:
                return json.dumps({
                    "success": False,
                    "error": "page_id is required for update action"
                })
            
            if page_id not in pages:
                return json.dumps({
                    "success": False,
                    "error": f"Page {page_id} not found"
                })
            
            if not updated_by_user_id:
                return json.dumps({
                    "success": False,
                    "error": "updated_by_user_id is required for update action"
                })
            
            if updated_by_user_id not in users:
                return json.dumps({
                    "success": False,
                    "error": f"User {updated_by_user_id} not found"
                })
            
            if not updates:
                return json.dumps({
                    "success": False,
                    "error": "updates dict is required for update action"
                })
            
            # Validate allowed update fields
            allowed_fields = ["title", "parent_page_id", "space_id", "content_format"]
            invalid_fields = [field for field in updates.keys() if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for page update: {', '.join(invalid_fields)}"
                })
            
            # Validate parent page if updating
            if "parent_page_id" in updates and updates["parent_page_id"]:
                if updates["parent_page_id"] not in pages:
                    return json.dumps({
                        "success": False,
                        "error": f"Parent page {updates['parent_page_id']} not found"
                    })
            
            # Validate space if updating
            if "space_id" in updates and updates["space_id"] not in spaces:
                return json.dumps({
                    "success": False,
                    "error": f"Space {updates['space_id']} not found"
                })
            
            # Validate content format if updating
            if "content_format" in updates:
                valid_formats = ["markdown", "html", "richtext"]
                if updates["content_format"] not in valid_formats:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid content_format. Must be one of: {', '.join(valid_formats)}"
                    })
            
            # Update page record
            timestamp = "2025-10-01T12:00:00"
            updated_page = pages[page_id].copy()
            for key, value in updates.items():
                updated_page[key] = value
            updated_page["updated_by_user_id"] = updated_by_user_id
            updated_page["updated_at"] = timestamp
            updated_page["current_version"] = updated_page.get("current_version", 1) + 1
            
            pages[page_id] = updated_page
            
            return json.dumps({
                "success": True,
                "action": "update",
                "page_id": page_id,
                "message": f"Page {page_id} updated successfully",
                "page_data": updated_page
            })
        
        elif action == "publish":
            if not page_id:
                return json.dumps({
                    "success": False,
                    "error": "page_id is required for publish action"
                })
            
            if page_id not in pages:
                return json.dumps({
                    "success": False,
                    "error": f"Page {page_id} not found"
                })
            
            if not updated_by_user_id:
                return json.dumps({
                    "success": False,
                    "error": "updated_by_user_id is required for publish action"
                })
            
            current_page = pages[page_id]
            if current_page.get("state") != "draft":
                return json.dumps({
                    "success": False,
                    "error": f"Page {page_id} is not in draft state. Current state: {current_page.get('state')}"
                })
            
            timestamp = "2025-10-01T12:00:00"
            published_page = current_page.copy()
            published_page["state"] = "published"
            published_page["is_published"] = True
            published_page["updated_by_user_id"] = updated_by_user_id
            published_page["updated_at"] = timestamp
            
            pages[page_id] = published_page
            
            return json.dumps({
                "success": True,
                "action": "publish",
                "page_id": page_id,
                "message": f"Page {page_id} published successfully",
                "page_data": published_page
            })
        
        elif action == "unpublish":
            if not page_id:
                return json.dumps({
                    "success": False,
                    "error": "page_id is required for unpublish action"
                })
            
            if page_id not in pages:
                return json.dumps({
                    "success": False,
                    "error": f"Page {page_id} not found"
                })
            
            if not updated_by_user_id:
                return json.dumps({
                    "success": False,
                    "error": "updated_by_user_id is required for unpublish action"
                })
            
            current_page = pages[page_id]
            if current_page.get("state") != "published":
                return json.dumps({
                    "success": False,
                    "error": f"Page {page_id} is not published. Current state: {current_page.get('state')}"
                })
            
            timestamp = "2025-10-01T12:00:00"
            unpublished_page = current_page.copy()
            unpublished_page["state"] = "draft"
            unpublished_page["is_published"] = False
            unpublished_page["updated_by_user_id"] = updated_by_user_id
            unpublished_page["updated_at"] = timestamp
            
            pages[page_id] = unpublished_page
            
            return json.dumps({
                "success": True,
                "action": "unpublish",
                "page_id": page_id,
                "message": f"Page {page_id} unpublished successfully",
                "page_data": unpublished_page
            })
        
        elif action == "delete":
            if not page_id:
                return json.dumps({
                    "success": False,
                    "error": "page_id is required for delete action"
                })
            
            if page_id not in pages:
                return json.dumps({
                    "success": False,
                    "error": f"Page {page_id} not found"
                })
            
            if not mode:
                return json.dumps({
                    "success": False,
                    "error": "mode is required for delete action"
                })
            
            if mode not in ["soft_delete", "hard_delete"]:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid mode '{mode}'. Must be 'soft_delete' or 'hard_delete'"
                })
            
            if mode == "soft_delete":
                # Soft delete: mark as trashed
                deleted_page = pages[page_id].copy()
                deleted_page["is_trashed"] = True
                pages[page_id] = deleted_page
                
                return json.dumps({
                    "success": True,
                    "action": "delete",
                    "mode": "soft_delete",
                    "page_id": page_id,
                    "message": f"Page {page_id} moved to trash successfully",
                    "page_data": deleted_page
                })
            else:
                # Hard delete: remove from database
                deleted_page = pages[page_id].copy()
                del pages[page_id]
                
                return json.dumps({
                    "success": True,
                    "action": "delete",
                    "mode": "hard_delete",
                    "page_id": page_id,
                    "message": f"Page {page_id} permanently deleted",
                    "page_data": deleted_page
                })
        
        elif action == "restore":
            if not page_id:
                return json.dumps({
                    "success": False,
                    "error": "page_id is required for restore action"
                })
            
            if page_id not in pages:
                return json.dumps({
                    "success": False,
                    "error": f"Page {page_id} not found"
                })
            
            current_page = pages[page_id]
            if not current_page.get("is_trashed", False):
                return json.dumps({
                    "success": False,
                    "error": f"Page {page_id} is not in trash"
                })
            
            restored_page = current_page.copy()
            restored_page["is_trashed"] = False
            pages[page_id] = restored_page
            
            return json.dumps({
                "success": True,
                "action": "restore",
                "page_id": page_id,
                "message": f"Page {page_id} restored successfully",
                "page_data": restored_page
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manage_pages",
                "description": "Create, update, delete, publish, unpublish, or restore pages in the Confluence system. This tool manages the complete page lifecycle including creation of new content pages within spaces, updates to existing page properties, state transitions between draft and published states, soft and hard deletion, and restoration from trash. Validates parent page relationships, space membership, user permissions, and content format specifications. Essential for content management, collaborative documentation, and knowledge base administration.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create', 'update', 'publish', 'unpublish', 'delete', or 'restore'",
                            "enum": ["create", "update", "publish", "unpublish", "delete", "restore"]
                        },
                        "page_id": {
                            "type": "string",
                            "description": "Unique identifier of the page (required for update, publish, unpublish, delete, and restore actions)"
                        },
                        "space_id": {
                            "type": "string",
                            "description": "Unique identifier of the space (required for create action)"
                        },
                        "title": {
                            "type": "string",
                            "description": "Page title (required for create action)"
                        },
                        "content_format": {
                            "type": "string",
                            "description": "Content format (required for create action)",
                            "enum": ["markdown", "html", "richtext"]
                        },
                        "created_by_user_id": {
                            "type": "string",
                            "description": "User ID of page creator (required for create action)"
                        },
                        "updated_by_user_id": {
                            "type": "string",
                            "description": "User ID performing the update (required for update, publish, and unpublish actions)"
                        },
                        "parent_page_id": {
                            "type": "string",
                            "description": "ID of parent page for hierarchical organization (optional for create)"
                        },
                        "updates": {
                            "type": "object",
                            "description": "Dictionary of fields to update for update action. Valid fields: title, parent_page_id, space_id, content_format. SYNTAX: {\"key\": \"value\"}",
                            "properties": {
                                "title": {
                                    "type": "string",
                                    "description": "Updated page title"
                                },
                                "parent_page_id": {
                                    "type": "string",
                                    "description": "Updated parent page ID"
                                },
                                "space_id": {
                                    "type": "string",
                                    "description": "Move page to different space"
                                },
                                "content_format": {
                                    "type": "string",
                                    "description": "Updated content format",
                                    "enum": ["markdown", "html", "richtext"]
                                }
                            }
                        },
                        "mode": {
                            "type": "string",
                            "description": "Deletion mode for delete action: 'soft_delete' (recoverable) or 'hard_delete' (permanent)",
                            "enum": ["soft_delete", "hard_delete"]
                        }
                    },
                    "required": ["action"]
                }
            }
        }
