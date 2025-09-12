#!/bin/bash

# Create get_page_by_id.py
cat > get_page_by_id.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetPageById(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], page_id: str) -> str:
        
        pages = data.get("pages", {})
        
        # Validate page exists
        if str(page_id) not in pages:
            return json.dumps({"error": f"Page {page_id} not found"})
        
        page = pages[str(page_id)]
        
        return json.dumps(page)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_page_by_id",
                "description": "Get a single page record by ID",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "page_id": {"type": "string", "description": "ID of the page to retrieve"}
                    },
                    "required": ["page_id"]
                }
            }
        }
EOF

# Create get_pages_by_space.py
cat > get_pages_by_space.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetPagesBySpace(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], space_id: str) -> str:
        
        pages = data.get("pages", {})
        spaces = data.get("spaces", {})
        
        # Validate space exists
        if str(space_id) not in spaces:
            return json.dumps({"error": f"Space {space_id} not found"})
        
        # Find all pages in the space
        space_pages = []
        for page in pages.values():
            if page.get("space_id") == space_id:
                space_pages.append(page)
        
        return json.dumps(space_pages)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_pages_by_space",
                "description": "Get all pages in a specific space",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "space_id": {"type": "string", "description": "ID of the space"}
                    },
                    "required": ["space_id"]
                }
            }
        }
EOF

# Create get_pages_by_parent.py
cat > get_pages_by_parent.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetPagesByParent(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], parent_page_id: str) -> str:
        
        pages = data.get("pages", {})
        
        # Validate parent page exists
        if str(parent_page_id) not in pages:
            return json.dumps({"error": f"Parent page {parent_page_id} not found"})
        
        # Find all child pages
        child_pages = []
        for page in pages.values():
            if page.get("parent_page_id") == parent_page_id:
                child_pages.append(page)
        
        return json.dumps(child_pages)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_pages_by_parent",
                "description": "Get all child pages of a parent page",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "parent_page_id": {"type": "string", "description": "ID of the parent page"}
                    },
                    "required": ["parent_page_id"]
                }
            }
        }
EOF

# Create get_pages_by_creator.py
cat > get_pages_by_creator.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetPagesByCreator(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], created_by_user_id: str) -> str:
        
        pages = data.get("pages", {})
        users = data.get("users", {})
        
        # Validate user exists
        if str(created_by_user_id) not in users:
            return json.dumps({"error": f"User {created_by_user_id} not found"})
        
        # Find all pages created by the user
        user_pages = []
        for page in pages.values():
            if page.get("created_by_user_id") == created_by_user_id:
                user_pages.append(page)
        
        return json.dumps(user_pages)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_pages_by_creator",
                "description": "Get all pages created by a specific user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "created_by_user_id": {"type": "string", "description": "ID of the user who created the pages"}
                    },
                    "required": ["created_by_user_id"]
                }
            }
        }
EOF

# Create get_pages_by_status.py
cat > get_pages_by_status.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetPagesByStatus(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], status: str) -> str:
        
        pages = data.get("pages", {})
        
        # Validate status
        valid_statuses = ["current", "draft", "deleted", "historical"]
        if status not in valid_statuses:
            return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}"})
        
        # Find all pages with the specified status
        status_pages = []
        for page in pages.values():
            if page.get("status") == status:
                status_pages.append(page)
        
        return json.dumps(status_pages)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_pages_by_status",
                "description": "Get all pages with a specific status",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string", "description": "Page status (current, draft, deleted, historical)"}
                    },
                    "required": ["status"]
                }
            }
        }
EOF

# Create get_pages_by_template.py
cat > get_pages_by_template.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetPagesByTemplate(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], template_id: str) -> str:
        
        pages = data.get("pages", {})
        templates = data.get("page_templates", {})
        
        # Validate template exists
        if str(template_id) not in templates:
            return json.dumps({"error": f"Template {template_id} not found"})
        
        # Find all pages using the template
        template_pages = []
        for page in pages.values():
            if page.get("template_id") == template_id:
                template_pages.append(page)
        
        return json.dumps(template_pages)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_pages_by_template",
                "description": "Get all pages using a specific template",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "template_id": {"type": "string", "description": "ID of the template"}
                    },
                    "required": ["template_id"]
                }
            }
        }
EOF

# Create get_page_version_by_id.py
cat > get_page_version_by_id.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetPageVersionById(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], page_version_id: str) -> str:
        
        page_versions = data.get("page_versions", {})
        
        # Validate page version exists
        if str(page_version_id) not in page_versions:
            return json.dumps({"error": f"Page version {page_version_id} not found"})
        
        page_version = page_versions[str(page_version_id)]
        
        return json.dumps(page_version)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_page_version_by_id",
                "description": "Get a single page version record by ID",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "page_version_id": {"type": "string", "description": "ID of the page version to retrieve"}
                    },
                    "required": ["page_version_id"]
                }
            }
        }
