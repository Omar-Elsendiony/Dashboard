import json
from typing import Any, Dict, Optional, List
from tau_bench.envs.tool import Tool

class FetchKnowledgeBaseArticles(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        article_id: str = None,
        incident_id: str = None,
        created_by_id: str = None,
        reviewed_by_id: str = None,
        article_type: str = None,   # troubleshooting|resolution_steps|prevention_guide|faq
        category: str = None,       # full enum string
        status: str = None,         # draft|published|archived
        title_contains: str = None
    ) -> str:
        try:
            kbs: Dict[str, Any] = data.get("knowledge_base_articles", {})
            results: List[Dict[str, Any]] = []
            needle = title_contains.lower() if title_contains else None

            for a in kbs.values():
                if article_id and a.get("article_id") != article_id:
                    continue
                if incident_id and a.get("incident_id") != incident_id:
                    continue
                if created_by_id and a.get("created_by_id") != created_by_id:
                    continue
                if reviewed_by_id and a.get("reviewed_by_id") != reviewed_by_id:
                    continue
                if article_type and a.get("article_type") != article_type:
                    continue
                if category and a.get("category") != category:
                    continue
                if status and a.get("status") != status:
                    continue
                if needle and needle not in (a.get("title","").lower()):
                    continue
                results.append(a)

            return json.dumps(results)
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return  {
            "type": "function",
            "function": {
                "name": "fetch_knowledge_base_articles",
                "description": "Unified get/list for knowledge base articles with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "article_id": {"type": "string"},
                        "incident_id": {"type": "string"},
                        "created_by_id": {"type": "string"},
                        "reviewed_by_id": {"type": "string"},
                        "article_type": {"type": "string", "description": "troubleshooting|resolution_steps|prevention_guide|faq"},
                        "category": {"type": "string", "description": "category enum value"},
                        "status": {"type": "string", "description": "draft|published|archived"},
                        "title_contains": {"type": "string", "description": "case-insensitive substring on title"}
                    },
                    "required": []
                }
            }
        }
