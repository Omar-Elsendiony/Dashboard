import json
from typing import Any, Dict, List, Optional
from tau_bench.envs.tool import Tool

class FetchDocumentTaskEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Optional[Dict[str, Any]] = None) -> str:
        """
        Discover document and task entities including documents and IT provisioning tasks with optional filtering.
        
        Entity Types:
        - documents: Discover documents with category, status, date, and verification filters
        - it_provisioning_tasks: Discover IT provisioning tasks with employee, type, and status filters
        """
        
        def matches_filter(entity: Dict[str, Any], filter_key: str, filter_value: Any) -> bool:
            """Check if entity matches a specific filter"""
            
            # Handle different filter types
            if filter_key.endswith('_from') or filter_key.endswith('_to'):
                # Date range filters - map to correct entity field names
                if filter_key.startswith('upload_date_'):
                    entity_field = 'upload_date'
                elif filter_key.startswith('expiry_date_'):
                    entity_field = 'expiry_date'
                elif filter_key.startswith('completion_date_'):
                    entity_field = 'completion_date'
                else:
                    return False
                
                entity_value = entity.get(entity_field)
                
                if entity_value is None:
                    return False
                
                if filter_key.endswith('_from'):
                    return entity_value >= filter_value
                else:  # _to
                    return entity_value <= filter_value
            else:
                # Exact match filters (case-insensitive for text fields)
                entity_value = entity.get(filter_key)
                
                if entity_value is None:
                    return False
                
                if isinstance(entity_value, str) and isinstance(filter_value, str):
                    return entity_value.lower() == filter_value.lower()
                else:
                    return str(entity_value).lower() == str(filter_value).lower()
        
        def validate_filter_conflicts(filters: Dict[str, Any]) -> Optional[str]:
            """Validate that filter parameters don't result in conflicting results"""
            if not filters:
                return None
            
            # Check for conflicting date ranges
            date_conflicts = []
            for base_field in ["upload_date", "expiry_date", "completion_date"]:
                from_key = f"{base_field}_from"
                to_key = f"{base_field}_to"
                
                if from_key in filters and to_key in filters:
                    from_value = filters[from_key]
                    to_value = filters[to_key]
                    if from_value > to_value:
                        date_conflicts.append(f"{base_field} range: {from_value} > {to_value}")
            
            if date_conflicts:
                return f"Search parameters result in ambiguous or conflicting results: {', '.join(date_conflicts)}"
            
            return None
        
        def apply_filters(entities: Dict[str, Any], valid_filters: List[str], filters: Dict[str, Any]) -> Dict[str, Any]:
            """Apply filters to entities and return matching results"""
            if not filters:
                return entities
            
            # Validate filter conflicts
            conflict_error = validate_filter_conflicts(filters)
            if conflict_error:
                return {"error": f"Halt: {conflict_error}"}
            
            # Validate filter keys
            invalid_filters = [key for key in filters.keys() if key not in valid_filters]
            if invalid_filters:
                return {
                    "error": f"Halt: Discovery tool execution failed due to system errors - invalid filter keys: {', '.join(invalid_filters)}. Valid filters are: {', '.join(valid_filters)}"
                }
            
            filtered_entities = {}
            for entity_id, entity in entities.items():
                matches = True
                for filter_key, filter_value in filters.items():
                    if not matches_filter(entity, filter_key, filter_value):
                        matches = False
                        break
                
                if matches:
                    filtered_entities[entity_id] = entity
            
            return filtered_entities
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Halt: Discovery tool execution failed due to system errors - invalid data format"
            })
        
        if entity_type not in ["documents", "it_provisioning_tasks"]:
            return json.dumps({
                "success": False,
                "error": "Halt: Missing entity_type or invalid entity_type - must be one of: documents, it_provisioning_tasks"
            })
        
        if entity_type == "documents":
            entities = data.get("documents", {})
            valid_filters = [
                "document_id", "document_category", "related_entity_type", "related_entity_id", 
                "file_name", "upload_date_from", "upload_date_to", "uploaded_by", 
                "document_status", "expiry_date_from", "expiry_date_to", "verification_status", "verified_by"
            ]
            
            if filters:
                filtered_entities = apply_filters(entities, valid_filters, filters)
                if "error" in filtered_entities:
                    return json.dumps({
                        "success": False,
                        "error": filtered_entities["error"]
                    })
                entities = filtered_entities
            
            return json.dumps({
                "success": True,
                "entity_type": "documents",
                "count": len(entities),
                "entities": entities,
                "filters_applied": filters or {}
            })
        
        elif entity_type == "it_provisioning_tasks":
            entities = data.get("it_provisioning_tasks", {})
            valid_filters = [
                "task_id", "employee_id", "task_type", "assigned_to", 
                "task_status", "completion_date_from", "completion_date_to"
            ]
            
            if filters:
                filtered_entities = apply_filters(entities, valid_filters, filters)
                if "error" in filtered_entities:
                    return json.dumps({
                        "success": False,
                        "error": filtered_entities["error"]
                    })
                entities = filtered_entities
            
            return json.dumps({
                "success": True,
                "entity_type": "it_provisioning_tasks",
                "count": len(entities),
                "entities": entities,
                "filters_applied": filters or {}
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "fetch_document_task_entities",
                "description": "Discover and filter document and task entities in the HR talent management system. This tool allows comprehensive discovery of documents and IT provisioning tasks with flexible filtering options. Supports date range filtering and exact match filtering for document details, task status, and verification information. Essential for document management, compliance tracking, and IT task oversight.\n\nEntity Types:\n- 'documents': Discover documents with category, status, date, and verification filters\n  * document_category: resume, cover_letter, verification_id_proof, verification_address_proof, verification_educational_certificate, verification_experience_letter, verification_work_visa, verification_pr_card, verification_bank_proof, budget_approval, headcount_justification, offer_letter, contract, policy_acknowledgment, insurance_form, tax_form, promotion_letter, transfer_memo, other\n  * related_entity_type: candidate, employee, offer, onboarding, benefit, job_requisition\n  * document_status: active, archived, expired\n  * verification_status: pending, verified, rejected\n  * Available filters: document_id, document_category, related_entity_type, related_entity_id, file_name, upload_date_from, upload_date_to, uploaded_by, document_status, expiry_date_from, expiry_date_to, verification_status, verified_by\n\n- 'it_provisioning_tasks': Discover IT provisioning tasks with employee, type, and status filters\n  * task_type: laptop_setup, software_installation, access_provisioning, email_setup, security_training, equipment_delivery, other\n  * task_status: pending, in_progress, completed, cancelled\n  * Available filters: task_id, employee_id, task_type, assigned_to, task_status, completion_date_from, completion_date_to",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of document/task entity to discover",
                            "enum": ["documents", "it_provisioning_tasks"]
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters to apply. For documents: document_id, document_category, related_entity_type, related_entity_id, file_name, upload_date_from, upload_date_to, uploaded_by, document_status, expiry_date_from, expiry_date_to, verification_status, verified_by. For it_provisioning_tasks: task_id, employee_id, task_type, assigned_to, task_status, completion_date_from, completion_date_to. SYNTAX: {\"key\": \"value\"}",
                            "properties": {
                                # Documents filters
                                "document_id": {"type": "string", "description": "Exact document ID match"},
                                "document_category": {"type": "string", "description": "Document category", "enum": ["resume", "cover_letter", "verification_id_proof", "verification_address_proof", "verification_educational_certificate", "verification_experience_letter", "verification_work_visa", "verification_pr_card", "verification_bank_proof", "budget_approval", "headcount_justification", "offer_letter", "contract", "policy_acknowledgment", "insurance_form", "tax_form", "promotion_letter", "transfer_memo", "other"]},
                                "related_entity_type": {"type": "string", "description": "Related entity type", "enum": ["candidate", "employee", "offer", "onboarding", "benefit", "job_requisition"]},
                                "related_entity_id": {"type": "string", "description": "Related entity ID match"},
                                "file_name": {"type": "string", "description": "File name match (case-insensitive)"},
                                "upload_date_from": {"type": "string", "description": "Upload date from (YYYY-MM-DD)"},
                                "upload_date_to": {"type": "string", "description": "Upload date to (YYYY-MM-DD)"},
                                "uploaded_by": {"type": "string", "description": "User who uploaded the document"},
                                "document_status": {"type": "string", "description": "Document status", "enum": ["active", "archived", "expired"]},
                                "expiry_date_from": {"type": "string", "description": "Expiry date from (YYYY-MM-DD)"},
                                "expiry_date_to": {"type": "string", "description": "Expiry date to (YYYY-MM-DD)"},
                                "verification_status": {"type": "string", "description": "Verification status", "enum": ["pending", "verified", "rejected"]},
                                "verified_by": {"type": "string", "description": "User who verified the document"},
                                
                                # IT Provisioning Tasks filters
                                "task_id": {"type": "string", "description": "Exact task ID match"},
                                "employee_id": {"type": "string", "description": "Employee ID match"},
                                "task_type": {"type": "string", "description": "Task type", "enum": ["laptop_setup", "software_installation", "access_provisioning", "email_setup", "security_training", "equipment_delivery", "other"]},
                                "assigned_to": {"type": "string", "description": "User assigned to the task"},
                                "task_status": {"type": "string", "description": "Task status", "enum": ["pending", "in_progress", "completed", "cancelled"]},
                                "completion_date_from": {"type": "string", "description": "Completion date from (YYYY-MM-DD)"},
                                "completion_date_to": {"type": "string", "description": "Completion date to (YYYY-MM-DD)"}
                            }
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
