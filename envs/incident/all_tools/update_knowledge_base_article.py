import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdateKnowledgeBaseArticle(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        article_id: str,
        incident_id: str = None,
        title: str = None,
        article_type: str = None,   # troubleshooting|resolution_steps|prevention_guide|faq
        created_by_id: str = None,
        reviewed_by_id: str = None,
        category: str = None,       # enum from schema
        view_count: int = None,
        status: str = None          # draft|published|archived
    ) -> str:
        try:
            articles = data.get("knowledge_base_articles", {})
            if article_id not in articles:
                return json.dumps({"success": False, "error": f"Knowledge base article {article_id} not found"})

            valid_types = {"troubleshooting","resolution_steps","prevention_guide","faq"}
            valid_status = {"draft","published","archived"}

            if article_type and article_type not in valid_types:
                return json.dumps({"success": False, "error": f"Invalid article_type. Must be one of {sorted(valid_types)}"})
            if status and status not in valid_status:
                return json.dumps({"success": False, "error": f"Invalid status. Must be one of {sorted(valid_status)}"})
            if view_count is not None and view_count < 0:
                return json.dumps({"success": False, "error": "view_count must be non-negative"})

            a = articles[article_id]
            if incident_id is not None: a["incident_id"] = incident_id
            if title is not None: a["title"] = title
            if article_type is not None: a["article_type"] = article_type
            if created_by_id is not None: a["created_by_id"] = created_by_id
            if reviewed_by_id is not None: a["reviewed_by_id"] = reviewed_by_id
            if category is not None: a["category"] = category
            if view_count is not None: a["view_count"] = view_count
            if status is not None: a["status"] = status

            a["updated_at"] = "2025-10-01T00:00:00"
            return json.dumps(a)
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})
    
    @staticmethod
    def get_info()->Dict[str,Any]:
        return{
            "type":"function",
            "function":{
                "name":"update_knowledge_base_article",
                "description":"Update a knowledge base article; validates enums; sets updated_at",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "article_id":{"type":"string"},
                        "incident_id":{"type":"string"},
                        "title":{"type":"string"},
                        "article_type":{"type":"string","description":"troubleshooting|resolution_steps|prevention_guide|faq"},
                        "created_by_id":{"type":"string"},
                        "reviewed_by_id":{"type":"string"},
                        "category":{"type":"string","description":"enum from schema"},
                        "view_count":{"type":"integer"},
                        "status":{"type":"string","description":"draft|published|archived"}
                    },
                    "required":["article_id"]
                }
            }
        }
