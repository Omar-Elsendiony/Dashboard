import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class RegisterKnowledgeArticleEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover knowledge base article entities.
        
        Supported entities:
        - knowledge_base_articles: Knowledge base article records
        """
        if entity_type not in ["knowledge_base_articles"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'knowledge_base_articles'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get("knowledge_base_articles", {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, "article_id": str(entity_id)})
            else:
                results.append({**entity_data, "article_id": str(entity_id)})
        
        return json.dumps({
            "success": True,
            "entity_type": entity_type,
            "count": len(results),
            "results": results
        })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "register_knowledge_article_entities",
                "description": "Discover knowledge base article entities. Entity types: 'knowledge_base_articles' (knowledge base article records; filterable by article_id (string), incident_id (string), title (string), article_type (enum: 'troubleshooting', 'resolution_steps', 'prevention_guide', 'faq'), created_by_id (string), reviewed_by_id (string), category (enum: 'authentication_issues', 'payment_processing', 'api_integration', 'data_synchronization', 'system_outages', 'performance_degradation', 'security_incidents', 'backup_recovery', 'user_management', 'billing_issues', 'compliance_procedures', 'vendor_escalations', 'configuration_changes', 'monitoring_alerts', 'network_connectivity', 'database_issues', 'file_transfer_problems', 'reporting_errors', 'mobile_app_issues', 'browser_compatibility', 'third_party_integrations', 'scheduled_maintenance', 'emergency_procedures', 'client_onboarding', 'account_provisioning', 'sla_management', 'incident_response', 'change_management', 'capacity_planning', 'disaster_recovery'), view_count (int), status (enum: 'draft', 'published', 'archived'), created_at (timestamp), updated_at (timestamp)).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'knowledge_base_articles'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False. For knowledge_base_articles, filters are: article_id (string), incident_id (string), title (string), article_type (enum: 'troubleshooting', 'resolution_steps', 'prevention_guide', 'faq'), created_by_id (string), reviewed_by_id (string), category (enum: 'authentication_issues', 'payment_processing', 'api_integration', 'data_synchronization', 'system_outages', 'performance_degradation', 'security_incidents', 'backup_recovery', 'user_management', 'billing_issues', 'compliance_procedures', 'vendor_escalations', 'configuration_changes', 'monitoring_alerts', 'network_connectivity', 'database_issues', 'file_transfer_problems', 'reporting_errors', 'mobile_app_issues', 'browser_compatibility', 'third_party_integrations', 'scheduled_maintenance', 'emergency_procedures', 'client_onboarding', 'account_provisioning', 'sla_management', 'incident_response', 'change_management', 'capacity_planning', 'disaster_recovery'), view_count (int), status (enum: 'draft', 'published', 'archived'), created_at (timestamp), updated_at (timestamp)"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
