import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class ProcessCandidate(Tool):
    """
    Execute candidate records including creation for recruitment processes.
    """
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        action: str,
        candidate_id: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        email: Optional[str] = None,
        source: Optional[str] = None,
        phone_number: Optional[str] = None,
        address: Optional[str] = None,
        status: Optional[str] = None,
    ) -> str:
        """
        Executes the specified action (create or update) on candidate records.
        """
        def generate_id(table: Dict[str, Any]) -> str:
            """Generates a new unique ID for a record."""
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        def validate_email_format(email: str) -> bool:
            """Basic email format validation"""
            return "@" in email and "." in email.split("@")[1]

        timestamp = "2025-10-01T12:00:00"
        candidates = data.get("candidates", {})

        # Validate supported sources based on SOPs
        supported_sources = ["website", "referral", "linkedin", "job_board", "recruiter", "other"]
        
        # Map SOPs sources to existing data sources for compatibility
        source_mapping = {
            "website": "company_website",
            "referral": "referral", 
            "linkedin": "social_media",
            "job_board": "job_board",
            "recruiter": "recruiter",
            "other": "career_fair"  # Map 'other' to existing career_fair for compatibility
        }

        # Validate supported statuses
        supported_statuses = ["new", "screening", "interviewing", "offered", "hired", "rejected"]

        if action == "create":
            # Required fields for candidate creation
            if not all([first_name, last_name, email, source]):
                return json.dumps({
                    "error": "Missing required parameters for create operation. Required: first_name, last_name, email, source"
                })

            # Validate source
            if source not in supported_sources:
                return json.dumps({
                    "error": f"Invalid source '{source}'. Must be one of: {', '.join(supported_sources)}"
                })

            # Validate email format
            if not validate_email_format(email):
                return json.dumps({
                    "error": "Invalid email format"
                })

            # Check for duplicate email addresses
            for existing_candidate in candidates.values():
                if existing_candidate.get("email", "").lower() == email.lower():
                    return json.dumps({
                        "error": f"Candidate with email '{email}' already exists"
                    })

            # Validate status if provided
            if status and status not in supported_statuses:
                return json.dumps({
                    "error": f"Invalid status '{status}'. Must be one of: {', '.join(supported_statuses)}"
                })

            # Generate new candidate ID
            new_candidate_id = generate_id(candidates)

            # Map source to internal format for data consistency
            internal_source = source_mapping.get(source, source)

            # Create new candidate record
            new_candidate = {
                "candidate_id": new_candidate_id,
                "first_name": first_name.strip(),
                "last_name": last_name.strip(),
                "email": email.lower().strip(),
                "phone_number": phone_number.strip() if phone_number else None,
                "address": address.strip() if address else None,
                "source": internal_source,
                "status": status if status else "new",
                "created_at": timestamp,
                "updated_at": timestamp
            }

            # Add to candidates data
            candidates[new_candidate_id] = new_candidate

            return json.dumps({
                "success": True,
                "message": f"Candidate '{first_name} {last_name}' created successfully",
                "candidate_id": new_candidate_id,
                "candidate_data": new_candidate
            })

        elif action == "update":
            # Required field for candidate update
            if not candidate_id:
                return json.dumps({
                    "error": "Missing required parameter 'candidate_id' for update operation"
                })

            # At least one optional field must be provided
            optional_fields = [first_name, last_name, email, source, phone_number, address, status]
            if not any(field is not None for field in optional_fields):
                return json.dumps({
                    "error": "At least one optional parameter (first_name, last_name, email, source, phone_number, address, status) must be provided for update operation"
                })

            # Check if candidate exists
            if candidate_id not in candidates:
                return json.dumps({
                    "error": f"Candidate with ID '{candidate_id}' not found"
                })

            # Validate source if provided
            if source and source not in supported_sources:
                return json.dumps({
                    "error": f"Invalid source '{source}'. Must be one of: {', '.join(supported_sources)}"
                })

            # Validate email format if provided
            if email and not validate_email_format(email):
                return json.dumps({
                    "error": "Invalid email format"
                })

            # Check for duplicate email addresses (excluding current candidate)
            if email:
                for existing_candidate_id, existing_candidate in candidates.items():
                    if (existing_candidate_id != candidate_id and 
                        existing_candidate.get("email", "").lower() == email.lower()):
                        return json.dumps({
                            "error": f"Candidate with email '{email}' already exists"
                        })

            # Validate status if provided
            if status and status not in supported_statuses:
                return json.dumps({
                    "error": f"Invalid status '{status}'. Must be one of: {', '.join(supported_statuses)}"
                })

            # Update candidate record
            candidate_record = candidates[candidate_id]
            
            if first_name:
                candidate_record["first_name"] = first_name.strip()
            if last_name:
                candidate_record["last_name"] = last_name.strip()
            if email:
                candidate_record["email"] = email.lower().strip()
            if source:
                # Map source to internal format for data consistency
                internal_source = source_mapping.get(source, source)
                candidate_record["source"] = internal_source
            if phone_number is not None:  # Allow setting to None
                candidate_record["phone_number"] = phone_number.strip() if phone_number else None
            if address is not None:  # Allow setting to None
                candidate_record["address"] = address.strip() if address else None
            if status:
                candidate_record["status"] = status
            
            candidate_record["updated_at"] = timestamp

            return json.dumps({
                "success": True,
                "message": f"Candidate with ID '{candidate_id}' updated successfully",
                "candidate_id": candidate_id,
                "candidate_data": candidate_record
            })

        else:
            return json.dumps({
                "error": f"Invalid action '{action}'. Must be 'create' or 'update'"
            })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "process_candidate",
                "description": "Execute candidate records for recruitment processes. For creation, requires first_name, last_name, email, and source (website, referral, linkedin, job_board, recruiter, other), with optional fields for phone_number, address, and status (new, screening, interviewing, offered, hired, rejected). For updates, requires candidate_id and at least one optional field. Used for adding candidate records and updating candidate information throughout the recruitment process.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "The action to perform: 'create' to add a new candidate, 'update' to modify an existing candidate",
                            "enum": ["create", "update"]
                        },
                        "candidate_id": {
                            "type": "string",
                            "description": "Candidate ID (required for update operations)"
                        },
                        "first_name": {
                            "type": "string",
                            "description": "First name (required for create, optional for update)"
                        },
                        "last_name": {
                            "type": "string",
                            "description": "Last name (required for create, optional for update)"
                        },
                        "email": {
                            "type": "string",
                            "description": "Email address (required for create, optional for update)"
                        },
                        "source": {
                            "type": "string",
                            "description": "Source of candidate: 'website', 'referral', 'linkedin', 'job_board', 'recruiter', or 'other' (required for create, optional for update)",
                            "enum": ["website", "referral", "linkedin", "job_board", "recruiter", "other"]
                        },
                        "phone_number": {
                            "type": "string",
                            "description": "Phone number (optional for both create and update)"
                        },
                        "address": {
                            "type": "string",
                            "description": "Address (optional for both create and update)"
                        },
                        "status": {
                            "type": "string",
                            "description": "Candidate status: 'new', 'screening', 'interviewing', 'offered', 'hired', or 'rejected' (optional for both create and update, defaults to 'new')",
                            "enum": ["new", "screening", "interviewing", "offered", "hired", "rejected"]
                        }
                    },
                    "required": ["action"]
                }
            }
        }