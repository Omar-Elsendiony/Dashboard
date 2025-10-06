import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class CreateVendors(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, vendor_data: Dict[str, Any] = None, vendor_id: str = None) -> str:
        """
        Create or update vendor records.

        Actions:
        - create: Create new vendor (requires vendor_data with vendor_name, vendor_type)
        - update: Update existing vendor (requires vendor_id and vendor_data with fields to change)
        """
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1

        if action not in ["create", "update"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid action '{action}'. Must be 'create' or 'update'"
            })

        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for vendors"
            })

        vendors = data.get("vendors", {})

        valid_vendor_types = ["cloud_provider", "payment_processor", "software_vendor", "infrastructure_provider", "security_vendor"]
        valid_statuses = ["active", "inactive", "suspended"]

        if action == "create":
            if not vendor_data:
                return json.dumps({
                    "success": False,
                    "error": "vendor_data is required for create action"
                })

            # Required fields
            required_fields = ["vendor_name", "vendor_type"]
            missing = [f for f in required_fields if f not in vendor_data or not vendor_data.get(f)]
            if missing:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields for vendor creation: {', '.join(missing)}"
                })

            vendor_name = vendor_data["vendor_name"]
            vendor_type = vendor_data["vendor_type"]
            contact_email = vendor_data.get("contact_email")
            contact_phone = vendor_data.get("contact_phone")
            status = vendor_data.get("status", "active")

            # Validate vendor_type
            if vendor_type not in valid_vendor_types:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid vendor_type. Must be one of: {', '.join(valid_vendor_types)}"
                })

            # Validate status
            if status not in valid_statuses:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                })

            # Check uniqueness of vendor_name
            for existing_vendor in vendors.values():
                if existing_vendor.get("vendor_name") == vendor_name:
                    return json.dumps({
                        "success": False,
                        "error": f"Vendor name '{vendor_name}' already exists"
                    })

            # Create vendor
            new_id = generate_id(vendors)
            new_vendor = {
                "vendor_id": str(new_id),
                "vendor_name": vendor_name,
                "vendor_type": vendor_type,
                "status": status,
                "created_at": "2025-10-04T12:00:00"
            }

            if contact_email:
                new_vendor["contact_email"] = contact_email
            if contact_phone:
                new_vendor["contact_phone"] = contact_phone

            vendors[str(new_id)] = new_vendor

            return json.dumps({
                "success": True,
                "action": "create",
                "vendor_id": str(new_id),
                "message": f"Vendor {new_id} created successfully",
                "vendor_data": new_vendor
            })

        elif action == "update":
            if not vendor_id:
                return json.dumps({
                    "success": False,
                    "error": "vendor_id is required for update action"
                })

            if vendor_id not in vendors:
                return json.dumps({
                    "success": False,
                    "error": f"Vendor {vendor_id} not found"
                })

            if not vendor_data:
                return json.dumps({
                    "success": False,
                    "error": "vendor_data is required for update action"
                })

            current_vendor = vendors[vendor_id].copy()

            # Validate and update vendor_type
            if "vendor_type" in vendor_data:
                vt = vendor_data["vendor_type"]
                if vt not in valid_vendor_types:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid vendor_type. Must be one of: {', '.join(valid_vendor_types)}"
                    })
                current_vendor["vendor_type"] = vt

            # Validate and update status
            if "status" in vendor_data:
                st = vendor_data["status"]
                if st not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                    })
                current_vendor["status"] = st

            # Check uniqueness of vendor_name if updating
            if "vendor_name" in vendor_data:
                new_name = vendor_data["vendor_name"]
                for vid, existing_vendor in vendors.items():
                    if vid != vendor_id and existing_vendor.get("vendor_name") == new_name:
                        return json.dumps({
                            "success": False,
                            "error": f"Vendor name '{new_name}' already exists"
                        })
                current_vendor["vendor_name"] = new_name

            # Update other fields
            for field in ["contact_email", "contact_phone"]:
                if field in vendor_data:
                    current_vendor[field] = vendor_data[field]

            vendors[vendor_id] = current_vendor

            return json.dumps({
                "success": True,
                "action": "update",
                "vendor_id": vendor_id,
                "message": f"Vendor {vendor_id} updated successfully",
                "vendor_data": current_vendor
            })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_vendors",
                "description": "Create or update vendor records in the incident management system. Validates uniqueness of vendor names. Supports cloud providers, payment processors, software vendors, infrastructure providers, and security vendors.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' or 'update'",
                            "enum": ["create", "update"]
                        },
                        "vendor_data": {
                            "type": "object",
                            "description": "Vendor data object. For create: requires vendor_name, vendor_type. For update: include fields to modify. SYNTAX: {\"key\": \"value\"}",
                            "properties": {
                                "vendor_name": {"type": "string", "description": "Name of the vendor (required for create)"},
                                "vendor_type": {
                                    "type": "string",
                                    "description": "Type of vendor (required for create)",
                                    "enum": ["cloud_provider", "payment_processor", "software_vendor", "infrastructure_provider", "security_vendor"]
                                },
                                "contact_email": {"type": "string", "description": "Contact email (optional)"},
                                "contact_phone": {"type": "string", "description": "Contact phone (optional)"},
                                "status": {
                                    "type": "string",
                                    "description": "Vendor status (optional)",
                                    "enum": ["active", "inactive", "suspended"]
                                }
                            }
                        },
                        "vendor_id": {"type": "string", "description": "Unique identifier of the vendor (required for update action only)"}
                    },
                    "required": ["action"]
                }
            }
        }