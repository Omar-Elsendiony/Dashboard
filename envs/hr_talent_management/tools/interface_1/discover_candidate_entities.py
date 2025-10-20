import json
from typing import Any, Dict, List, Optional
from tau_bench.envs.tool import Tool


class DiscoverCandidateEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Optional[Dict[str, Any]] = None) -> str:
        """
        Discover and retrieve candidate-related entities including candidates, applications, and shortlists.

        entity_type: "candidates" | "applications"
        filters: optional dict with exact-match filtering and date range support
        Returns: {"entities": list, "count": int, "message": str}
        """

        if entity_type not in ["candidates", "applications"]:
            return json.dumps({
                "entities": [],
                "count": 0,
                "message": f"Invalid entity_type '{entity_type}'. Must be 'candidates' or 'applications'"
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

        results: List[Dict[str, Any]] = []

        if entity_type == "candidates":
            candidates = data.get("candidates", {})

            # Supported candidate filters
            candidate_exact_keys = [
                "candidate_id", "first_name", "last_name", "email_address", 
                "contact_number", "country_of_residence", "status", "source_of_application"
            ]

            for candidate_id, candidate in candidates.items():
                record = {**candidate}

                # Exact-match filters
                if filters:
                    if not apply_exact_filters(record, candidate_exact_keys, filters):
                        continue

                # ensure id present as string
                record["candidate_id"] = str(candidate_id)
                results.append(record)

            return json.dumps({
                "success": True,
                "entity_type": "candidates",
                "count": len(results),
                "entities": results,
                "filters_applied": filters or {}
            })

        if entity_type == "applications":
            applications = data.get("applications", {})

            # Supported application filters
            application_exact_keys = [
                "application_id", "candidate_id", "posting_id", "resume_file_id", 
                "cover_letter_file_id", "status", "screened_by", "shortlist_approved_by"
            ]

            for application_id, application in applications.items():
                record = {**application}

                if filters:
                    # Exact-match filters
                    if not apply_exact_filters(record, application_exact_keys, filters):
                        continue

                    # Date range filters for application_date
                    if not in_date_range(record.get("application_date"), "application_date_from", "application_date_to", filters):
                        continue
                    
                    # Date range filters for screened_date
                    if not in_date_range(record.get("screened_date"), "screened_date_from", "screened_date_to", filters):
                        continue
                    
                    # Date range filters for shortlist_approval_date
                    if not in_date_range(record.get("shortlist_approval_date"), "shortlist_approval_date_from", "shortlist_approval_date_to", filters):
                        continue

                # ensure id present as string
                record["application_id"] = str(application_id)
                results.append(record)

            return json.dumps({
                "success": True,
                "entity_type": "applications",
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
                "name": "discover_candidate_entities",
                "description": "Discover and retrieve candidate-related entities including candidates, applications, and shortlists.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of candidate entity to discover. Valid values: 'candidates', 'applications'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters for discovery. For candidates: candidate_id, first_name, last_name, email_address, contact_number, country_of_residence, status, source_of_application. For applications: application_id, candidate_id, posting_id, resume_file_id, cover_letter_file_id, application_date_from, application_date_to, status, screened_by, shortlist_approved_by, shortlist_approval_date_from, shortlist_approval_date_to, screened_date_from, screened_date_to"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }



