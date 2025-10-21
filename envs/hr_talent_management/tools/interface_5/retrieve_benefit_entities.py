import json
from typing import Any, Dict, List, Optional
from tau_bench.envs.tool import Tool

class RetrieveBenefitEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Optional[Dict[str, Any]] = None, requesting_user_id: str = None) -> str:
        """
        Discover benefit entities including plans and enrollments with optional filtering.
        
        Entity Types:
        - benefit_plans: Discover benefit plans with type, status, and date filters
        - benefit_enrollments: Discover benefit enrollments with employee, plan, and approval filters
        """
        
        def matches_filter(entity: Dict[str, Any], filter_key: str, filter_value: Any) -> bool:
            """Check if entity matches a specific filter"""
            
            # Handle different filter types
            if filter_key.endswith('_from') or filter_key.endswith('_to'):
                # Date range filters - map to correct entity field names
                if filter_key.startswith('effective_from_'):
                    entity_field = 'effective_from'
                elif filter_key.startswith('effective_until_'):
                    entity_field = 'effective_until'
                elif filter_key.startswith('effective_date_'):
                    entity_field = 'effective_date'
                elif filter_key.startswith('enrollment_window_start_'):
                    entity_field = 'enrollment_window_start'
                elif filter_key.startswith('enrollment_window_end_'):
                    entity_field = 'enrollment_window_end'
                elif filter_key.startswith('approval_date_'):
                    entity_field = 'approval_date'
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
            for base_field in ["effective_from", "effective_until", "effective_date", "enrollment_window_start", "enrollment_window_end", "approval_date"]:
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
        
        if entity_type not in ["benefit_plans", "benefit_enrollments"]:
            return json.dumps({
                "success": False,
                "error": "Halt: Missing entity_type or invalid entity_type - must be one of: benefit_plans, benefit_enrollments"
            })
        
        # Validate requesting user authorization
        if requesting_user_id:
            users = data.get("users", {})
            if requesting_user_id not in users:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Unauthorized requester attempting to access restricted entities - user not found"
                })
            
            user = users[requesting_user_id]
            user_role = user.get("role")
            valid_roles = ["hr_payroll_administrator", "hr_manager", "hr_admin", "finance_manager"]
            
            if user_role not in valid_roles:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Unauthorized requester attempting to access restricted entities - insufficient permissions"
                })
            
            if user.get("employment_status") != "active":
                return json.dumps({
                    "success": False,
                    "error": "Halt: Unauthorized requester attempting to access restricted entities - user not active"
                })
        
        if entity_type == "benefit_plans":
            entities = data.get("benefit_plans", {})
            valid_filters = [
                "plan_id", "benefit_type", "plan_name", "provider_name", "plan_status",
                "effective_from_from", "effective_from_to", "effective_until_from", "effective_until_to"
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
                "entity_type": "benefit_plans",
                "count": len(entities),
                "entities": entities,
                "filters_applied": filters or {}
            })
        
        elif entity_type == "benefit_enrollments":
            entities = data.get("benefit_enrollments", {})
            valid_filters = [
                "enrollment_id", "employee_id", "plan_id", "effective_date_from", "effective_date_to",
                "enrollment_window_start_from", "enrollment_window_start_to", "enrollment_window_end_from", 
                "enrollment_window_end_to", "enrollment_status", "hr_manager_approval_status", 
                "approved_by", "approval_date_from", "approval_date_to"
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
                "entity_type": "benefit_enrollments",
                "count": len(entities),
                "entities": entities,
                "filters_applied": filters or {}
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "retrieve_benefit_entities",
				"description": "List and filter benefit plans and enrollments with clear input guidance for trainers.\n\nWhat this tool does:\n- Returns entities for benefit_plans or benefit_enrollments.\n- Supports exact matches and date ranges using …_from/…_to.\n- Enforces optional requester authorization if provided.\n\nWho can use it:\n- Anyone can omit requesting_user_id. If provided, requester must be active with role in {hr_payroll_administrator, hr_manager, hr_admin, finance_manager}.\n\nInput guidance:\n- entity_type: Choose one of benefit_plans | benefit_enrollments.\n- filters: Provide an object with keys listed below for the chosen entity_type. Use YYYY-MM-DD for dates. Unknown filter keys will be rejected.\n\nAllowed filters by entity_type:\n- benefit_plans: plan_id, benefit_type (medical|dental|vision|401k|life_insurance|disability), plan_name, provider_name, plan_status (active|inactive|discontinued), effective_from_from, effective_from_to, effective_until_from, effective_until_to.\n- benefit_enrollments: enrollment_id, employee_id, plan_id, effective_date_from, effective_date_to, enrollment_window_start_from, enrollment_window_start_to, enrollment_window_end_from, enrollment_window_end_to, enrollment_status (pending|valid|outside_window|approved|active), hr_manager_approval_status (pending|approved|rejected), approved_by, approval_date_from, approval_date_to.\n\nExample queries:\n- Active medical plans effective in 2025:\n{\n  \"entity_type\": \"benefit_plans\",\n  \"filters\": {\n    \"benefit_type\": \"medical\",\n    \"plan_status\": \"active\",\n    \"effective_from_from\": \"2025-01-01\",\n    \"effective_until_to\": \"2025-12-31\"\n  }\n}\n- Approved enrollments within enrollment window:\n{\n  \"entity_type\": \"benefit_enrollments\",\n  \"filters\": {\n    \"enrollment_status\": \"approved\",\n    \"enrollment_window_start_from\": \"2025-01-01\",\n    \"enrollment_window_end_to\": \"2025-03-31\"\n  }\n}\n\nTypical errors if inputs are incorrect:\n- Missing or invalid entity_type.\n- Invalid filter keys or conflicting ranges (e.g., *_from > *_to).\n- Unauthorized requester when requesting_user_id is provided but not permitted.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
							"description": "Type of benefit entity to discover: benefit_plans | benefit_enrollments",
                            "enum": ["benefit_plans", "benefit_enrollments"]
                        },
                        "requesting_user_id": {
                            "type": "string",
							"description": "Optional requester id. If provided: must exist, be 'active', and role in {hr_payroll_administrator, hr_manager, hr_admin, finance_manager}."
                        },
                        "filters": {
                            "type": "object",
							"description": "Optional filters to apply. For benefit_plans: plan_id, benefit_type, plan_name, provider_name, plan_status, effective_from_from, effective_from_to, effective_until_from, effective_until_to. For benefit_enrollments: enrollment_id, employee_id, plan_id, effective_date_from, effective_date_to, enrollment_window_start_from, enrollment_window_start_to, enrollment_window_end_from, enrollment_window_end_to, enrollment_status, hr_manager_approval_status, approved_by, approval_date_from, approval_date_to. SYNTAX: {\"key\": \"value\"}",
                            "properties": {
                                # Benefit Plans filters
                                "plan_id": {"type": "string", "description": "Exact plan ID match"},
                                "benefit_type": {"type": "string", "description": "Benefit type", "enum": ["medical", "dental", "vision", "401k", "life_insurance", "disability"]},
                                "plan_name": {"type": "string", "description": "Plan name match (case-insensitive)"},
                                "provider_name": {"type": "string", "description": "Provider name match (case-insensitive)"},
                                "plan_status": {"type": "string", "description": "Plan status", "enum": ["active", "inactive", "discontinued"]},
                                "effective_from_from": {"type": "string", "description": "Effective from date from (YYYY-MM-DD)"},
                                "effective_from_to": {"type": "string", "description": "Effective from date to (YYYY-MM-DD)"},
                                "effective_until_from": {"type": "string", "description": "Effective until date from (YYYY-MM-DD)"},
                                "effective_until_to": {"type": "string", "description": "Effective until date to (YYYY-MM-DD)"},
                                
                                # Benefit Enrollments filters
                                "enrollment_id": {"type": "string", "description": "Exact enrollment ID match"},
                                "employee_id": {"type": "string", "description": "Employee ID match"},
                                "plan_id": {"type": "string", "description": "Plan ID match"},
                                "effective_date_from": {"type": "string", "description": "Effective date from (YYYY-MM-DD)"},
                                "effective_date_to": {"type": "string", "description": "Effective date to (YYYY-MM-DD)"},
                                "enrollment_window_start_from": {"type": "string", "description": "Enrollment window start from (YYYY-MM-DD)"},
                                "enrollment_window_start_to": {"type": "string", "description": "Enrollment window start to (YYYY-MM-DD)"},
                                "enrollment_window_end_from": {"type": "string", "description": "Enrollment window end from (YYYY-MM-DD)"},
                                "enrollment_window_end_to": {"type": "string", "description": "Enrollment window end to (YYYY-MM-DD)"},
                                "enrollment_status": {"type": "string", "description": "Enrollment status", "enum": ["pending", "valid", "outside_window", "approved", "active"]},
                                "hr_manager_approval_status": {"type": "string", "description": "HR manager approval status", "enum": ["pending", "approved", "rejected"]},
                                "approved_by": {"type": "string", "description": "User who approved"},
                                "approval_date_from": {"type": "string", "description": "Approval date from (YYYY-MM-DD)"},
                                "approval_date_to": {"type": "string", "description": "Approval date to (YYYY-MM-DD)"}
                            }
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
