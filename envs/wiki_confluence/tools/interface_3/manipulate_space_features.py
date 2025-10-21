import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ManipulateSpaceFeatures(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], space_id: str, feature_type: str, is_enabled: bool) -> str:
        """
        Enable or disable specific features for a space.
        """
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format"
            })
        
        spaces = data.get("spaces", {})
        space_features = data.get("space_features", {})
        
        # Validate space exists
        if space_id not in spaces:
            return json.dumps({
                "success": False,
                "error": f"Space {space_id} not found"
            })
        
        # Validate feature_type enum
        valid_features = ["live_docs", "calendars", "whiteboard", "databases", 
                         "smart_links", "folders", "blogs"]
        if feature_type not in valid_features:
            return json.dumps({
                "success": False,
                "error": f"Invalid feature_type. Must be one of: {', '.join(valid_features)}"
            })
        
        # Check if feature already exists
        existing_feature_id = None
        for feature_id, feature in space_features.items():
            if feature.get("space_id") == space_id and feature.get("feature_type") == feature_type:
                existing_feature_id = feature_id
                break
        
        if existing_feature_id:
            # Update existing feature
            space_features[existing_feature_id]["is_enabled"] = is_enabled
            
            return json.dumps({
                "success": True,
                "action": "update",
                "feature_id": existing_feature_id,
                "message": f"Feature '{feature_type}' for space {space_id} {'enabled' if is_enabled else 'disabled'}",
                "feature_data": space_features[existing_feature_id]
            })
        else:
            # Create new feature record
            new_feature_id = generate_id(space_features)
            
            new_feature = {
                "feature_id": str(new_feature_id),
                "space_id": space_id,
                "feature_type": feature_type,
                "is_enabled": is_enabled
            }
            
            space_features[str(new_feature_id)] = new_feature
            
            return json.dumps({
                "success": True,
                "action": "create",
                "feature_id": str(new_feature_id),
                "message": f"Feature '{feature_type}' created for space {space_id} and {'enabled' if is_enabled else 'disabled'}",
                "feature_data": new_feature
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manipulate_space_features",
                "description": "Enable or disable specific features for a space in the Confluence system. This tool manages space-level feature configuration by enabling or disabling capabilities such as live documents, calendars, whiteboards, databases, smart links, folders, and blogs. Creates new feature records when configuring a feature for the first time, or updates existing feature settings. Essential for customizing space functionality, controlling available tools, and tailoring workspace capabilities to team needs.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "space_id": {
                            "type": "string",
                            "description": "Unique identifier of the space (required)"
                        },
                        "feature_type": {
                            "type": "string",
                            "description": "Type of feature to configure (required)",
                            "enum": ["live_docs", "calendars", "whiteboard", "databases", "smart_links", "folders", "blogs"]
                        },
                        "is_enabled": {
                            "type": "boolean",
                            "description": "Enable (true) or disable (false) the feature (required)"
                        }
                    },
                    "required": ["space_id", "feature_type", "is_enabled"]
                }
            }
        }
