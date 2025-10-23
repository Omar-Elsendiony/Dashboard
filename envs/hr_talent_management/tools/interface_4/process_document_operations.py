import json
import re
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool
from datetime import datetime


class ProcessDocumentOperations(Tool):
    
    @staticmethod
    def invoke(data: Dict[str, Any], operation_type: str, **kwargs) -> str:
        """
        Manages document operations including upload, verification, and status updates.
        """
        
        # --- Utility Functions ---
        def generate_id(table: Dict[str, Any]) -> int:
            """Utility to generate a new sequential ID for the documents table."""
            if not table:
                return 9001
            return max(int(k) for k in table.keys()) + 1

        def validate_date_format(date_str: str, field_name: str) -> Optional[str]:
            """Validates date format is YYYY-MM-DD."""
            if date_str:
                date_pattern = r'^\d{4}-\d{2}-\d{2}$'
                if not re.match(date_pattern, date_str):
                    return f"Invalid {field_name} format. Must be YYYY-MM-DD"
                
                try:
                    datetime.strptime(date_str, '%Y-%m-%d')
                except ValueError:
                    return f"Invalid date value provided for {field_name}. Please check year/month/day validity."
            return None

        def convert_date_format(date_str: str) -> str:
            """Convert YYYY-MM-DD format for internal storage."""
            if date_str and re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
                return date_str
            return date_str

        def validate_file_format(file_name: str) -> tuple[str, Optional[str]]:
            """Extract and validate file format from file name. Returns (extension, error_message)."""
            if not file_name:
                return "", "File name cannot be empty"
            
            # Extract extension
            if '.' not in file_name:
                return "", "File name must have a valid extension (e.g., .pdf, .doc, .docx, .txt, .jpg, .png, .xls, .xlsx)"
            
            extension = file_name.split('.')[-1].lower()
            
            # Validate common document formats
            valid_formats = ['pdf', 'doc', 'docx', 'txt', 'jpg', 'jpeg', 'png', 'gif', 'xls', 'xlsx', 'csv', 'rtf', 'odt', 'ods', 'ppt', 'pptx']
            if extension not in valid_formats:
                return "", f"Invalid file extension '{extension}'. Supported formats: {', '.join(valid_formats)}"
            
            return extension, None
        
        valid_operations = ["upload_document", "verify_document", "update_document_status"]
        if operation_type not in valid_operations:
            return json.dumps({
                "success": False,
                "document_id": None,
                "message": f"Invalid operation_type '{operation_type}'. Must be one of: {', '.join(valid_operations)}"
            })

        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "document_id": None,
                "message": "Invalid data format for document operations"
            })
        
        documents = data.get("documents", {})
        users = data.get("users", {})

        # --- Document Upload (upload_document) ---
        if operation_type == "upload_document":
            required_fields = ["document_category", "related_entity_type", "related_entity_id", "file_name", "uploaded_by"]
            missing_fields = [field for field in required_fields if field not in kwargs or kwargs[field] is None]
            
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "document_id": None,
                    "message": f"Missing mandatory fields: {', '.join(missing_fields)}"
                })

            # 1. Validate uploaded_by user exists and is active
            uploaded_by_user = users.get(str(kwargs["uploaded_by"]))
            if not uploaded_by_user or uploaded_by_user.get("employment_status") != "active":
                return json.dumps({
                    "success": False,
                    "document_id": None,
                    "message": "Halt: Uploader user not found or inactive"
                })

            # 2. Validate document_category enum
            valid_categories = [
                "verification_id_proof", "verification_address_proof", "verification_educational_certificate",
                "verification_experience_letter", "verification_work_visa", "verification_pr_card",
                "verification_bank_proof", "offer_letter", "contract", "policy_acknowledgment",
                "tax_form", "insurance_form", "nda", "resume", "cover_letter", "job_description",
                "budget_justification", "budget_approval", "headcount_justification", "workforce_plan", "recruitment_checklist",
                "promotion_letter", "transfer_memo", "other"
            ]
            if kwargs["document_category"] not in valid_categories:
                return json.dumps({
                    "success": False,
                    "document_id": None,
                    "message": f"Invalid document_category. Must be one of: {', '.join(valid_categories)}"
                })

            # 3. Validate related_entity_type enum
            valid_entity_types = [
                "employee", "candidate", "offer", "onboarding", "job_requisition", "job_posting", "application", "benefit"
            ]
            if kwargs["related_entity_type"] not in valid_entity_types:
                return json.dumps({
                    "success": False,
                    "document_id": None,
                    "message": f"Halt: Invalid related_entity_type. Must be one of: {', '.join(valid_entity_types)}"
                })
            
            # 3.1. Validate related_entity_id
            related_entity_id = kwargs["related_entity_id"]
            if not related_entity_id or not isinstance(related_entity_id, str) or len(related_entity_id.strip()) == 0:
                return json.dumps({
                    "success": False,
                    "document_id": None,
                    "message": "Halt: related_entity_id must be a non-empty string"
                })

            # 4. Validate file_name and extract file format
            file_name = kwargs["file_name"]
            if not file_name or len(file_name.strip()) == 0:
                return json.dumps({
                    "success": False,
                    "document_id": None,
                    "message": "Halt: File name cannot be empty"
                })
            if len(file_name) > 255:
                return json.dumps({
                    "success": False,
                    "document_id": None,
                    "message": "Halt: File name cannot exceed 255 characters"
                })
            
            # Validate file extension
            file_extension, extension_error = validate_file_format(file_name)
            if extension_error:
                return json.dumps({
                    "success": False,
                    "document_id": None,
                    "message": f"Halt: {extension_error}"
                })

            # 5. Check for duplicate file name
            for existing_doc in documents.values():
                if existing_doc.get("file_name") == file_name:
                    return json.dumps({
                        "success": False,
                        "document_id": None,
                        "message": "Halt: Document with this file name already exists"
                    })

            # 6. Handle upload_date (default to 2025-10-10 if not provided)
            upload_date = kwargs.get("upload_date", "2025-10-10")
            
            # Validate upload_date format
            upload_date_error = validate_date_format(upload_date, "upload_date")
            if upload_date_error:
                return json.dumps({
                    "success": False,
                    "document_id": None,
                    "message": f"Halt: {upload_date_error}"
                })
            
            # Validate that upload_date is not in the future
            try:
                upload_dt = datetime.strptime(convert_date_format(upload_date), '%Y-%m-%d')
                current_dt = datetime.strptime("2025-10-10", '%Y-%m-%d')
                if upload_dt > current_dt:
                    return json.dumps({
                        "success": False,
                        "document_id": None,
                        "message": "Halt: Upload date cannot be in the future"
                    })
            except ValueError:
                return json.dumps({
                    "success": False,
                    "document_id": None,
                    "message": "Halt: Invalid upload date format"
                })

            # 7. Validate expiry_date format if provided
            expiry_date = kwargs.get("expiry_date")
            if expiry_date:
                expiry_date_error = validate_date_format(expiry_date, "expiry_date")
                if expiry_date_error:
                    return json.dumps({
                        "success": False,
                        "document_id": None,
                        "message": f"Halt: {expiry_date_error}"
                    })
                
                # Validate that expiry_date is not in the past
                try:
                    expiry_dt = datetime.strptime(convert_date_format(expiry_date), '%Y-%m-%d')
                    current_dt = datetime.strptime("2025-10-10", '%Y-%m-%d')
                    if expiry_dt < current_dt:
                        return json.dumps({
                            "success": False,
                            "document_id": None,
                            "message": "Halt: Expiry date cannot be in the past"
                        })
                except ValueError:
                    return json.dumps({
                        "success": False,
                        "document_id": None,
                        "message": "Halt: Invalid expiry date format"
                    })

            # 8. Create Document
            new_document_id = generate_id(documents)
            timestamp = "2025-10-10T12:00:00"

            new_document = {
                "document_id": str(new_document_id),
                "document_category": kwargs["document_category"],
                "related_entity_type": kwargs["related_entity_type"],
                "related_entity_id": related_entity_id.strip(),
                "file_name": file_name.strip(),
                "file_format": file_extension,
                "upload_date": convert_date_format(upload_date),
                "uploaded_by": str(kwargs["uploaded_by"]),
                "document_status": "active",
                "expiry_date": convert_date_format(expiry_date) if expiry_date else None,
                "verification_status": "pending" if kwargs["document_category"].startswith("verification_") else None,
                "verified_by": None,
                "verified_date": None,
                "created_at": timestamp
            }
            
            documents[str(new_document_id)] = new_document
            
            return json.dumps({
                "success": True,
                "document_id": str(new_document_id),
                "message": f"Document {new_document_id} uploaded successfully",
                "document_data": new_document
            })

        # --- Document Verification (verify_document) ---
        elif operation_type == "verify_document":
            required_fields = ["document_id", "verification_status", "verified_by", "verified_date"]
            missing_fields = [field for field in required_fields if field not in kwargs or kwargs[field] is None]
            
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "document_id": None,
                    "message": f"Missing mandatory fields: {', '.join(missing_fields)}"
                })

            document_id_str = str(kwargs["document_id"])
            document = documents.get(document_id_str)
            
            # 1. Verify document exists and is active
            if not document or document.get("document_status") != "active":
                return json.dumps({
                    "success": False,
                    "document_id": document_id_str,
                    "message": "Halt: Document not found or not in 'active' status"
                })

            # 2. Validate verifier user exists and is active
            verifier_user = users.get(str(kwargs["verified_by"]))
            if not verifier_user or verifier_user.get("employment_status") != "active":
                return json.dumps({
                    "success": False,
                    "document_id": document_id_str,
                    "message": "Halt: Verifier user not found or inactive"
                })

            # 3. Validate verifier has appropriate role
            verifier_role = verifier_user.get("role")
            valid_verifier_roles = ["compliance_officer", "finance_manager", "hr_manager"]
            if verifier_role not in valid_verifier_roles:
                return json.dumps({
                    "success": False,
                    "document_id": document_id_str,
                    "message": "Halt: Verifier not authorized (must be Compliance Officer, Finance Manager, or HR Manager)"
                })

            # 4. Validate verification_status enum
            valid_statuses = ["pending", "verified", "failed"]
            if kwargs["verification_status"] not in valid_statuses:
                return json.dumps({
                    "success": False,
                    "document_id": document_id_str,
                    "message": f"Invalid verification_status. Must be one of: {', '.join(valid_statuses)}"
                })

            # 5. Validate verified_date format
            verified_date_error = validate_date_format(kwargs["verified_date"], "verified_date")
            if verified_date_error:
                return json.dumps({
                    "success": False,
                    "document_id": document_id_str,
                    "message": f"Halt: {verified_date_error}"
                })
            
            # Validate that verified_date is not in the future
            try:
                verified_dt = datetime.strptime(convert_date_format(kwargs["verified_date"]), '%Y-%m-%d')
                current_dt = datetime.strptime("2025-10-10", '%Y-%m-%d')
                if verified_dt > current_dt:
                    return json.dumps({
                        "success": False,
                        "document_id": document_id_str,
                        "message": "Halt: Verification date cannot be in the future"
                    })
            except ValueError:
                return json.dumps({
                    "success": False,
                    "document_id": document_id_str,
                    "message": "Halt: Invalid verification date format"
                })

            # 6. Update document verification
            document["verification_status"] = kwargs["verification_status"]
            document["verified_by"] = str(kwargs["verified_by"])
            document["verified_date"] = convert_date_format(kwargs["verified_date"])
            
            return json.dumps({
                "success": True,
                "document_id": document_id_str,
                "message": f"Document {document_id_str} verification status updated to '{kwargs['verification_status']}' successfully"
            })

        # --- Document Status Update (update_document_status) ---
        elif operation_type == "update_document_status":
            required_fields = ["document_id", "document_status", "user_id"]
            missing_fields = [field for field in required_fields if field not in kwargs or kwargs[field] is None]
            
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "document_id": None,
                    "message": f"Missing mandatory fields: {', '.join(missing_fields)}"
                })

            document_id_str = str(kwargs["document_id"])
            document = documents.get(document_id_str)
            
            # 1. Verify document exists
            if not document:
                return json.dumps({
                    "success": False,
                    "document_id": document_id_str,
                    "message": "Halt: Document not found"
                })

            # 2. Validate user authorization
            user = users.get(str(kwargs["user_id"]))
            if not user or user.get("employment_status") != "active":
                return json.dumps({
                    "success": False,
                    "document_id": document_id_str,
                    "message": "Halt: User not found or inactive"
                })

            # 3. Validate user has appropriate role
            user_role = user.get("role")
            valid_roles = ["hr_admin", "hr_manager", "hr_director"]
            if user_role not in valid_roles:
                return json.dumps({
                    "success": False,
                    "document_id": document_id_str,
                    "message": "Halt: User lacks authorization to perform this action"
                })

            # 4. Validate document_status enum
            valid_statuses = ["active", "archived", "expired"]
            if kwargs["document_status"] not in valid_statuses:
                return json.dumps({
                    "success": False,
                    "document_id": document_id_str,
                    "message": f"Invalid document_status. Must be one of: {', '.join(valid_statuses)}"
                })

            # 5. Validate status transitions
            current_status = document.get("document_status")
            new_status = kwargs["document_status"]
            
            # Define valid status transitions
            valid_transitions = {
                "active": ["archived", "expired"],
                "archived": ["active"],  # Can reactivate archived documents
                "expired": ["active"]    # Can reactivate expired documents
            }
            
            if new_status not in valid_transitions.get(current_status, []):
                return json.dumps({
                    "success": False,
                    "document_id": document_id_str,
                    "message": f"Invalid status transition from '{current_status}' to '{new_status}'"
                })

            # 6. Update document status
            document["document_status"] = new_status
            
            return json.dumps({
                "success": True,
                "document_id": document_id_str,
                "message": f"Document {document_id_str} status updated to '{new_status}' successfully"
            })

        return json.dumps({
            "success": False,
            "document_id": None,
            "message": "Unhandled operation type"
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "process_document_operations",
                "description": "Manages document operations in the HR talent management system. 'upload_document' establishes new document records with comprehensive validation of document categories (verification_id_proof, verification_address_proof, verification_educational_certificate, verification_experience_letter, verification_work_visa, verification_pr_card, verification_bank_proof, offer_letter, contract, policy_acknowledgment, tax_form, insurance_form, nda, resume, cover_letter, job_description, budget_justification, budget_approval, workforce_plan, recruitment_checklist, promotion_letter, transfer_memo, other), related entity types (employee, candidate, offer, onboarding, job_requisition, job_posting, application), file names with valid extensions (pdf, doc, docx, txt, jpg, jpeg, png, gif, xls, xlsx, csv, rtf, odt, ods, ppt, pptx), upload dates, and user permissions. Validates file formats, prevents duplicate file names, and enforces proper document categorization. 'verify_document' manages document verification workflow by updating verification status (pending, verified, failed) with proper authorization validation for Compliance Officers, Finance Managers, and HR Managers. 'update_document_status' manages document lifecycle by updating status (active, archived, expired) with proper status transition validation. Essential for document management, compliance tracking, audit trails, and maintaining proper document status throughout the employee lifecycle including onboarding verification, offer documentation, policy acknowledgments, and benefits enrollment documents.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation_type": {
                            "type": "string",
                            "description": "Type of operation: 'upload_document' to create new document record, 'verify_document' to update verification status, 'update_document_status' to update document lifecycle status",
                            "enum": ["upload_document", "verify_document", "update_document_status"]
                        },
                        "document_category": {
                            "type": "string",
                            "description": "Category of the document (required for upload_document)",
                            "enum": ["verification_id_proof", "verification_address_proof", "verification_educational_certificate", "verification_experience_letter", "verification_work_visa", "verification_pr_card", "verification_bank_proof", "offer_letter", "contract", "policy_acknowledgment", "tax_form", "insurance_form", "nda", "resume", "cover_letter", "job_description", "budget_justification", "budget_approval", "headcount_justification", "workforce_plan", "recruitment_checklist", "promotion_letter", "transfer_memo", "other"]
                        },
                        "related_entity_type": {
                            "type": "string",
                            "description": "Type of entity this document relates to (required for upload_document)",
                            "enum": ["employee", "candidate", "offer", "onboarding", "job_requisition", "job_posting", "application", "benefit"]
                        },
                        "related_entity_id": {
                            "type": "string",
                            "description": "ID of the related entity (required for upload_document)"
                        },
                        "file_name": {
                            "type": "string",
                            "description": "Name of the uploaded file (required for upload_document, must be unique, max 255 characters)"
                        },
                        "upload_date": {
                            "type": "string",
                            "description": "Date when document was uploaded in YYYY-MM-DD format (optional for upload_document, defaults to 2025-10-10)"
                        },
                        "uploaded_by": {
                            "type": "string",
                            "description": "User ID of the person uploading the document (required for upload_document, must exist and be active)"
                        },
                        "expiry_date": {
                            "type": "string",
                            "description": "Document expiry date in YYYY-MM-DD format (optional for upload_document)"
                        },
                        "document_id": {
                            "type": "string",
                            "description": "Document ID (required for verify_document and update_document_status, must exist)"
                        },
                        "verification_status": {
                            "type": "string",
                            "description": "Verification status (required for verify_document)",
                            "enum": ["pending", "verified", "failed"]
                        },
                        "verified_by": {
                            "type": "string",
                            "description": "User ID of the person verifying the document (required for verify_document, must be Compliance Officer, Finance Manager, or HR Manager)"
                        },
                        "verified_date": {
                            "type": "string",
                            "description": "Date when document was verified in YYYY-MM-DD format (required for verify_document)"
                        },
                        "document_status": {
                            "type": "string",
                            "description": "Document lifecycle status (required for update_document_status)",
                            "enum": ["active", "archived", "expired"]
                        },
                        "user_id": {
                            "type": "string",
                            "description": "User ID performing the status update (required for update_document_status, must be HR Admin, HR Manager, or HR Director)"
                        }
                    },
                    "required": ["operation_type"]
                }
            }
        }
