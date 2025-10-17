import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class ManageAssets(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        action: str,
        entity_type: str,
        entity_data: Optional[Dict[str, Any]] = None,
        entity_id: Optional[str] = None
    ) -> str:
        """
        Create or update product and configuration item records.
        
        Actions:
        - create: Create new product or configuration item record (requires entity_data)
        - update: Update existing product or configuration item record (requires entity_id and entity_data)
        """
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        timestamp = "2025-10-01T00:00:00"
        
        if action not in ["create", "update"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid action '{action}'. Must be 'create' or 'update'"
            })
        
        if entity_type not in ["products", "configuration_items"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'products' or 'configuration_items'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format"
            })
        
        # ========== PRODUCTS ==========
        if entity_type == "products":
            products = data.get("products", {})
            
            if action == "create":
                if not entity_data:
                    return json.dumps({
                        "success": False,
                        "error": "entity_data is required for create action"
                    })
                
                # Validate required fields
                required_fields = ["product_name"]
                missing_fields = [field for field in required_fields if field not in entity_data]
                if missing_fields:
                    return json.dumps({
                        "success": False,
                        "error": f"Missing required fields: {', '.join(missing_fields)}"
                    })
                
                # Validate allowed fields
                allowed_fields = ["product_name", "product_code", "description", "status"]
                invalid_fields = [field for field in entity_data.keys() if field not in allowed_fields]
                if invalid_fields:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid fields: {', '.join(invalid_fields)}"
                    })
                
                # Validate status enum
                if "status" in entity_data:
                    valid_status = ["active", "deprecated", "retired"]
                    if entity_data["status"] not in valid_status:
                        return json.dumps({
                            "success": False,
                            "error": f"Invalid status '{entity_data['status']}'. Must be one of: {', '.join(valid_status)}"
                        })
                
                # Check product_code uniqueness if provided
                if "product_code" in entity_data and entity_data["product_code"]:
                    for product in products.values():
                        if product.get("product_code") == entity_data["product_code"]:
                            return json.dumps({
                                "success": False,
                                "error": "Product code already exists"
                            })
                
                # Create new product
                new_id = str(generate_id(products))
                new_product = {
                    "product_id": new_id,
                    "product_name": entity_data["product_name"],
                    "product_code": entity_data.get("product_code"),
                    "description": entity_data.get("description"),
                    "status": entity_data.get("status", "active"),
                    "created_at": timestamp
                }
                products[new_id] = new_product
                
                return json.dumps({
                    "success": True,
                    "action": "create",
                    "entity_type": "products",
                    "product_id": new_id,
                    "product_data": new_product
                })
            
            elif action == "update":
                if not entity_id:
                    return json.dumps({
                        "success": False,
                        "error": "entity_id is required for update action"
                    })
                
                if entity_id not in products:
                    return json.dumps({
                        "success": False,
                        "error": f"Product {entity_id} not found"
                    })
                
                if not entity_data:
                    return json.dumps({
                        "success": False,
                        "error": "entity_data is required for update action"
                    })
                
                # Validate allowed fields
                allowed_fields = ["product_name", "product_code", "description", "status"]
                invalid_fields = [field for field in entity_data.keys() if field not in allowed_fields]
                if invalid_fields:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid fields: {', '.join(invalid_fields)}"
                    })
                
                # Validate status enum if provided
                if "status" in entity_data:
                    valid_status = ["active", "deprecated", "retired"]
                    if entity_data["status"] not in valid_status:
                        return json.dumps({
                            "success": False,
                            "error": f"Invalid status. Must be one of: {', '.join(valid_status)}"
                        })
                
                # Check product_code uniqueness if being updated
                if "product_code" in entity_data and entity_data["product_code"]:
                    for pid, product in products.items():
                        if pid != entity_id and product.get("product_code") == entity_data["product_code"]:
                            return json.dumps({
                                "success": False,
                                "error": "New product_code already exists"
                            })
                
                # Update product
                updated_product = products[entity_id].copy()
                for key, value in entity_data.items():
                    updated_product[key] = value
                products[entity_id] = updated_product
                
                return json.dumps({
                    "success": True,
                    "action": "update",
                    "entity_type": "products",
                    "product_id": entity_id,
                    "product_data": updated_product
                })
        
        # ========== CONFIGURATION ITEMS ==========
        elif entity_type == "configuration_items":
            configuration_items = data.get("configuration_items", {})
            products = data.get("products", {})
            
            if action == "create":
                if not entity_data:
                    return json.dumps({
                        "success": False,
                        "error": "entity_data is required for create action"
                    })
                
                # Validate required fields
                required_fields = ["ci_name", "product_id", "ci_type", "environment"]
                missing_fields = [field for field in required_fields if field not in entity_data]
                if missing_fields:
                    return json.dumps({
                        "success": False,
                        "error": f"Missing required fields: {', '.join(missing_fields)}"
                    })
                
                # Validate allowed fields
                allowed_fields = ["ci_name", "product_id", "ci_type", "environment", "location", "operational_status"]
                invalid_fields = [field for field in entity_data.keys() if field not in allowed_fields]
                if invalid_fields:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid fields: {', '.join(invalid_fields)}"
                    })
                
                # Validate ci_type enum
                valid_ci_types = ["server", "application", "database", "network", "storage", "service"]
                if entity_data["ci_type"] not in valid_ci_types:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid ci_type '{entity_data['ci_type']}'. Must be one of: {', '.join(valid_ci_types)}"
                    })
                
                # Validate environment enum
                valid_environments = ["production", "staging", "development", "testing"]
                if entity_data["environment"] not in valid_environments:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid environment '{entity_data['environment']}'. Must be one of: {', '.join(valid_environments)}"
                    })
                
                # Validate operational_status enum if provided
                if "operational_status" in entity_data:
                    valid_operational_status = ["operational", "degraded", "down", "maintenance"]
                    if entity_data["operational_status"] not in valid_operational_status:
                        return json.dumps({
                            "success": False,
                            "error": f"Invalid operational_status '{entity_data['operational_status']}'. Must be one of: {', '.join(valid_operational_status)}"
                        })
                
                # Validate product_id exists
                if entity_data["product_id"] not in products:
                    return json.dumps({
                        "success": False,
                        "error": "Product not found"
                    })
                
                # Check ci_name uniqueness per product
                for ci in configuration_items.values():
                    if ci.get("ci_name") == entity_data["ci_name"] and ci.get("product_id") == entity_data["product_id"]:
                        return json.dumps({
                            "success": False,
                            "error": "CI name already exists for this product"
                        })
                
                # Create new configuration item
                new_id = str(generate_id(configuration_items))
                new_ci = {
                    "ci_id": new_id,
                    "ci_name": entity_data["ci_name"],
                    "product_id": entity_data["product_id"],
                    "ci_type": entity_data["ci_type"],
                    "environment": entity_data["environment"],
                    "location": entity_data.get("location"),
                    "operational_status": entity_data.get("operational_status", "operational"),
                    "created_at": timestamp,
                    "updated_at": timestamp
                }
                configuration_items[new_id] = new_ci
                
                return json.dumps({
                    "success": True,
                    "action": "create",
                    "entity_type": "configuration_items",
                    "ci_id": new_id,
                    "ci_data": new_ci
                })
            
            elif action == "update":
                if not entity_id:
                    return json.dumps({
                        "success": False,
                        "error": "entity_id is required for update action"
                    })
                
                if entity_id not in configuration_items:
                    return json.dumps({
                        "success": False,
                        "error": f"Configuration item {entity_id} not found"
                    })
                
                if not entity_data:
                    return json.dumps({
                        "success": False,
                        "error": "entity_data is required for update action"
                    })
                
                # Validate allowed fields
                allowed_fields = ["ci_name", "product_id", "ci_type", "environment", "location", "operational_status"]
                invalid_fields = [field for field in entity_data.keys() if field not in allowed_fields]
                if invalid_fields:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid fields: {', '.join(invalid_fields)}"
                    })
                
                # Validate ci_type enum if provided
                if "ci_type" in entity_data:
                    valid_ci_types = ["server", "application", "database", "network", "storage", "service"]
                    if entity_data["ci_type"] not in valid_ci_types:
                        return json.dumps({
                            "success": False,
                            "error": f"Invalid ci_type. Must be one of: {', '.join(valid_ci_types)}"
                        })
                
                # Validate environment enum if provided
                if "environment" in entity_data:
                    valid_environments = ["production", "staging", "development", "testing"]
                    if entity_data["environment"] not in valid_environments:
                        return json.dumps({
                            "success": False,
                            "error": f"Invalid environment. Must be one of: {', '.join(valid_environments)}"
                        })
                
                # Validate operational_status enum if provided
                if "operational_status" in entity_data:
                    valid_operational_status = ["operational", "degraded", "down", "maintenance"]
                    if entity_data["operational_status"] not in valid_operational_status:
                        return json.dumps({
                            "success": False,
                            "error": f"Invalid operational_status. Must be one of: {', '.join(valid_operational_status)}"
                        })
                
                # Validate product_id if being updated
                if "product_id" in entity_data:
                    if entity_data["product_id"] not in products:
                        return json.dumps({
                            "success": False,
                            "error": "Product not found"
                        })
                
                # Check ci_name uniqueness per product if being updated
                current_ci = configuration_items[entity_id]
                new_ci_name = entity_data.get("ci_name", current_ci.get("ci_name"))
                new_product_id = entity_data.get("product_id", current_ci.get("product_id"))
                
                if "ci_name" in entity_data or "product_id" in entity_data:
                    for cid, ci in configuration_items.items():
                        if cid != entity_id and ci.get("ci_name") == new_ci_name and ci.get("product_id") == new_product_id:
                            return json.dumps({
                                "success": False,
                                "error": "New CI name already exists for this product"
                            })
                
                # Update configuration item
                updated_ci = configuration_items[entity_id].copy()
                for key, value in entity_data.items():
                    updated_ci[key] = value
                updated_ci["updated_at"] = timestamp
                configuration_items[entity_id] = updated_ci
                
                return json.dumps({
                    "success": True,
                    "action": "update",
                    "entity_type": "configuration_items",
                    "ci_id": entity_id,
                    "ci_data": updated_ci
                })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manage_assets",
                "description": "Create or update product and configuration item records in the incident management system. For creation, establishes new product or configuration item records with comprehensive validation. For updates, modifies existing records while maintaining data integrity. Validates product codes, CI types, environments, and operational status values according to system requirements.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' to establish new record, 'update' to modify existing record",
                            "enum": ["create", "update"]
                        },
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to manage: 'products' or 'configuration_items'",
                            "enum": ["products", "configuration_items"]
                        },
                        "entity_data": {
                            "type": "object",
                            "description": "Entity data object. For products create: requires product_name, with optional product_code (must be unique), description, status ('active', 'deprecated', 'retired'). For configuration_items create: requires ci_name, product_id, ci_type ('server', 'application', 'database', 'network', 'storage', 'service'), environment ('production', 'staging', 'development', 'testing'), with optional location, operational_status ('operational', 'degraded', 'down', 'maintenance'). For update: includes fields to change. SYNTAX: {\"key\": \"value\"}"
                        },
                        "entity_id": {
                            "type": "string",
                            "description": "Unique identifier of the entity record (product_id for products, ci_id for configuration_items). Required for update action only."
                        }
                    },
                    "required": ["action", "entity_type"]
                }
            }
        }
