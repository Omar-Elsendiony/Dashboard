import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class SetGroupMemberships(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, user_id: str, group_id: str) -> str:
        """
        Add or remove users from groups.
        
        Actions:
        - add: Add user to group
        - remove: Remove user from group
        """

        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1

        if action not in ["add", "remove"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid action '{action}'. Must be 'add' or 'remove'"
            })

        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format"
            })

        user_groups = data.get("user_groups", {})
        users = data.get("users", {})
        groups = data.get("groups", {})

        # Validate user and group exist
        if user_id not in users:
            return json.dumps({
                "success": False,
                "error": f"User {user_id} not found"
            })

        if group_id not in groups:
            return json.dumps({
                "success": False,
                "error": f"Group {group_id} not found"
            })

        # Create a composite key for user_groups
        membership_key = f"{user_id}_{group_id}"

        if action == "add":
            # Check if membership already exists
            for ug_id, membership in user_groups.items():
                if membership.get("user_id") == user_id and membership.get("group_id") == group_id:
                    return json.dumps({
                        "success": False,
                        "error": f"User {user_id} is already a member of group {group_id}"
                    })

            timestamp = "2025-10-01T12:00:00"

            # Generate new ID
            new_id = generate_id(user_groups)

            new_membership = {
                "_id": str(new_id),
                "user_id": user_id,
                "group_id": group_id,
                "joined_at": timestamp
            }

            user_groups[str(new_id)] = new_membership

            return json.dumps({
                "success": True,
                "action": "add",
                "message": f"User {user_id} added to group {group_id} successfully",
                "membership_id": str(new_id),
                "membership_data": new_membership
            })
        
        elif action == "remove":
            # Find and remove the membership
            membership_to_remove = None
            key_to_remove = None

            for ug_id, membership in user_groups.items():
                if membership.get("user_id") == user_id and membership.get("group_id") == group_id:
                    membership_to_remove = membership.copy()
                    key_to_remove = ug_id
                    break
            
            if not membership_to_remove:
                return json.dumps({
                    "success": False,
                    "error": f"User {user_id} is not a member of group {group_id}"
                })
            
            del user_groups[key_to_remove]

            return json.dumps({
                "success": True,
                "action": "remove",
                "message": f"User {user_id} removed from group {group_id} successfully",
                "membership_id": key_to_remove,
                "membership_data": membership_to_remove
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "set_group_memberships",
                "description": "Add or remove users from groups in the Confluence system. This tool manages group membership by adding users to groups for collective permission assignment and notification distribution, or removing users from groups when their access needs change. Validates that both user and group exist before creating or removing memberships. Prevents duplicate memberships and ensures clean removal of existing memberships. Essential for organizing users into teams, managing group-based permissions, and facilitating collaborative workflows.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'add' to add user to group, 'remove' to remove user from group",
                            "enum": ["add", "remove"]
                        },
                        "user_id": {
                            "type": "string",
                            "description": "Unique identifier of the user (required)"
                        },
                        "group_id": {
                            "type": "string",
                            "description": "Unique identifier of the group (required)"
                        }
                    },
                    "required": ["action", "user_id", "group_id"]
                }
            }
        }
