#!/bin/bash

# Create get_user_by_id.py
cat > get_user_by_id.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetUserById(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: str) -> str:
        users = data.get("users", {})
        
        # Validate user exists
        if str(user_id) not in users:
            return json.dumps({"error": f"User {user_id} not found"})
        
        user = users[str(user_id)]
        return json.dumps(user)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_user_by_id",
                "description": "Get a user record by user ID",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "ID of the user to retrieve"}
                    },
                    "required": ["user_id"]
                }
            }
        }
EOF

# Create get_user_by_username.py
cat > get_user_by_username.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetUserByUsername(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], username: str) -> str:
        users = data.get("users", {})
        
        # Find user by username
        for user_id, user in users.items():
            if user.get("username") == username:
                return json.dumps(user)
        
        return json.dumps({"error": f"User with username '{username}' not found"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_user_by_username",
                "description": "Get a user record by username",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "username": {"type": "string", "description": "Username of the user to retrieve"}
                    },
                    "required": ["username"]
                }
            }
        }
EOF

# Create get_user_by_email.py
cat > get_user_by_email.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetUserByEmail(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], email: str) -> str:
        users = data.get("users", {})
        
        # Find user by email
        for user_id, user in users.items():
            if user.get("email") == email:
                return json.dumps(user)
        
        return json.dumps({"error": f"User with email '{email}' not found"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_user_by_email",
                "description": "Get a user record by email address",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "email": {"type": "string", "description": "Email address of the user to retrieve"}
                    },
                    "required": ["email"]
                }
            }
        }
EOF

# Create get_users_by_role.py
cat > get_users_by_role.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetUsersByRole(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], role: str) -> str:
        users = data.get("users", {})
        
        # Validate role
        valid_roles = ["PlatformOwner", "WikiProgramManager", "User"]
        if role not in valid_roles:
            return json.dumps({"error": f"Invalid role. Must be one of {valid_roles}"})
        
        # Find users by role
        matching_users = []
        for user_id, user in users.items():
            if user.get("role") == role:
                matching_users.append(user)
        
        return json.dumps(matching_users)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_users_by_role",
                "description": "Get all users with a specific role",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "role": {"type": "string", "description": "Role to filter by (PlatformOwner, WikiProgramManager, User)"}
                    },
                    "required": ["role"]
                }
            }
        }
EOF

# Create get_users_by_status.py
cat > get_users_by_status.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetUsersByStatus(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], status: str) -> str:
        users = data.get("users", {})
        
        # Validate status
        valid_statuses = ["active", "inactive", "suspended"]
        if status not in valid_statuses:
            return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}"})
        
        # Find users by status
        matching_users = []
        for user_id, user in users.items():
            if user.get("status") == status:
                matching_users.append(user)
        
        return json.dumps(matching_users)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_users_by_status",
                "description": "Get all users with a specific status",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string", "description": "Status to filter by (active, inactive, suspended)"}
                    },
                    "required": ["status"]
                }
            }
        }
EOF

# Create get_space_by_id.py
cat > get_space_by_id.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetSpaceById(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], space_id: str) -> str:
        spaces = data.get("spaces", {})
        
        # Validate space exists
        if str(space_id) not in spaces:
            return json.dumps({"error": f"Space {space_id} not found"})
        
        space = spaces[str(space_id)]
        return json.dumps(space)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_space_by_id",
                "description": "Get a space record by space ID",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "space_id": {"type": "string", "description": "ID of the space to retrieve"}
                    },
                    "required": ["space_id"]
                }
            }
        }
EOF

# Create get_space_by_key.py
cat > get_space_by_key.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetSpaceByKey(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], space_key: str) -> str:
        spaces = data.get("spaces", {})
        
        # Find space by key
        for space_id, space in spaces.items():
            if space.get("space_key") == space_key:
                return json.dumps(space)
        
        return json.dumps({"error": f"Space with key '{space_key}' not found"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_space_by_key",
                "description": "Get a space record by space key",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "space_key": {"type": "string", "description": "Key of the space to retrieve"}
                    },
                    "required": ["space_key"]
                }
            }
        }
EOF

# Create get_spaces_by_type.py
cat > get_spaces_by_type.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetSpacesByType(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], type: str) -> str:
        spaces = data.get("spaces", {})
        
        # Validate type
        valid_types = ["global", "personal", "private"]
        if type not in valid_types:
            return json.dumps({"error": f"Invalid type. Must be one of {valid_types}"})
        
        # Find spaces by type
        matching_spaces = []
        for space_id, space in spaces.items():
            if space.get("type") == type:
                matching_spaces.append(space)
        
        return json.dumps(matching_spaces)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_spaces_by_type",
                "description": "Get all spaces with a specific type",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "type": {"type": "string", "description": "Type to filter by (global, personal, private)"}
                    },
                    "required": ["type"]
                }
            }
        }
EOF

# Create get_spaces_by_creator.py
cat > get_spaces_by_creator.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetSpacesByCreator(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], created_by_user_id: str) -> str:
        spaces = data.get("spaces", {})
        users = data.get("users", {})
        
        # Validate user exists
        if str(created_by_user_id) not in users:
            return json.dumps({"error": f"User {created_by_user_id} not found"})
        
        # Find spaces created by user
        matching_spaces = []
        for space_id, space in spaces.items():
            if space.get("created_by_user_id") == created_by_user_id:
                matching_spaces.append(space)
        
        return json.dumps(matching_spaces)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_spaces_by_creator",
                "description": "Get all spaces created by a specific user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "created_by_user_id": {"type": "string", "description": "ID of the user who created the spaces"}
                    },
                    "required": ["created_by_user_id"]
                }
            }
        }
EOF

# Create get_spaces_by_status.py
cat > get_spaces_by_status.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetSpacesByStatus(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], status: str) -> str:
        spaces = data.get("spaces", {})
        
        # Validate status
        valid_statuses = ["current", "archived"]
        if status not in valid_statuses:
            return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}"})
        
        # Find spaces by status
        matching_spaces = []
        for space_id, space in spaces.items():
            if space.get("status") == status:
                matching_spaces.append(space)
        
        return json.dumps(matching_spaces)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_spaces_by_status",
                "description": "Get all spaces with a specific status",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string", "description": "Status to filter by (current, archived)"}
                    },
                    "required": ["status"]
                }
            }
        }
EOF

echo "All tool files have been created successfully!"
echo "Files created:"
echo "- get_user_by_id.py"
echo "- get_user_by_username.py"
echo "- get_user_by_email.py"
echo "- get_users_by_role.py"
echo "- get_users_by_status.py"
echo "- get_space_by_id.py"
echo "- get_space_by_key.py"
echo "- get_spaces_by_type.py"
echo "- get_spaces_by_creator.py"
echo "- get_spaces_by_status.py"