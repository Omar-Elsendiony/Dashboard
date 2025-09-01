import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class LogKnowledgeBaseArticle(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        title: str,
        article_type: str,
        category: str,
        created_by_id: str,
        incident_id: str = None,
        reviewed_by_id: str = None,
        status: str = "draft"
    ) -> str:
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        try:
            articles = data.setdefault("knowledge_base_articles", {})

            valid_types = {"troubleshooting","resolution_steps","prevention_guide","faq"}
            if article_type not in valid_types:
                return json.dumps({"success": False, "error": f"Invalid article_type. Must be one of {sorted(valid_types)}"})

            valid_status = {"draft","published","archived"}
            if status not in valid_status:
                return json.dumps({"success": False, "error": f"Invalid status. Must be one of {sorted(valid_status)}"})

            article_id = generate_id(articles)
            timestamp = "2025-10-01T00:00:00"

            new_article = {
                "article_id": article_id,
                "incident_id": incident_id,
                "title": title,
                "article_type": article_type,
                "created_by_id": created_by_id,
                "reviewed_by_id": reviewed_by_id,
                "category": category,
                "view_count": 0,
                "status": status,
                "created_at": timestamp,
                "updated_at": timestamp
            }

            articles[article_id] = new_article
            return json.dumps({"article_id": article_id, "status": status, "success": True})
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return  {
            "type": "function",
            "function": {
                "name": "log_knowledge_base_article",
                "description": "Create a knowledge base article; initializes view_count and timestamps",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "article_type": {"type": "string", "description": "troubleshooting|resolution_steps|prevention_guide|faq"},
                        "category": {"type": "string", "description": "category enum value"},
                        "created_by_id": {"type": "string"},
                        "incident_id": {"type": "string"},
                        "reviewed_by_id": {"type": "string"},
                        "status": {"type": "string", "description": "draft|published|archived (default draft)"}
                    },
                    "required": ["title","article_type","category","created_by_id"]
                }
            }
        }
