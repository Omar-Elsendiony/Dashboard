import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class SetGroups(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, group_name: Optional[str] = None,
               group_id: Optional[str] = None, updates: Optional[Dict[str, Any]] = None) -> str:
        """
        Create, update, or delete groups.
        
        Actions:
        - create: Create new group (requires group_name)
        - update: Update existing group (requires group_id and updates dict)
        - delete: Delete group (requires group_id)
        """
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        if action not in ["create", "update", "delete"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid action '{action}'. Must be 'create', 'update', or 'delete'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format"
            })
        
        groups = data.get("groups", {})
        
        if action == "create":
            # Validate required fields
            if not group_name or not group_name.strip():
                return json.dumps({
                    "success": False,
                    "error": "Group name is required and cannot be empty"
                })
            
            # Check for duplicate group name
            for existing_group in groups.values():
                if existing_group.get("group_name") == group_name:
                    return json.dumps({
                        "success": False,
                        "error": f"Group with name '{group_name}' already exists"
                    })
            
            # Generate new group ID
            new_group_id = generate_id(groups)
            timestamp = "2025-10-01T12:00:00"
            
            new_group = {
                "group_id": str(new_group_id),
                "group_name": group_name,
                "created_at": timestamp
            }
            
            groups[str(new_group_id)] = new_group
            
            return json.dumps({
                "success": True,
                "action": "create",
                "group_id": str(new_group_id),
                "message": f"Group created successfully with name '{group_name}'",
                "group_data": new_group
            })
        
        elif action == "update":
            if not group_id:
                return json.dumps({
                    "success": False,
                    "error": "group_id is required for update action"
                })
            
            if group_id not in groups:
                return json.dumps({
                    "success": False,
                    "error": f"Group {group_id} not found"
                })
            
            if not updates:
                return json.dumps({
                    "success": False,
                    "error": "updates dict is required for update action"
                })
            
            # Validate allowed update fields
            allowed_fields = ["group_name"]
            invalid_fields = [field for field in updates.keys() if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for group update: {', '.join(invalid_fields)}"
                })
            
            # Check for duplicate group name if updating name
            if "group_name" in updates:
                new_name = updates["group_name"]
                for existing_group_id, existing_group in groups.items():
                    if existing_group_id != group_id and existing_group.get("group_name") == new_name:
                        return json.dumps({
                            "success": False,
                            "error": f"Group with name '{new_name}' already exists"
                        })
            
            # Update group record
            updated_group = groups[group_id].copy()
            for key, value in updates.items():
                updated_group[key] = value
            
            groups[group_id] = updated_group
            
            return json.dumps({
                "success": True,
                "action": "update",
                "group_id": group_id,
                "message": f"Group {group_id} updated successfully",
                "group_data": updated_group
            })
        
        elif action == "delete":
            if not group_id:
                return json.dumps({
                    "success": False,
                    "error": "group_id is required for delete action"
                })
            
            if group_id not in groups:
                return json.dumps({
                    "success": False,
                    "error": f"Group {group_id} not found"
                })
            
            deleted_group = groups[group_id].copy()
            del groups[group_id]
            
            return json.dumps({
                "success": True,
                "action": "delete",
                "group_id": group_id,
                "message": f"Group {group_id} deleted successfully",
                "group_data": deleted_group
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "set_groups",
                "description": "Create, update, or delete groups in the Confluence system. This tool manages the complete group lifecycle including creation of new user groups, updates to existing group configurations, and group deletion. Groups are used for permission and notification management, enabling efficient access control and communication with multiple users. Validates group name uniqueness and maintains data integrity across all operations. Essential for organizing users, managing permissions at scale, and facilitating team-based collaboration.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' to establish new group, 'update' to modify existing group, 'delete' to remove group",
                            "enum": ["create", "update", "delete"]
                        },
                        "group_name": {
                            "type": "string",
                            "description": "Group name (required for create, must be unique across all groups)"
                        },
                        "group_id": {
                            "type": "string",
                            "description": "Unique identifier of the group (required for update and delete actions)"
                        },
                        "updates": {
                            "type": "object",
                            "description": "Dictionary of fields to update for update action. Valid fields: group_name. SYNTAX: {\"key\": \"value\"}",
                            "properties": {
                                "group_name": {
                                    "type": "string",
                                    "description": "Updated group name (must be unique)"
                                }
                            }
                        }
                    },
                    "required": ["action"]
                }
            }
        }
