import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ManageLocationOperations(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], operation_type: str, location_id: str = None, 
               location_name: str = None, address: str = None, city_name: str = None, 
               country: str = None, status: str = None) -> str:
        """
        Manage location operations for HR talent management system.
        
        Operations:
        - create_location: Create new location (requires location_name, address, city_name, country)
        - update_location: Update existing location (requires location_id and field changes)
        - deactivate_location: Deactivate location (requires location_id)
        """
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        if operation_type not in ["create_location", "update_location", "deactivate_location"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid operation_type '{operation_type}'. Must be 'create_location', 'update_location', or 'deactivate_location'"
            })
        
        # Access locations data
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for locations"
            })
        
        locations = data.get("locations", {})
        
        if operation_type == "create_location":
            # Validate required fields for creation
            if not location_name:
                return json.dumps({
                    "success": False,
                    "error": "location_name is required for create_location operation"
                })
            if not address:
                return json.dumps({
                    "success": False,
                    "error": "address is required for create_location operation"
                })
            if not city_name:
                return json.dumps({
                    "success": False,
                    "error": "city_name is required for create_location operation"
                })
            if not country:
                return json.dumps({
                    "success": False,
                    "error": "country is required for create_location operation"
                })
            
            # Validate status enum if provided, otherwise default to active
            if status:
                valid_statuses = ["active", "inactive"]
                if status not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                    })
            else:
                status = "active"  # Default to active if not provided
            
            # Check for duplicate location name
            location_name_clean = location_name.strip()
            for existing_location in locations.values():
                if existing_location.get("location_name", "").strip().lower() == location_name_clean.lower():
                    return json.dumps({
                        "success": False,
                        "error": f"Location with name '{location_name_clean}' already exists"
                    })
            
            # Check for duplicate address
            address_clean = address.strip()
            for existing_location in locations.values():
                if existing_location.get("address", "").strip().lower() == address_clean.lower():
                    return json.dumps({
                        "success": False,
                        "error": f"Location with address '{address_clean}' already exists"
                    })
            
            # Generate new location ID
            new_location_id = generate_id(locations)
            
            # Create new location record
            new_location = {
                "location_id": str(new_location_id),
                "location_name": location_name,
                "address": address,
                "city_name": city_name,
                "country": country,
                "status": status,
                "created_at": "2025-10-10T12:00:00"
            }
            
            locations[str(new_location_id)] = new_location
            
            return json.dumps({
                "success": True,
                "operation_type": "create_location",
                "location_id": str(new_location_id),
                "message": f"Location {new_location_id} created successfully with name '{location_name_clean}'",
                "location_data": new_location
            })
        
        elif operation_type == "update_location":
            if not location_id:
                return json.dumps({
                    "success": False,
                    "error": "location_id is required for update_location operation"
                })
            
            if location_id not in locations:
                return json.dumps({
                    "success": False,
                    "error": f"Location {location_id} not found"
                })
            
            # Check if at least one field is provided for update
            update_fields = [location_name, address, city_name, country, status]
            if not any(field is not None for field in update_fields):
                return json.dumps({
                    "success": False,
                    "error": "At least one field must be provided for update_location operation"
                })
            
            # Validate status enum if provided
            if status is not None:
                valid_statuses = ["active", "inactive"]
                if status not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                    })
            
            # Check for duplicate location name if updating name
            if location_name is not None:
                new_location_name = location_name.strip()
                for existing_location_id, existing_location in locations.items():
                    if (existing_location_id != location_id and 
                        existing_location.get("location_name", "").strip().lower() == new_location_name.lower()):
                        return json.dumps({
                            "success": False,
                            "error": f"Location with name '{new_location_name}' already exists"
                        })
            
            # Check for duplicate address if updating address
            if address is not None:
                new_address = address.strip()
                for existing_location_id, existing_location in locations.items():
                    if (existing_location_id != location_id and 
                        existing_location.get("address", "").strip().lower() == new_address.lower()):
                        return json.dumps({
                            "success": False,
                            "error": f"Location with address '{new_address}' already exists"
                        })
            
            # Update location record
            current_location = locations[location_id]
            updated_location = current_location.copy()
            
            if location_name is not None:
                updated_location["location_name"] = location_name
            if address is not None:
                updated_location["address"] = address
            if city_name is not None:
                updated_location["city_name"] = city_name
            if country is not None:
                updated_location["country"] = country
            if status is not None:
                updated_location["status"] = status
            
            locations[location_id] = updated_location
            
            return json.dumps({
                "success": True,
                "operation_type": "update_location",
                "location_id": str(location_id),
                "message": f"Location {location_id} updated successfully",
                "location_data": updated_location
            })
        
        elif operation_type == "deactivate_location":
            if not location_id:
                return json.dumps({
                    "success": False,
                    "error": "location_id is required for deactivate_location operation"
                })
            
            if location_id not in locations:
                return json.dumps({
                    "success": False,
                    "error": f"Location {location_id} not found"
                })
            
            # Update location status to inactive
            current_location = locations[location_id]
            if current_location.get("status") == "inactive":
                return json.dumps({
                    "success": False,
                    "error": f"Location {location_id} is already inactive"
                })
            
            updated_location = current_location.copy()
            updated_location["status"] = "inactive"
            locations[location_id] = updated_location
            
            return json.dumps({
                "success": True,
                "operation_type": "deactivate_location",
                "location_id": str(location_id),
                "message": f"Location {location_id} deactivated successfully",
                "location_data": updated_location
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manage_location_operations",
                "description": "Manage location operations in the HR talent management system. This tool handles location data management including creation of new office locations, updates to existing location information, and location deactivation. For creation, establishes new location records with comprehensive validation to ensure data integrity and prevent duplicates. For updates, modifies existing location records while maintaining referential integrity. For deactivation, safely transitions locations to inactive status. Validates location names, addresses, and enforces uniqueness constraints. Essential for location administration, payroll jurisdiction management, and maintaining accurate location records for organizational structure and compliance reporting.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation_type": {
                            "type": "string",
                            "description": "Type of operation to perform: 'create_location' to create new location, 'update_location' to modify existing location information, 'deactivate_location' to deactivate location",
                            "enum": ["create_location", "update_location", "deactivate_location"]
                        },
                        "location_name": {
                            "type": "string",
                            "description": "Name of the location (required for create_location, optional for update_location, must be unique)"
                        },
                        "address": {
                            "type": "string",
                            "description": "Full address of the location (required for create_location, optional for update_location, must be unique)"
                        },
                        "city_name": {
                            "type": "string",
                            "description": "City name where location is situated (required for create_location, optional for update_location)"
                        },
                        "country": {
                            "type": "string",
                            "description": "Country where location is situated (required for create_location, optional for update_location)"
                        },
                        "status": {
                            "type": "string",
                            "description": "Location status (optional for both create and update, defaults to active)",
                            "enum": ["active", "inactive"]
                        },
                        "location_id": {
                            "type": "string",
                            "description": "Unique identifier of the location (required for update_location and deactivate_location operations)"
                        }
                    },
                    "required": ["operation_type"]
                }
            }
        }
