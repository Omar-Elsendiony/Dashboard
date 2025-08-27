# create_performance_review.py
import json
from typing import Any, Dict, Optional
from datetime import datetime, date

from tau_bench.envs.tool import Tool


class CreatePerformanceReview(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        employee_id: str,
        reviewer_id: str,
        review_period_start: str,
        review_period_end: str,
        review_type: str,
        overall_rating: str,
        goals_achievement_score: Optional[float] = None,
        communication_score: Optional[float] = None,
        teamwork_score: Optional[float] = None,
        leadership_score: Optional[float] = None,
        technical_skills_score: Optional[float] = None,
        comments: Optional[str] = None,
        development_goals: Optional[str] = None,
        status: str = "draft",
        hr_manager_approval: Optional[bool] = None,
    ) -> str:
        """
        Create a performance review row in data["performance_reviews"].
        Returns JSON: {"review_id": str, "success": True} or {"error": "...", "halt": True}
        """

        # ---------- helpers ----------
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        def parse_date(d: str) -> date:
            try:
                return datetime.fromisoformat(d).date()
            except ValueError:
                try:
                    return datetime.strptime(d, "%Y-%m-%d").date()
                except Exception:
                    raise ValueError("Dates must be ISO format YYYY-MM-DD")

        def one_decimal(val: float) -> str:
            # DECIMAL(3,1) formatting as string
            return f"{round(float(val), 1):.1f}"

        def validate_score(name: str, val: Optional[float]) -> Optional[str]:
            if val is None:
                return None
            try:
                f = float(val)
            except Exception:
                raise ValueError(f"{name} must be a number between 1.0 and 5.0")
            if f < 1.0 or f > 5.0:
                raise ValueError(f"{name} must be between 1.0 and 5.0")
            return one_decimal(f)

        # ---------- load tables ----------
        reviews = data.get("performance_reviews", {})
        employees_tbl = data.get("employees") or data.get("users") or {}

        # ---------- required validations ----------
        if not employee_id:
            raise ValueError("employee_id is required")
        if not reviewer_id:
            raise ValueError("reviewer_id is required")
        if not review_period_start or not review_period_end:
            raise ValueError("review_period_start and review_period_end are required")
        if not review_type:
            raise ValueError("review_type is required")
        if not overall_rating:
            raise ValueError("overall_rating is required")

        # Employee & reviewer existence checks (by key or by id fields)
        def record_exists(table: Dict[str, Any], needle: str) -> bool:
            if needle in table:
                return True
            for v in table.values():
                if isinstance(v, dict) and str(v.get("employee_id") or v.get("user_id")) == str(needle):
                    return True
            return False

        if employees_tbl:
            if not record_exists(employees_tbl, str(employee_id)):
                return json.dumps({"error": f"Employee {employee_id} not found", "halt": True})
            if not record_exists(employees_tbl, str(reviewer_id)):
                return json.dumps({"error": f"Reviewer {reviewer_id} not found", "halt": True})

        # Enums
        valid_types = ["annual", "quarterly", "probationary", "project_based"]
        if review_type not in valid_types:
            return json.dumps({"error": f"Invalid review_type. Must be one of {valid_types}", "halt": True})

        valid_ratings = ["exceeds_expectations", "meets_expectations", "below_expectations", "unsatisfactory"]
        if overall_rating not in valid_ratings:
            return json.dumps({"error": f"Invalid overall_rating. Must be one of {valid_ratings}", "halt": True})

        valid_statuses = ["draft", "submitted", "approved"]
        if status not in valid_statuses:
            return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}", "halt": True})

        # Dates
        try:
            start_d = parse_date(review_period_start)
            end_d = parse_date(review_period_end)
        except ValueError as ve:
            return json.dumps({"error": str(ve), "halt": True})

        if end_d < start_d:
            return json.dumps({"error": "review_period_end must be on/after review_period_start", "halt": True})

        # If final approval requested, require HR Manager approval True
        if status == "approved":
            if hr_manager_approval is None:
                return json.dumps({"error": "HR Manager approval required to approve a review", "halt": True})
            if not hr_manager_approval:
                return json.dumps({"error": "Approval denied by HR Manager", "halt": True})

        # Scores (optional, must be 1.0–5.0 if provided)
        try:
            goals_s = validate_score("goals_achievement_score", goals_achievement_score)
            comm_s = validate_score("communication_score", communication_score)
            team_s = validate_score("teamwork_score", teamwork_score)
            lead_s = validate_score("leadership_score", leadership_score)
            tech_s = validate_score("technical_skills_score", technical_skills_score)
        except ValueError as ve:
            return json.dumps({"error": str(ve), "halt": True})

        # ---------- create row ----------
        review_id = generate_id(reviews)
        timestamp = "2025-10-01T00:00:00"

        new_row = {
            "review_id": review_id,
            "employee_id": str(employee_id),
            "reviewer_id": str(reviewer_id),
            "review_period_start": start_d.isoformat(),
            "review_period_end": end_d.isoformat(),
            "review_type": review_type,
            "overall_rating": overall_rating,
            "goals_achievement_score": goals_s,
            "communication_score": comm_s,
            "teamwork_score": team_s,
            "leadership_score": lead_s,
            "technical_skills_score": tech_s,
            "status": status,
            "created_at": timestamp,
            "updated_at": timestamp,
        }

        # Non-schema fields are safe to carry in-memory (for UI/audit)
        if comments is not None:
            new_row["comments"] = comments
        if development_goals is not None:
            new_row["development_goals"] = development_goals
        if status == "approved":
            new_row["approved_by"] = "hr_manager"

        reviews[review_id] = new_row
        data["performance_reviews"] = reviews

        return json.dumps({"review_id": review_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_performance_review",
                "description": "Create a performance review (scores 1.0–5.0; HR Manager approval required if approving).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "employee_id": {"type": "string", "description": "Employee ID (required)"},
                        "reviewer_id": {"type": "string", "description": "Reviewer user ID (required)"},
                        "review_period_start": {"type": "string", "description": "Start date YYYY-MM-DD (required)"},
                        "review_period_end": {"type": "string", "description": "End date YYYY-MM-DD (required)"},
                        "review_type": {"type": "string", "description": "annual, quarterly, probationary, project_based (required)"},
                        "overall_rating": {"type": "string", "description": "exceeds_expectations, meets_expectations, below_expectations, unsatisfactory (required)"},
                        "goals_achievement_score": {"type": "number", "description": "1.0–5.0 (optional)"},
                        "communication_score": {"type": "number", "description": "1.0–5.0 (optional)"},
                        "teamwork_score": {"type": "number", "description": "1.0–5.0 (optional)"},
                        "leadership_score": {"type": "number", "description": "1.0–5.0 (optional)"},
                        "technical_skills_score": {"type": "number", "description": "1.0–5.0 (optional)"},
                        "comments": {"type": "string", "description": "Review comments (optional)"},
                        "development_goals": {"type": "string", "description": "Development goals (optional)"},
                        "status": {"type": "string", "description": "draft, submitted, approved (default draft)"},
                        "hr_manager_approval": {"type": "boolean", "description": "Required if status=approved"}
                    },
                    "required": [
                        "employee_id",
                        "reviewer_id",
                        "review_period_start",
                        "review_period_end",
                        "review_type",
                        "overall_rating"
                    ]
                }
            }
        }
