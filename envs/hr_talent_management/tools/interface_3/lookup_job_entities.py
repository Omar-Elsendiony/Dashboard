import json
from typing import Any, Dict, List, Optional
from tau_bench.envs.tool import Tool


class LookupJobEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Optional[Dict[str, Any]] = None) -> str:
        """
        Discover and retrieve job entities including job requisitions and job postings.

        entity_type: "job_requisitions" | "job_postings"
        filters: optional dict with exact-match filtering and date range support
        Returns: {"entities": list, "count": int, "message": str}
        """

        if entity_type not in ["job_requisitions", "job_postings"]:
            return json.dumps({
                "entities": [],
                "count": 0,
                "message": f"Invalid entity_type '{entity_type}'. Must be 'job_requisitions' or 'job_postings'"
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

        if entity_type == "job_requisitions":
            requisitions = data.get("job_requisitions", {})

            # Supported requisition filters
            requisition_exact_keys = [
                "requisition_id", "job_title", "department_id", "location_id", 
                "employment_type", "hiring_manager_id", "grade", "shift_type", 
                "remote_indicator", "status", "hr_manager_approver", "dept_head_approver", 
                "created_by"
            ]

            for requisition_id, requisition in requisitions.items():
                record = {**requisition}

                if filters:
                    # Exact-match filters
                    if not apply_exact_filters(record, requisition_exact_keys, filters):
                        continue

                    # Date range filters
                    if not in_date_range(record.get("hr_manager_approval_date"), "hr_manager_approval_date_from", "hr_manager_approval_date_to", filters):
                        continue
                    if not in_date_range(record.get("dept_head_approval_date"), "dept_head_approval_date_from", "dept_head_approval_date_to", filters):
                        continue
                    if not in_date_range(record.get("posted_date"), "posted_date_from", "posted_date_to", filters):
                        continue

                # ensure id present as string
                record["requisition_id"] = str(requisition_id)
                results.append(record)

            return json.dumps({
                "success": True,
                "entity_type": "job_requisitions",
                "count": len(results),
                "entities": results,
                "filters_applied": filters or {}
            })

        if entity_type == "job_postings":
            postings = data.get("job_postings", {})

            # Supported posting filters
            posting_exact_keys = [
                "posting_id", "requisition_id", "portal_type", "status"
            ]

            for posting_id, posting in postings.items():
                record = {**posting}

                if filters:
                    # Exact-match filters
                    if not apply_exact_filters(record, posting_exact_keys, filters):
                        continue

                    # Date range filters
                    if not in_date_range(record.get("posted_date"), "posted_date_from", "posted_date_to", filters):
                        continue
                    if not in_date_range(record.get("closed_date"), "closed_date_from", "closed_date_to", filters):
                        continue

                # ensure id present as string
                record["posting_id"] = str(posting_id)
                results.append(record)

            return json.dumps({
                "success": True,
                "entity_type": "job_postings",
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
                "name": "lookup_job_entities",
                "description": "Discover and retrieve job entities including job requisitions and job postings.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of job entity to discover. Valid values: 'job_requisitions', 'job_postings'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters for discovery. For job_requisitions: requisition_id, job_title, department_id, location_id, employment_type, hiring_manager_id, grade, shift_type, remote_indicator, status, hr_manager_approver, dept_head_approver, hr_manager_approval_date_from, hr_manager_approval_date_to, dept_head_approval_date_from, dept_head_approval_date_to, posted_date_from, posted_date_to, created_by. For job_postings: posting_id, requisition_id, posted_date_from, posted_date_to, portal_type, status, closed_date_from, closed_date_to"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }

