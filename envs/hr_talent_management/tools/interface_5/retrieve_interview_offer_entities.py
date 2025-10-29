import json
from typing import Any, Dict, List, Optional
from tau_bench.envs.tool import Tool


class RetrieveInterviewOfferEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Optional[Dict[str, Any]] = None) -> str:
        """
        Discover and retrieve interview and offer entities.

        entity_type: "interviews" | "offers"
        filters: optional dict with exact-match filtering, date ranges, and numeric ranges
        Returns: {"entities": list, "count": int, "message": str}
        """

        if entity_type not in ["interviews", "offers"]:
            return json.dumps({
                "entities": [],
                "count": 0,
                "message": f"Invalid entity_type '{entity_type}'. Must be 'interviews' or 'offers'"
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

        def in_numeric_range(numeric_value: Optional[float], min_key: str, max_key: str, filters_obj: Dict[str, Any]) -> bool:
            if numeric_value is None:
                return False if (min_key in filters_obj or max_key in filters_obj) else True
            if min_key in filters_obj and numeric_value < filters_obj[min_key]:
                return False
            if max_key in filters_obj and numeric_value > filters_obj[max_key]:
                return False
            return True

        results: List[Dict[str, Any]] = []

        if entity_type == "interviews":
            interviews = data.get("interviews", {})
            interview_panel_members = data.get("interview_panel_members", {})

            # Supported interview filters
            interview_exact_keys = [
                "interview_id", "application_id", "interview_type", "interview_status", 
                "recommendation", "completed_by"
            ]

            for interview_id, interview in interviews.items():
                record = {**interview}

                if filters:
                    # Exact-match filters
                    if not apply_exact_filters(record, interview_exact_keys, filters):
                        continue

                    # Date range filters
                    if not in_date_range(record.get("scheduled_date"), "scheduled_date_from", "scheduled_date_to", filters):
                        continue
                    if not in_date_range(record.get("completed_date"), "completed_date_from", "completed_date_to", filters):
                        continue

                    # Numeric range filters for rating
                    if not in_numeric_range(record.get("rating"), "rating_min", "rating_max", filters):
                        continue

                # Look up panel members for this interview
                panel_member_ids = []
                for panel_member_id, panel_member in interview_panel_members.items():
                    if panel_member.get("interview_id") == interview_id:
                        panel_member_ids.append(panel_member.get("user_id"))
                
                # Add panel_member_ids to the record
                record["panel_member_ids"] = panel_member_ids

                # ensure id present as string
                record["interview_id"] = str(interview_id)
                results.append(record)

            return json.dumps({
                "success": True,
                "entity_type": "interviews",
                "count": len(results),
                "entities": results,
                "filters_applied": filters or {}
            })

        if entity_type == "offers":
            offers = data.get("offers", {})

            # Supported offer filters
            offer_exact_keys = [
                "offer_id", "candidate_id", "requisition_id", "position", 
                "reporting_manager_id", "offer_status", "compliance_approved_by", "hr_manager_approved_by"
            ]

            for offer_id, offer in offers.items():
                record = {**offer}

                if filters:
                    # Exact-match filters
                    if not apply_exact_filters(record, offer_exact_keys, filters):
                        continue

                    # Date range filters
                    if not in_date_range(record.get("start_date"), "start_date_from", "start_date_to", filters):
                        continue

                    # Numeric range filters for base_salary
                    if not in_numeric_range(record.get("base_salary"), "base_salary_min", "base_salary_max", filters):
                        continue

                # ensure id present as string
                record["offer_id"] = str(offer_id)
                results.append(record)

            return json.dumps({
                "success": True,
                "entity_type": "offers",
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
                "name": "retrieve_interview_offer_entities",
                "description": "Discover and retrieve interview and offer entities. For interviews, panel_member_ids (user_ids of panel members) are included in the returned entities.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover. Valid values: 'interviews', 'offers'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters for discovery. For interviews: interview_id, application_id, interview_type, scheduled_date_from, scheduled_date_to, interview_status, rating_min, rating_max, recommendation, completed_by, completed_date_from, completed_date_to. For offers: offer_id, candidate_id, requisition_id, position, start_date_from, start_date_to, base_salary_min, base_salary_max, reporting_manager_id, offer_status, compliance_approved_by, hr_manager_approved_by"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
