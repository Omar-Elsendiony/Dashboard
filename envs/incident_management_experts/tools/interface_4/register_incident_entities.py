import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class RegisterIncidentEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover incident-related entities.
        
        Supported entities:
        - incidents: Incident records
        - incident_reports: Incident report records
        - post_incident_reviews: Post-incident review records
        """
        if entity_type not in ["incidents", "incident_reports", "post_incident_reviews"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'incidents', 'incident_reports', or 'post_incident_reviews'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get(entity_type, {})
        
        # Determine the ID field based on entity type
        id_field_map = {
            "incidents": "incident_id",
            "incident_reports": "report_id",
            "post_incident_reviews": "pir_id"
        }
        id_field = id_field_map[entity_type]
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, id_field: str(entity_id)})
            else:
                results.append({**entity_data, id_field: str(entity_id)})
        
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
                "name": "register_incident_entities",
                "description": "Discover incident-related entities. Entity types: 'incidents' (incident records; filterable by incident_id (string), incident_code (string), title (string), reporter_id (string), assigned_manager_id (string), client_id (string), component_id (string), severity (enum: 'P1', 'P2', 'P3', 'P4'), status (enum: 'open', 'in_progress', 'resolved', 'closed'), impact (enum: 'critical', 'high', 'medium', 'low'), urgency (enum: 'critical', 'high', 'medium', 'low'), category (enum: 'system_outage', 'performance_degradation', 'security_incident', 'data_corruption', 'integration_failure', 'network_issue', 'hardware_failure', 'software_bug', 'configuration_error', 'capacity_issue', 'backup_failure', 'authentication_failure', 'api_error', 'database_issue', 'service_unavailable'), detection_source (enum: 'client_reported', 'internally_detected', 'monitoring_alert', 'vendor_reported', 'scheduled_maintenance', 'emergency_maintenance'), detected_at (timestamp), resolved_at (timestamp), closed_at (timestamp), rto_breach (boolean: True/False), sla_breach (boolean: True/False), is_recurring (boolean: True/False), downtime_minutes (int), created_at (timestamp), updated_at (timestamp)); 'incident_reports' (incident report records; filterable by report_id (string), incident_id (string), report_type (enum: 'executive_summary', 'technical_details', 'business_impact', 'compliance_report', 'post_mortem'), generated_by_id (string), generated_at (timestamp), status (enum: 'draft', 'completed', 'distributed'), created_at (timestamp)); 'post_incident_reviews' (post-incident review records; filterable by pir_id (string), incident_id (string), scheduled_date (timestamp), facilitator_id (string), timeline_accuracy_rating (int), communication_effectiveness_rating (int), technical_response_rating (int), status (enum: 'scheduled', 'completed', 'cancelled'), created_at (timestamp)).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'incidents', 'incident_reports', or 'post_incident_reviews'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False. For incidents, filters are: incident_id (string), incident_code (string), title (string), reporter_id (string), assigned_manager_id (string), client_id (string), component_id (string), severity (enum: 'P1', 'P2', 'P3', 'P4'), status (enum: 'open', 'in_progress', 'resolved', 'closed'), impact (enum: 'critical', 'high', 'medium', 'low'), urgency (enum: 'critical', 'high', 'medium', 'low'), category (enum: 'system_outage', 'performance_degradation', 'security_incident', 'data_corruption', 'integration_failure', 'network_issue', 'hardware_failure', 'software_bug', 'configuration_error', 'capacity_issue', 'backup_failure', 'authentication_failure', 'api_error', 'database_issue', 'service_unavailable'), detection_source (enum: 'client_reported', 'internally_detected', 'monitoring_alert', 'vendor_reported', 'scheduled_maintenance', 'emergency_maintenance'), detected_at (timestamp), resolved_at (timestamp), closed_at (timestamp), rto_breach (boolean: True/False), sla_breach (boolean: True/False), is_recurring (boolean: True/False), downtime_minutes (int), created_at (timestamp), updated_at (timestamp). For incident_reports, filters are: report_id (string), incident_id (string), report_type (enum: 'executive_summary', 'technical_details', 'business_impact', 'compliance_report', 'post_mortem'), generated_by_id (string), generated_at (timestamp), status (enum: 'draft', 'completed', 'distributed'), created_at (timestamp). For post_incident_reviews, filters are: pir_id (string), incident_id (string), scheduled_date (timestamp), facilitator_id (string), timeline_accuracy_rating (int), communication_effectiveness_rating (int), technical_response_rating (int), status (enum: 'scheduled', 'completed', 'cancelled'), created_at (timestamp)"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }