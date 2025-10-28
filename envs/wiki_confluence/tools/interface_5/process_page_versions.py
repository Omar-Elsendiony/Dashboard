import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class ProcessPageVersions(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, page_id: str,
               editor_user_id: str, content_snapshot: Optional[str] = None,
               version_number: Optional[int] = None) -> str:
        """
        Create or restore page versions.
        
        Actions:
        - create: Create new version (requires page_id, editor_user_id, content_snapshot)
        - restore: Restore specific version (requires page_id, version_number, editor_user_id)
        """
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        if action not in ["create", "restore"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid action '{action}'. Must be 'create' or 'restore'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format"
            })
        
        pages = data.get("pages", {})
        page_versions = data.get("page_versions", {})
        users = data.get("users", {})
        
        # Validate page exists
        if page_id not in pages:
            return json.dumps({
                "success": False,
                "error": f"Page {page_id} not found"
            })
        
        # Validate user exists
        if editor_user_id not in users:
            return json.dumps({
                "success": False,
                "error": f"User {editor_user_id} not found"
            })
        
        if action == "create":
            if not content_snapshot:
                return json.dumps({
                    "success": False,
                    "error": "content_snapshot is required for create action"
                })
            
            # Get current version number from page
            current_page = pages[page_id]

            existing_versions_for_page = [
                v.get("version_number", 0)
                for v in page_versions.values()
                if isinstance(v, dict) and v.get("page_id") == page_id
            ]

          
            if existing_versions_for_page:

                new_version_number = max(existing_versions_for_page) + 1
            else:

                page_current_version = current_page.get("current_version", 1)
                new_version_number = page_current_version
            
            # Generate new version ID
            new_version_id = generate_id(page_versions)
            timestamp = "2025-10-01T12:00:00"
            
            new_version = {
                "version_id": str(new_version_id),
                "page_id": page_id,
                "version_number": new_version_number,
                "editor_user_id": editor_user_id,
                "edited_at": timestamp,
                "content_snapshot": content_snapshot
            }
            
            page_versions[str(new_version_id)] = new_version
            
            # Update page's current version
            pages[page_id]["current_version"] = new_version_number
            
            return json.dumps({
                "success": True,
                "action": "create",
                "version_id": str(new_version_id),
                "version_number": new_version_number,
                "message": f"Version {new_version_number} created for page {page_id}",
                "version_data": new_version
            })
        
        elif action == "restore":
            if version_number is None:
                return json.dumps({
                    "success": False,
                    "error": "version_number is required for restore action"
                })
            
            # Find the version to restore
            version_to_restore = None
            for version_id, version_data in page_versions.items():
                if (version_data.get("page_id") == page_id and 
                    version_data.get("version_number") == version_number):
                    version_to_restore = version_data
                    break
            
            if not version_to_restore:
                return json.dumps({
                    "success": False,
                    "error": f"Version {version_number} not found for page {page_id}"
                })
            
            # Create a new version with the restored content
            current_page = pages[page_id]
            
            # Determine next version just like in create path
            existing_versions_for_page = [
                v.get("version_number", 0)
                for v in page_versions.values()
                if isinstance(v, dict) and v.get("page_id") == page_id
            ]
            if existing_versions_for_page:
                new_version_number = max(existing_versions_for_page) + 1
            else:
                new_version_number = current_page.get("current_version", 1) + 1
            # Determine next version just like in create path
            new_version_id = generate_id(page_versions)
            timestamp = "2025-10-01T12:00:00"
            
            restored_version = {
                "version_id": str(new_version_id),
                "page_id": page_id,
                "version_number": new_version_number,
                "editor_user_id": editor_user_id,
                "edited_at": timestamp,
                "content_snapshot": version_to_restore.get("content_snapshot")
            }
            
            page_versions[str(new_version_id)] = restored_version
            
            # Update page's current version
            pages[page_id]["current_version"] = new_version_number
            
            return json.dumps({
                "success": True,
                "action": "restore",
                "version_id": str(new_version_id),
                "restored_from_version": version_number,
                "new_version_number": new_version_number,
                "message": f"Version {version_number} restored as version {new_version_number} for page {page_id}",
                "version_data": restored_version
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "process_page_versions",
                "description": "Create or restore page versions in the Confluence system. This tool manages page version history by creating new version snapshots when content is updated or restoring previous versions to become the current version. Version creation captures content snapshots with editor attribution and timestamps. Version restoration creates a new version with content from a previous version, maintaining complete version history. Essential for content versioning, change tracking, audit trails, and content recovery.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' to save new version, 'restore' to revert to previous version",
                            "enum": ["create", "restore"]
                        },
                        "page_id": {
                            "type": "string",
                            "description": "Unique identifier of the page (required)"
                        },
                        "editor_user_id": {
                            "type": "string",
                            "description": "User ID of the editor creating or restoring the version (required)"
                        },
                        "content_snapshot": {
                            "type": "string",
                            "description": "Content snapshot for the new version (required for create action)"
                        },
                        "version_number": {
                            "type": "integer",
                            "description": "Version number to restore (required for restore action)"
                        }
                    },
                    "required": ["action", "page_id", "editor_user_id"]
                }
            }
        }