EOF

# Create get_page_versions_by_page.py
cat > get_page_versions_by_page.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetPageVersionsByPage(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], page_id: str) -> str:
        
        page_versions = data.get("page_versions", {})
        pages = data.get("pages", {})
        
        # Validate page exists
        if str(page_id) not in pages:
            return json.dumps({"error": f"Page {page_id} not found"})
        
        # Find all versions for the page
        page_version_list = []
        for version in page_versions.values():
            if version.get("page_id") == page_id:
                page_version_list.append(version)
        
        return json.dumps(page_version_list)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_page_versions_by_page",
                "description": "Get all versions for a specific page",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "page_id": {"type": "string", "description": "ID of the page"}
                    },
                    "required": ["page_id"]
                }
            }
        }
EOF

# Create get_page_versions_by_creator.py
cat > get_page_versions_by_creator.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetPageVersionsByCreator(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], created_by_user_id: str) -> str:
        
        page_versions = data.get("page_versions", {})
        users = data.get("users", {})
        
        # Validate user exists
        if str(created_by_user_id) not in users:
            return json.dumps({"error": f"User {created_by_user_id} not found"})
        
        # Find all page versions created by the user
        user_versions = []
        for version in page_versions.values():
            if version.get("created_by_user_id") == created_by_user_id:
                user_versions.append(version)
        
        return json.dumps(user_versions)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_page_versions_by_creator",
                "description": "Get all page versions created by a specific user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "created_by_user_id": {"type": "string", "description": "ID of the user who created the versions"}
                    },
                    "required": ["created_by_user_id"]
                }
            }
        }
EOF

# Create get_template_by_id.py
cat > get_template_by_id.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetTemplateById(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], template_id: str) -> str:
        
        templates = data.get("page_templates", {})
        
        # Validate template exists
        if str(template_id) not in templates:
            return json.dumps({"error": f"Template {template_id} not found"})
        
        template = templates[str(template_id)]
        
        return json.dumps(template)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_template_by_id",
                "description": "Get a single template record by ID",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "template_id": {"type": "string", "description": "ID of the template to retrieve"}
                    },
                    "required": ["template_id"]
                }
            }
        }
EOF

# Create get_templates_by_space.py
cat > get_templates_by_space.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetTemplatesBySpace(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], space_id: str) -> str:
        
        templates = data.get("page_templates", {})
        spaces = data.get("spaces", {})
        
        # Validate space exists
        if str(space_id) not in spaces:
            return json.dumps({"error": f"Space {space_id} not found"})
        
        # Find all templates in the space
        space_templates = []
        for template in templates.values():
            if template.get("space_id") == space_id:
                space_templates.append(template)
        
        return json.dumps(space_templates)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_templates_by_space",
                "description": "Get all templates in a specific space",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "space_id": {"type": "string", "description": "ID of the space"}
                    },
                    "required": ["space_id"]
                }
            }
        }
EOF

# Create get_templates_by_creator.py
cat > get_templates_by_creator.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetTemplatesByCreator(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], created_by_user_id: str) -> str:
        
        templates = data.get("page_templates", {})
        users = data.get("users", {})
        
        # Validate user exists
        if str(created_by_user_id) not in users:
            return json.dumps({"error": f"User {created_by_user_id} not found"})
        
        # Find all templates created by the user
        user_templates = []
        for template in templates.values():
            if template.get("created_by_user_id") == created_by_user_id:
                user_templates.append(template)
        
        return json.dumps(user_templates)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_templates_by_creator",
                "description": "Get all templates created by a specific user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "created_by_user_id": {"type": "string", "description": "ID of the user who created the templates"}
                    },
                    "required": ["created_by_user_id"]
                }
            }
        }
EOF

# Create get_global_templates.py
cat > get_global_templates.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetGlobalTemplates(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any]) -> str:
        
        templates = data.get("page_templates", {})
        
        # Find all global templates
        global_templates = []
        for template in templates.values():
            if template.get("is_global") is True:
                global_templates.append(template)
        
        return json.dumps(global_templates)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_global_templates",
                "description": "Get all global templates",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            }
        }
EOF

echo "All database tools have been created successfully!"
echo "Generated files:"
echo "- get_page_by_id.py"
echo "- get_pages_by_space.py"
echo "- get_pages_by_parent.py"
echo "- get_pages_by_creator.py"
echo "- get_pages_by_status.py"
echo "- get_pages_by_template.py"
echo "- get_page_version_by_id.py"
echo "- get_page_versions_by_page.py"
echo "- get_page_versions_by_creator.py"
echo "- get_template_by_id.py"
echo "- get_templates_by_space.py"
echo "- get_templates_by_creator.py"
echo "- get_global_templates.py"