import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class ManipulateAttachments(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        action: str,
        attachment_data: Optional[Dict[str, Any]] = None,
        attachment_id: Optional[str] = None # Although attachments are typically immutable, including for consistency if a delete action were added later.
    ) -> str:
        """
        Create new attachment records.

        Actions:
        - create: Create a new attachment record (requires attachment_data)
        """

        def generate_id(table: Dict[str, Any], prefix: str) -> str:
            if not table:
                return 1
            return str(max(int(k) for k in table.keys()) + 1)

        timestamp = "2025-10-07T12:00:00"

        if action not in ["create"]: # Attachments are typically created and then immutable, not updated.
            return json.dumps({
                "success": False,
                "error": f"Invalid action '{action}'. Must be 'create'"
            })

        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format"
            })

        attachments = data.get("attachments", {})
        users = data.get("users", {})
        
        # Tables that can be referenced by attachments
        reference_tables = {
            "incident": data.get("incidents", {}),
            "change": data.get("change_requests", {}),
            "rca": data.get("root_cause_analyses", {}),
            "report": data.get("incident_reports", {}),
            "pir": data.get("post_incident_reviews", {}),
            "communication": data.get("communications", {}),
            "work_order": data.get("work_orders", {}),
            "problem": data.get("problem_tickets", {})
        }

        # Define valid enums based on DBML schema
        valid_reference_types = [
            "incident", "change", "rca", "report", "pir", "communication", "work_order", "problem"
        ]

        if action == "create":
            if not attachment_data:
                return json.dumps({
                    "success": False,
                    "error": "attachment_data is required for create action"
                })

            # Validate required fields as per DBML
            required_fields = [
                "reference_id", "reference_type", "file_name", "file_url",
                "file_type", "file_size_bytes", "uploaded_by"
            ]
            missing_fields = [field for field in required_fields if field not in attachment_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields: {', '.join(missing_fields)}"
                })
            
            # Validate non-empty required fields
            for field in required_fields:
                if (isinstance(attachment_data[field], str) and str(attachment_data[field]).strip() == "") or attachment_data[field] is None:
                    return json.dumps({
                        "success": False,
                        "error": f"Field '{field}' cannot be empty or null"
                    })

            # Validate reference_type enum
            reference_type = attachment_data["reference_type"]
            if reference_type not in valid_reference_types:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid reference_type '{reference_type}'. Must be one of: {', '.join(valid_reference_types)}"
                })

            # Validate uploaded_by FK
            uploaded_by = str(attachment_data["uploaded_by"]).strip().strip('"')
            if uploaded_by not in users:
                return json.dumps({
                    "success": False,
                    "error": f"Uploaded by user '{uploaded_by}' not found"
                })
            if users[uploaded_by]["status"] != "active":
                return json.dumps({
                    "success": False,
                    "error": f"Uploaded by user '{uploaded_by}' is not active"
                })

            # Validate reference_id FK based on reference_type
            reference_id = str(attachment_data["reference_id"]).strip().strip('"')
            target_table = reference_tables.get(reference_type)
            if not target_table:
                return json.dumps({
                    "success": False,
                    "error": f"Reference type '{reference_type}' does not map to a known table for validation."
                })
            if reference_id not in target_table:
                return json.dumps({
                    "success": False,
                    "error": f"Reference ID '{reference_id}' not found in '{reference_type}' table."
                })
            
            # Validate file_size_bytes is a positive integer
            file_size_bytes = attachment_data["file_size_bytes"]
            if not isinstance(file_size_bytes, int) or file_size_bytes < 0:
                return json.dumps({
                    "success": False,
                    "error": f"file_size_bytes must be a non-negative integer."
                })

            new_id = generate_id(attachments, "ATT")
            new_attachment = {
                "attachment_id": new_id,
                "reference_id": reference_id,
                "reference_type": reference_type,
                "file_name": attachment_data["file_name"],
                "file_url": attachment_data["file_url"],
                "file_type": attachment_data["file_type"],
                "file_size_bytes": file_size_bytes,
                "uploaded_by": uploaded_by,
                "uploaded_at": timestamp
            }
            attachments[new_id] = new_attachment
            return json.dumps({
                "success": True,
                "action": "create",
                "attachment_id": new_id,
                "attachment_data": new_attachment
            })
        
        # No 'update' action for attachments as per schema (no updated_at field, implies immutability)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manipulate_attachments",
                "description": "Create new attachment records in the system. Attachments are associated with various record types like incidents, changes, or problem tickets.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' to add a new attachment."
                        },
                        "attachment_data": {
                            "type": "object",
                            "description": "Data object containing fields for creating an attachment.",
                            "properties": {
                                "reference_id": {
                                    "type": "string",
                                    "description": "The ID of the record this attachment belongs to (e.g., incident_id, change_id). Required for create, cannot be empty. Must refer to an existing record of the specified reference_type."
                                },
                                "reference_type": {
                                    "type": "string",
                                    "description": "The type of record this attachment is linked to (e.g., incident, change, rca). Required for create. Must be one of: incident, change, rca, report, pir, communication, work_order, problem.",
                                    "enum": ["incident", "change", "rca", "report", "pir", "communication", "work_order", "problem"]
                                },
                                "file_name": {
                                    "type": "string",
                                    "description": "The name of the attached file (e.g., 'screenshot.png'). Required for create, cannot be empty."
                                },
                                "file_url": {
                                    "type": "string",
                                    "description": "The URL or path where the file is stored (e.g., 'https://storage.example.com/files/abc.png'). Required for create, cannot be empty."
                                },
                                "file_type": {
                                    "type": "string",
                                    "description": "The MIME type or extension of the file (e.g., 'image/png', 'application/pdf'). Required for create, cannot be empty."
                                },
                                "file_size_bytes": {
                                    "type": "integer",
                                    "description": "The size of the file in bytes. Required for create, must be a non-negative integer."
                                },
                                "uploaded_by": {
                                    "type": "string",
                                    "description": "The user ID of the person who uploaded the attachment. Required for create. Must refer to an existing active user."
                                }
                            }
                        }
                    },
                    "required": ["action"]
                }
            }
        }