import json
from typing import Any, Dict, List, Optional
from tau_bench.envs.tool import Tool


class GetEmployeeEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Optional[Dict[str, Any]] = None) -> str:
        """
        Discover and retrieve employee-related entities including employees and onboarding checklists.

        entity_type: "employees" | "onboarding_checklists"
        filters: optional dict with exact-match filtering and date range support
        Returns: {"entities": list, "count": int, "message": str}
        """

        if entity_type not in ["employees", "onboarding_checklists"]:
            return json.dumps({
                "entities": [],
                "count": 0,
                "message": f"Invalid entity_type '{entity_type}'. Must be 'employees' or 'onboarding_checklists'"
            })

        if not isinstance(data, dict):
            return json.dumps({
                "entities": [],
                "count": 0,
                "message": f"Invalid data format for {entity_type}"
            })

        def apply_exact_filters(record: Dict[str, Any], exact_filter_keys: List[str], filters_obj: Dict[str, Any]) -> bool:
            for key in exact_filter_keys:
                if key in filters_obj:
                    if record.get(key) != filters_obj[key]:
                        return False
            return True

        def in_date_range(date_value: Optional[str], start_key: str, end_key: str, filters_obj: Dict[str, Any]) -> bool:
            if not date_value:
                return False if (start_key in filters_obj or end_key in filters_obj) else True
            if start_key in filters_obj and date_value < filters_obj[start_key]:
                return False
            if end_key in filters_obj and date_value > filters_obj[end_key]:
                return False
            return True

        def in_numeric_range(value: Optional[float], min_key: str, max_key: str, filters_obj: Dict[str, Any]) -> bool:
            if value is None:
                return False if (min_key in filters_obj or max_key in filters_obj) else True
            if min_key in filters_obj and value < filters_obj[min_key]:
                return False
            if max_key in filters_obj and value > filters_obj[max_key]:
                return False
            return True

        results: List[Dict[str, Any]] = []

        if entity_type == "employees":
            employees = data.get("employees", {})

            # Supported employee filters
            employee_exact_keys = [
                "employee_id", "candidate_id", "first_name", "last_name", 
                "employee_type", "department_id", "location_id", "job_title",
                "tax_id", "work_email", "phone_number", "manager_id", 
                "tax_filing_status", "employment_status"
            ]

            for employee_id, employee in employees.items():
                record = {**employee}

                if filters:
                    # Apply exact match filters
                    if not apply_exact_filters(record, employee_exact_keys, filters):
                        continue
                    
                    # Apply date range filters
                    if not in_date_range(record.get("start_date"), "start_date_from", "start_date_to", filters):
                        continue

                # ensure id present as string
                record["employee_id"] = str(employee_id)
                results.append(record)

            return json.dumps({
                "success": True,
                "entity_type": "employees",
                "count": len(results),
                "entities": results,
                "filters_applied": filters or {}
            })

        if entity_type == "onboarding_checklists":
            onboarding_checklists = data.get("onboarding_checklists", {})

            # Supported onboarding checklist filters
            checklist_exact_keys = [
                "checklist_id", "employee_id", "position", "hiring_manager_id",
                "pre_onboarding_status", "background_check_status", "document_verification_status",
                "it_provisioning_status", "orientation_completed", "benefits_enrollment_status",
                "overall_status"
            ]

            for checklist_id, checklist in onboarding_checklists.items():
                record = {**checklist}

                if filters:
                    # Apply exact match filters
                    if not apply_exact_filters(record, checklist_exact_keys, filters):
                        continue
                    
                    # Apply date range filters
                    if not in_date_range(record.get("start_date"), "start_date_from", "start_date_to", filters):
                        continue
                    
                    if not in_date_range(record.get("background_check_cleared_date"), "background_check_cleared_date_from", "background_check_cleared_date_to", filters):
                        continue
                    
                    if not in_date_range(record.get("orientation_date"), "orientation_date_from", "orientation_date_to", filters):
                        continue

                # ensure id present as string
                record["checklist_id"] = str(checklist_id)
                results.append(record)

            return json.dumps({
                "success": True,
                "entity_type": "onboarding_checklists",
                "count": len(results),
                "entities": results,
                "filters_applied": filters or {}
            })

        return json.dumps({
            "success": False,
            "error": "Halt: Missing entity_type or invalid entity_type"
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_employee_entities",
                "description": "Discover and retrieve employee-related entities with comprehensive filtering capabilities. This tool supports two entity types: (1) 'employees' - for employee records with personal, job, and employment details. Employee filters include: employee_id, candidate_id, first_name, last_name, employee_type (enum: 'full_time', 'part_time', 'contractor', 'intern'), department_id, location_id, job_title, start_date_from/to (YYYY-MM-DD), tax_id, work_email, phone_number, manager_id, tax_filing_status (enum: 'single', 'married_filing_joint', 'married_filing_separate', 'head_of_household', 'surviving_spouse'), employment_status (enum: 'active', 'inactive', 'on_leave', 'suspended', 'terminated'). (2) 'onboarding_checklists' - for onboarding process tracking and status monitoring. Onboarding filters include: checklist_id, employee_id, start_date_from/to (YYYY-MM-DD), position, hiring_manager_id, pre_onboarding_status (enum: 'pending', 'in_progress', 'completed'), background_check_status (enum: 'pending', 'in_progress', 'passed', 'failed'), document_verification_status (enum: 'pending', 'verified', 'failed'), it_provisioning_status (enum: 'pending', 'in_progress', 'completed'), orientation_completed (boolean), benefits_enrollment_status (enum: 'pending', 'in_progress', 'completed'), overall_status (enum: 'not_started', 'in_progress', 'completed', 'on_hold'), background_check_cleared_date_from/to (YYYY-MM-DD), orientation_date_from/to (YYYY-MM-DD). Supports exact match, date range, and boolean filtering for precise data retrieval.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of employee entity to discover. MUST be one of these exact values: 'employees' (for employee records with personal, job, and employment details) or 'onboarding_checklists' (for onboarding process tracking and status monitoring)"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters for discovery. Apply multiple filters for precise searches. For 'employees' entity_type, use these filters: employee_id (string), candidate_id (string), first_name (string), last_name (string), employee_type (enum: 'full_time', 'part_time', 'contractor', 'intern'), department_id (string), location_id (string), job_title (string), start_date_from (date YYYY-MM-DD), start_date_to (date YYYY-MM-DD), tax_id (string), work_email (string), phone_number (string), manager_id (string), tax_filing_status (enum: 'single', 'married_filing_joint', 'married_filing_separate', 'head_of_household', 'surviving_spouse'), employment_status (enum: 'active', 'inactive', 'on_leave', 'suspended', 'terminated'). For 'onboarding_checklists' entity_type, use these filters: checklist_id (string), employee_id (string), start_date_from (date YYYY-MM-DD), start_date_to (date YYYY-MM-DD), position (string), hiring_manager_id (string), pre_onboarding_status (enum: 'pending', 'in_progress', 'completed'), background_check_status (enum: 'pending', 'in_progress', 'passed', 'failed'), document_verification_status (enum: 'pending', 'verified', 'failed'), it_provisioning_status (enum: 'pending', 'in_progress', 'completed'), orientation_completed (boolean: true/false), benefits_enrollment_status (enum: 'pending', 'in_progress', 'completed'), overall_status (enum: 'not_started', 'in_progress', 'completed', 'on_hold'), background_check_cleared_date_from (date YYYY-MM-DD), background_check_cleared_date_to (date YYYY-MM-DD), orientation_date_from (date YYYY-MM-DD), orientation_date_to (date YYYY-MM-DD)"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
