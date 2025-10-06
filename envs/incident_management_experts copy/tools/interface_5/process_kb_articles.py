import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ProcessKbArticles(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, article_data: Dict[str, Any] = None, article_id: str = None) -> str:
        """
        Create or update knowledge base articles.

        Actions:
        - create: requires article_data with title, article_type, created_by_id, category
        - update: requires article_id and article_data with fields to update
        """

        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1

        if action not in ["create", "update"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid action '{action}'. Must be 'create' or 'update'"
            })

        kb_articles = data.get("knowledge_base_articles", {})
        users = data.get("users", {})
        incidents = data.get("incidents", {})

        valid_article_types = ["troubleshooting", "resolution_steps", "prevention_guide", "faq"]
        valid_categories = [
            "authentication_issues", "payment_processing", "api_integration", "data_synchronization",
            "system_outages", "performance_degradation", "security_incidents", "backup_recovery",
            "user_management", "billing_issues", "compliance_procedures", "vendor_escalations",
            "configuration_changes", "monitoring_alerts", "network_connectivity", "database_issues",
            "file_transfer_problems", "reporting_errors", "mobile_app_issues", "browser_compatibility",
            "third_party_integrations", "scheduled_maintenance", "emergency_procedures", "client_onboarding",
            "account_provisioning", "sla_management", "incident_response", "change_management",
            "capacity_planning", "disaster_recovery"
        ]
        valid_statuses = ["draft", "published", "archived"]

        if action == "create":
            if not article_data:
                return json.dumps({
                    "success": False,
                    "error": "article_data is required for create action"
                })

            required_fields = ["title", "article_type", "created_by_id", "category"]
            missing = [f for f in required_fields if f not in article_data or not article_data.get(f)]
            if missing:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields for article creation: {', '.join(missing)}"
                })

            title = article_data["title"]
            article_type = article_data["article_type"]
            created_by_id = str(article_data["created_by_id"])
            category = article_data["category"]
            incident_id = article_data.get("incident_id")
            reviewed_by_id = article_data.get("reviewed_by_id")
            view_count = article_data.get("view_count", 0)
            status = article_data.get("status", "draft")

            # Validations
            if article_type not in valid_article_types:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid article_type. Must be one of: {', '.join(valid_article_types)}"
                })

            if category not in valid_categories:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid category. Must be one of: {', '.join(valid_categories)}"
                })

            if status not in valid_statuses:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                })

            if incident_id:
                if incident_id not in incidents:
                    return json.dumps({"success": False, "error": f"Incident {incident_id} not found"})
                if incidents[incident_id].get("status") not in ["resolved", "closed"]:
                    return json.dumps({"success": False, "error": f"Incident must be resolved or closed"})

            if reviewed_by_id and reviewed_by_id not in users:
                return json.dumps({"success": False, "error": f"Reviewer {reviewed_by_id} not found"})

            if not isinstance(view_count, int) or view_count < 0:
                return json.dumps({"success": False, "error": "view_count must be a non-negative integer"})

            new_article_id = generate_id(kb_articles)
            new_article = {
                "article_id": str(new_article_id),
                "incident_id": incident_id,
                "title": title,
                "article_type": article_type,
                "created_by_id": created_by_id,
                "reviewed_by_id": reviewed_by_id,
                "category": category,
                "view_count": view_count,
                "status": status,
                "created_at": "2025-10-02T12:00:00",
                "updated_at": "2025-10-02T12:00:00"
            }

            kb_articles[str(new_article_id)] = new_article
            return json.dumps({
                "success": True, 
                "action": "create", 
                "article_id": str(new_article_id),
                "message": f"KB article {new_article_id} created successfully", 
                "article_data": new_article
            })

        elif action == "update":
            if not article_id:
                return json.dumps({"success": False, "error": "article_id is required for update action"})
            if article_id not in kb_articles:
                return json.dumps({"success": False, "error": f"Knowledge base article {article_id} not found"})
            if not article_data:
                return json.dumps({"success": False, "error": "article_data is required for update action"})

            current_article = kb_articles[article_id].copy()
            for key in ["title", "article_type", "incident_id", "reviewed_by_id", "category", "view_count", "status"]:
                if key in article_data:
                    value = article_data[key]
                    # Validation for certain fields
                    if key == "article_type" and value not in valid_article_types:
                        return json.dumps({"success": False, "error": f"Invalid article_type. Must be one of: {', '.join(valid_article_types)}"})
                    if key == "category" and value not in valid_categories:
                        return json.dumps({"success": False, "error": f"Invalid category. Must be one of: {', '.join(valid_categories)}"})
                    if key == "status" and value not in valid_statuses:
                        return json.dumps({"success": False, "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"})
                    if key == "incident_id" and value and value not in incidents:
                        return json.dumps({"success": False, "error": f"Incident {value} not found"})
                    if key == "reviewed_by_id" and value and value not in users:
                        return json.dumps({"success": False, "error": f"Reviewer {value} not found"})
                    if key == "view_count" and (not isinstance(value, int) or value < 0):
                        return json.dumps({"success": False, "error": "view_count must be a non-negative integer"})
                    current_article[key] = value

            current_article["updated_at"] = "2025-10-02T12:00:00"
            kb_articles[article_id] = current_article
            return json.dumps({
                "success": True, 
                "action": "update", 
                "article_id": article_id,
                "message": f"KB article {article_id} updated successfully",
                "article_data": current_article
            })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "process_kb_articles",
                "description": "Create or update knowledge base articles in the incident management system. Supports creation with proper role validation and article categorization, and updates with field-level validation.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {"type": "string", "enum": ["create", "update"], "description": "Action to perform"},
                        "article_id": {"type": "string", "description": "ID of the KB article (required for update)"},
                        "article_data": {"type": "object", "description": "Article fields for create or update"}
                    },
                    "required": ["action"]
                }
            }
        }
