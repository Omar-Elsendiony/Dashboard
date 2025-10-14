import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class DiscoverIncidentTracking(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover incident tracking entities (incidents, problem_tickets, work_notes, attachments, incident_reports, work_orders). 
        The entity to discover is decided by entity_type.
        Optionally, filters can be applied to narrow down the search results.
        
        Supported entities:
        - incidents: Incident records
        - problem_tickets: Problem Ticket records
        - work_notes: Work Note records
        - attachments: Attachment records
        - incident_reports: Incident Report records
        - work_orders: Work Order records
        """
        valid_types = ["incidents", "problem_tickets", "work_notes", "attachments", "incident_reports", "work_orders"]
        if entity_type not in valid_types:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be one of {valid_types}"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get(entity_type, {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    # Add appropriate ID field based on entity type
                    id_field_map = {
                        "incidents": "incident_id",
                        "problem_tickets": "problem_id",
                        "work_notes": "note_id",
                        "attachments": "attachment_id",
                        "incident_reports": "report_id",
                        "work_orders": "work_order_id"
                    }
                    id_field = id_field_map[entity_type]
                    results.append({**entity_data, id_field: entity_id})
            else:
                id_field_map = {
                    "incidents": "incident_id",
                    "problem_tickets": "problem_id",
                    "work_notes": "note_id",
                    "attachments": "attachment_id",
                    "incident_reports": "report_id",
                    "work_orders": "work_order_id"
                }
                id_field = id_field_map[entity_type]
                results.append({**entity_data, id_field: entity_id})
        
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
                "name": "discover_incident_tracking",
                "description": "Discover incident tracking entities (incidents, problem tickets, work notes, attachments, incident reports, work orders). The entity to discover is decided by entity_type. Optional filters can be applied to narrow down the search results. Entity types: 'incidents' (incident records; filterable by incident_id (string), problem_id (string), incident_number (string), title (string), description (text), category (enum: 'inquiry/help', 'software', 'hardware', 'Network', 'Database'), client_id (string), affected_ci_id (string), severity (enum: 'P1', 'P2', 'P3', 'P4'), impact (enum: 'critical', 'high', 'medium', 'low'), urgency (enum: 'critical', 'high', 'medium', 'low'), status (enum: 'open', 'in_progress', 'monitoring', 'resolved', 'closed'), reported_by (string), assigned_to (string), detection_time (timestamp), acknowledged_at (timestamp), resolved_at (timestamp), closed_at (timestamp), created_at (timestamp), updated_at (timestamp)), 'problem_tickets' (problem ticket records; filterable by problem_id (string), problem_number (string), client_id (string), title (string), description (text), status (enum: 'open', 'investigating', 'resolved', 'closed'), reported_by (string), created_at (timestamp), updated_at (timestamp)), 'work_notes' (work note records; filterable by note_id (string), incident_id (string), note_text (text), created_by (string), created_at (timestamp)), 'attachments' (attachment records; filterable by attachment_id (string), reference_id (string), reference_type (enum: 'incident', 'change', 'rca', 'report', 'pir', 'communication', 'work_order', 'problem'), file_name (string), file_url (string), file_type (string), file_size_bytes (bigint), uploaded_by (string), uploaded_at (timestamp)), 'incident_reports' (incident report records; filterable by report_id (string), report_number (string), report_title (string), incident_id (string), report_type (enum: 'post_incident_review', 'client_impact', 'compliance'), report_content (text), generated_by (string), generation_date (timestamp), report_status (enum: 'draft', 'completed', 'approved', 'archived')), 'work_orders' (work order records; filterable by work_order_id (string), work_order_number (string), change_id (string), incident_id (string), title (string), description (text), assigned_to (string), status (enum: 'pending', 'in_progress', 'completed', 'cancelled'), scheduled_date (timestamp), completed_at (timestamp), created_at (timestamp)).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'incidents', 'problem_tickets', 'work_notes', 'attachments', 'incident_reports', or 'work_orders'",
                            "enum": ["incidents", "problem_tickets", "work_notes", "attachments", "incident_reports", "work_orders"]
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False. For incidents: incident_id, problem_id, incident_number, title, description, category, client_id, affected_ci_id, severity, impact, urgency, status, reported_by, assigned_to, detection_time, acknowledged_at, resolved_at, closed_at, created_at, updated_at. For problem_tickets: problem_id, problem_number, client_id, title, description, status, reported_by, created_at, updated_at. For work_notes: note_id, incident_id, note_text, created_by, created_at. For attachments: attachment_id, reference_id, reference_type, file_name, file_url, file_type, file_size_bytes, uploaded_by, uploaded_at. For incident_reports: report_id, report_number, report_title, incident_id, report_type, report_content, generated_by, generation_date, report_status. For work_orders: work_order_id, work_order_number, change_id, incident_id, title, description, assigned_to, status, scheduled_date, completed_at, created_at"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }

