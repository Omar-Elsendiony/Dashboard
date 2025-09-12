import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetUserGroups(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: Optional[str] = None, 
               group_id: Optional[str] = None) -> str:
        
        groups = data.get("groups", {})
        user_groups = data.get("user_groups", {})
        users = data.get("users", {})
        
        result = []
        
        # If group_id is specified, return info for that specific group
        if group_id:
            if str(group_id) not in groups:
                return json.dumps({"error": "Group not found"})
            
            group = groups[str(group_id)]
            group_info = {
                "group_id": group.get("group_id"),
                "name": group.get("name"),
                "description": group.get("description"),
                "type": group.get("type"),
                "created_at": group.get("created_at"),
                "created_by_user_id": group.get("created_by_user_id"),
                "members": []
            }
            
            # Get all members of this group
            for ug in user_groups.values():
                if ug.get("group_id") == group_id:
                    member_user_id = ug.get("user_id")
                    if str(member_user_id) in users:
                        user = users[str(member_user_id)]
                        member_info = {
                            "user_id": user.get("user_id"),
                            "username": user.get("username"),
                            "display_name": user.get("display_name"),
                            "role": user.get("role"),
                            "added_at": ug.get("added_at"),
                            "added_by_user_id": ug.get("added_by_user_id")
                        }
                        group_info["members"].append(member_info)
            
            result.append(group_info)
        
        # If user_id is specified, return groups that user belongs to
        elif user_id:
            if str(user_id) not in users:
                return json.dumps({"error": "User not found"})
            
            user_group_ids = []
            for ug in user_groups.values():
                if ug.get("user_id") == user_id:
                    user_group_ids.append(ug.get("group_id"))
            
            for gid in user_group_ids:
                if str(gid) in groups:
                    group = groups[str(gid)]
                    group_info = {
                        "group_id": group.get("group_id"),
                        "name": group.get("name"),
                        "description": group.get("description"),
                        "type": group.get("type"),
                        "created_at": group.get("created_at"),
                        "created_by_user_id": group.get("created_by_user_id")
                    }
                    
                    # Add membership info for this user
                    for ug in user_groups.values():
                        if ug.get("user_id") == user_id and ug.get("group_id") == gid:
                            group_info["added_at"] = ug.get("added_at")
                            group_info["added_by_user_id"] = ug.get("added_by_user_id")
                            break
                    
                    result.append(group_info)
        
        # If no specific filters, return all groups with their members
        else:
            for group in groups.values():
                group_info = {
                    "group_id": group.get("group_id"),
                    "name": group.get("name"),
                    "description": group.get("description"),
                    "type": group.get("type"),
                    "created_at": group.get("created_at"),
                    "created_by_user_id": group.get("created_by_user_id"),
                    "members": []
                }
                
                # Get all members of this group
                for ug in user_groups.values():
                    if ug.get("group_id") == group.get("group_id"):
                        member_user_id = ug.get("user_id")
                        if str(member_user_id) in users:
                            user = users[str(member_user_id)]
                            member_info = {
                                "user_id": user.get("user_id"),
                                "username": user.get("username"),
                                "display_name": user.get("display_name"),
                                "role": user.get("role"),
                                "added_at": ug.get("added_at"),
                                "added_by_user_id": ug.get("added_by_user_id")
                            }
                            group_info["members"].append(member_info)
                
                result.append(group_info)
        
        # Note: space_id parameter is included for future extension if needed
        # Currently groups are not space-specific based on the schema provided
        
        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_user_groups",
                "description": "Get information about groups and their members. Can filter by user, group, or return all groups.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "Filter by user ID to get groups that user belongs to"},
                        "group_id": {"type": "string", "description": "Filter by group ID to get specific group info with members"}                    },
                    "required": []
                }
            }
        }