# update_performance_review.py
import json
from typing import Any, Dict, Optional

from tau_bench.envs.tool import Tool


class UpdatePerformanceReview(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        review_id: str,
        overall_rating: Optional[str] = None,
        goals_achievement_score: Optional[float] = None,
        communication_score: Optional[float] = None,
        teamwork_score: Optional[float] = None,
        leadership_score: Optional[float] = None,
        technical_skills_score: Optional[float] = None,
        comments: Optional[str] = None,
        development_goals: Optional[str] = None,
        status: Optional[str] = None,
        hr_manager_approval: Optional[bool] = None,
    ) -> str:
        """
        Update fields on an existing performance review.
        Returns JSON: {"success": True, "message": "Performance review updated"} or {"error": "...", "halt": True}
        """

        # ---------- helpers ----------
        def one_decimal(val: float) -> str:
            # format to DECIMAL(3,1)
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

        # ---------- load ----------
        reviews = data.get("performance_reviews", {})

        # ---------- validations ----------
        if not review_id:
            raise ValueError("review_id is required")
        if str(review_id) not in reviews:
            return json.dumps({"error": f"Performance review {review_id} not found", "halt": True})

        # If nothing to update
        if all(
            v is None
            for v in [
                overall_rating,
                goals_achievement_score,
                communication_score,
                teamwork_score,
                leadership_score,
                technical_skills_score,
                comments,
                development_goals,
                status,
            ]
        ):
            return json.dumps({"success": True, "message": "No changes provided"})

        # Enums
        if overall_rating is not None:
            valid_ratings = [
                "exceeds_expectations",
                "meets_expectations",
                "below_expectations",
                "unsatisfactory",
            ]
            if overall_rating not in valid_ratings:
                return json.dumps(
                    {"error": f"Invalid overall_rating. Must be one of {valid_ratings}", "halt": True}
                )

        if status is not None:
            valid_statuses = ["draft", "submitted", "approved"]
            if status not in valid_statuses:
                return json.dumps(
                    {"error": f"Invalid status. Must be one of {valid_statuses}", "halt": True}
                )
            if status == "approved":
                if hr_manager_approval is None:
                    return json.dumps(
                        {"error": "HR Manager approval required to approve a review", "halt": True}
                    )
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

        # ---------- persist ----------
        row = reviews[str(review_id)]
        timestamp = "2025-10-01T00:00:00"

        if overall_rating is not None:
            row["overall_rating"] = overall_rating
        if goals_achievement_score is not None:
            row["goals_achievement_score"] = goals_s
        if communication_score is not None:
            row["communication_score"] = comm_s
        if teamwork_score is not None:
            row["teamwork_score"] = team_s
        if leadership_score is not None:
            row["leadership_score"] = lead_s
        if technical_skills_score is not None:
            row["technical_skills_score"] = tech_s
        if comments is not None:
            row["comments"] = comments  # not in schema, safe as in-memory field
        if development_goals is not None:
            row["development_goals"] = development_goals  # not in schema, safe in-memory
        if status is not None:
            row["status"] = status
            if status == "approved":
                row["approved_by"] = "hr_manager"  # optional in-memory audit field

        row["updated_at"] = timestamp

        reviews[str(review_id)] = row
        data["performance_reviews"] = reviews

        return json.dumps({"success": True, "message": "Performance review updated"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_performance_review",
                "description": "Update fields on an existing performance review (scores 1.0–5.0; HR Manager approval required if approving).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "review_id": {"type": "string", "description": "Review ID (required)"},
                        "overall_rating": {"type": "string", "description": "exceeds_expectations, meets_expectations, below_expectations, unsatisfactory (optional)"},
                        "goals_achievement_score": {"type": "number", "description": "1.0–5.0 (optional)"},
                        "communication_score": {"type": "number", "description": "1.0–5.0 (optional)"},
                        "teamwork_score": {"type": "number", "description": "1.0–5.0 (optional)"},
                        "leadership_score": {"type": "number", "description": "1.0–5.0 (optional)"},
                        "technical_skills_score": {"type": "number", "description": "1.0–5.0 (optional)"},
                        "comments": {"type": "string", "description": "Updated comments (optional)"},
                        "development_goals": {"type": "string", "description": "Updated development goals (optional)"},
                        "status": {"type": "string", "description": "draft, submitted, approved (optional)"},
                        "hr_manager_approval": {"type": "boolean", "description": "Required if status=approved"}
                    },
                    "required": ["review_id"]
                }
            }
        }
