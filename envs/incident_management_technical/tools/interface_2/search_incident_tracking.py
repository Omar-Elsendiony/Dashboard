import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class SearchIncidentTracking(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover incident tracking entities (incidents, problem_tickets, work_notes, attachments, 
        incident_reports, work_orders, incident_configuration_items, problem_configuration_items). 
        The entity to discover is decided by entity_type. Optionally, filters can be applied to narrow down the search results.
        
        Supported entities:
        - incidents: Incident records
        - problem_tickets: Problem Ticket records
        - work_notes: Work Note records
        - attachments: Attachment records
        - incident_reports: Incident Report records
        - work_orders: Work Order records
        - incident_configuration_items: Incident CI links
        - problem_configuration_items: Problem CI links
        """
        valid_types = ["incidents", "problem_tickets", "work_notes", "attachments", 
                      "incident_reports", "work_orders", "incident_configuration_items", 
                      "problem_configuration_items"]
        
        if entity_type not in valid_types:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be one of: {', '.join(valid_types)}"
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
                    id_mapping = {
                        "incidents": "incident_id",
                        "problem_tickets": "problem_id",
                        "work_notes": "note_id",
                        "attachments": "attachment_id",
                        "incident_reports": "report_id",
                        "work_orders": "work_order_id",
                        "incident_configuration_items": "incident_ci_id",
                        "problem_configuration_items": "problem_ci_id"
                    }
                    id_field = id_mapping[entity_type]
                    results.append({**entity_data, id_field: entity_id})
            else:
                id_mapping = {
                    "incidents": "incident_id",
                    "problem_tickets": "problem_id",
                    "work_notes": "note_id",
                    "attachments": "attachment_id",
                    "incident_reports": "report_id",
                    "work_orders": "work_order_id",
                    "incident_configuration_items": "incident_ci_id",
                    "problem_configuration_items": "problem_ci_id"
                }
                id_field = id_mapping[entity_type]
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
                "name": "search_incident_tracking",
                "description": "Discover incident tracking entities (incidents, problem tickets, work notes, attachments, incident reports, work orders, incident configuration items, problem configuration items). The entity to discover is decided by entity_type. Optional filters can be applied to narrow down the search results.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'incidents', 'problem_tickets', 'work_notes', 'attachments', 'incident_reports', 'work_orders', 'incident_configuration_items', or 'problem_configuration_items'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters to narrow down search results. Only exact matches are supported (AND logic for multiple filters).",
                            "properties": {
                                "incident_id": {
                                    "type": "string",
                                    "description": "Incident ID"
                                },
                                "problem_id": {
                                    "type": "string",
                                    "description": "Problem ticket ID"
                                },
                                "incident_number": {
                                    "type": "string",
                                    "description": "Incident number, e.g., INC0012345 (for incidents)"
                                },
                                "problem_number": {
                                    "type": "string",
                                    "description": "Problem number, e.g., PRB0001234 (for problem_tickets)"
                                },
                                "title": {
                                    "type": "string",
                                    "description": "Title of the incident, problem, or work order"
                                },
                                "description": {
                                    "type": "string",
                                    "description": "Description text"
                                },
                                "category": {
                                    "type": "string",
                                    "description": "Category: 'inquiry/help', 'software', 'hardware', 'network', 'database' (for incidents and problem_tickets)"
                                },
                                "severity": {
                                    "type": "string",
                                    "description": "Severity level: 'P1', 'P2', 'P3', 'P4' (for incidents)"
                                },
                                "impact": {
                                    "type": "string",
                                    "description": "Impact level: 'critical', 'high', 'medium', 'low' (for incidents)"
                                },
                                "urgency": {
                                    "type": "string",
                                    "description": "Urgency level: 'critical', 'high', 'medium', 'low' (for incidents)"
                                },
                                "status": {
                                    "type": "string",
                                    "description": "Status of the entity"
                                },
                                "reported_by": {
                                    "type": "string",
                                    "description": "User ID who reported the incident or problem"
                                },
                                "assigned_to": {
                                    "type": "string",
                                    "description": "User ID assigned to the incident, problem, or work order"
                                },
                                "detection_time": {
                                    "type": "string",
                                    "description": "Detection timestamp in YYYY-MM-DD format (for incidents)"
                                },
                                "detected_at": {
                                    "type": "string",
                                    "description": "Detection timestamp in YYYY-MM-DD format (for problem_tickets)"
                                },
                                "acknowledged_at": {
                                    "type": "string",
                                    "description": "Acknowledgement timestamp in YYYY-MM-DD format (for incidents)"
                                },
                                "resolved_at": {
                                    "type": "string",
                                    "description": "Resolution timestamp in YYYY-MM-DD format (for incidents and problem_tickets)"
                                },
                                "closed_at": {
                                    "type": "string",
                                    "description": "Closure timestamp in YYYY-MM-DD format (for incidents and problem_tickets)"
                                },
                                "note_id": {
                                    "type": "string",
                                    "description": "Work note ID (for work_notes)"
                                },
                                "note_text": {
                                    "type": "string",
                                    "description": "Work note text content (for work_notes)"
                                },
                                "note_type": {
                                    "type": "string",
                                    "description": "Note type (for work_notes)"
                                },
                                "created_by": {
                                    "type": "string",
                                    "description": "User ID who created the note or entity"
                                },
                                "attachment_id": {
                                    "type": "string",
                                    "description": "Attachment ID (for attachments)"
                                },
                                "reference_id": {
                                    "type": "string",
                                    "description": "Reference ID of the parent record (for attachments)"
                                },
                                "reference_type": {
                                    "type": "string",
                                    "description": "Type of parent record: 'incident', 'change', 'rca', 'report', 'pir', 'communication', 'work_order', 'problem' (for attachments)"
                                },
                                "file_name": {
                                    "type": "string",
                                    "description": "File name (for attachments)"
                                },
                                "file_url": {
                                    "type": "string",
                                    "description": "File URL (for attachments)"
                                },
                                "file_type": {
                                    "type": "string",
                                    "description": "File type (for attachments)"
                                },
                                "file_size_bytes": {
                                    "type": "integer",
                                    "description": "File size in bytes (for attachments)"
                                },
                                "uploaded_by": {
                                    "type": "string",
                                    "description": "User ID who uploaded the file (for attachments)"
                                },
                                "uploaded_at": {
                                    "type": "string",
                                    "description": "Upload timestamp in YYYY-MM-DD format (for attachments)"
                                },
                                "report_id": {
                                    "type": "string",
                                    "description": "Report ID (for incident_reports)"
                                },
                                "report_number": {
                                    "type": "string",
                                    "description": "Report number, e.g., RPT0001234 (for incident_reports)"
                                },
                                "report_title": {
                                    "type": "string",
                                    "description": "Report title (for incident_reports)"
                                },
                                "report_type": {
                                    "type": "string",
                                    "description": "Report type: 'post_incident_review', 'client_impact', 'compliance' (for incident_reports)"
                                },
                                "report_content": {
                                    "type": "string",
                                    "description": "Report content (for incident_reports)"
                                },
                                "generated_by": {
                                    "type": "string",
                                    "description": "User ID who generated the report (for incident_reports)"
                                },
                                "generation_date": {
                                    "type": "string",
                                    "description": "Generation timestamp in YYYY-MM-DD format (for incident_reports)"
                                },
                                "report_status": {
                                    "type": "string",
                                    "description": "Report status: 'draft', 'completed', 'approved', 'archived' (for incident_reports)"
                                },
                                "work_order_id": {
                                    "type": "string",
                                    "description": "Work order ID (for work_orders)"
                                },
                                "work_order_number": {
                                    "type": "string",
                                    "description": "Work order number, e.g., WO0001234 (for work_orders)"
                                },
                                "change_id": {
                                    "type": "string",
                                    "description": "Associated change request ID (for work_orders)"
                                },
                                "scheduled_date": {
                                    "type": "string",
                                    "description": "Scheduled date in YYYY-MM-DD format (for work_orders)"
                                },
                                "completed_at": {
                                    "type": "string",
                                    "description": "Completion timestamp in YYYY-MM-DD format (for work_orders)"
                                },
                                "incident_ci_id": {
                                    "type": "string",
                                    "description": "Incident CI link ID (for incident_configuration_items)"
                                },
                                "problem_ci_id": {
                                    "type": "string",
                                    "description": "Problem CI link ID (for problem_configuration_items)"
                                },
                                "ci_id": {
                                    "type": "string",
                                    "description": "Configuration Item ID (for incident_configuration_items and problem_configuration_items)"
                                },
                                "created_at": {
                                    "type": "string",
                                    "description": "Creation timestamp in YYYY-MM-DD format"
                                },
                                "updated_at": {
                                    "type": "string",
                                    "description": "Update timestamp in YYYY-MM-DD format"
                                }
                            }
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
