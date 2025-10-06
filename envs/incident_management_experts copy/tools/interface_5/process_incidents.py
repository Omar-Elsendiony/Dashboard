import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ProcessIncidents(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, incident_data: Dict[str, Any] = None, incident_id: str = None) -> str:
        """
        Create or update incident records.
        
        Actions:
        - create: Create new incident record (requires incident_data with title, reporter_id, client_id, category, impact, detection_source, urgency, detected_at)
        - update: Update existing incident record (requires incident_id and incident_data with changes)
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
        
        # Access incidents data
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for incidents"
            })
        
        incidents = data.get("incidents", {})
        
        if action == "create":
            if not incident_data:
                return json.dumps({
                    "success": False,
                    "error": "incident_data is required for create action"
                })
            
            # Validate required fields for creation
            required_fields = ["title", "reporter_id", "client_id", "category", "impact", "detection_source", "urgency", "detected_at"]
            missing_fields = [field for field in required_fields if field not in incident_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields for incident creation: {', '.join(missing_fields)}"
                })
            
            # Validate only allowed fields are present (incident_code should NOT be in create)
            allowed_fields = ["title", "reporter_id", "assigned_manager_id", "client_id", "component_id", 
                            "severity", "status", "impact", "urgency", "category", "detection_source", "detected_at", 
                            "resolved_at", "closed_at", "rto_breach", "sla_breach", "is_recurring", "downtime_minutes"]
            invalid_fields = [field for field in incident_data.keys() if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for incident creation: {', '.join(invalid_fields)}"
                })
            
            # Validate enum fields (only if provided for optional fields)
            valid_severities = ["P1", "P2", "P3", "P4"]
            if "severity" in incident_data and incident_data["severity"] not in valid_severities:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid severity '{incident_data['severity']}'. Must be one of: {', '.join(valid_severities)}"
                })
            
            valid_statuses = ["open", "in_progress", "resolved", "closed"]
            if "status" in incident_data and incident_data["status"] not in valid_statuses:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid status '{incident_data['status']}'. Must be one of: {', '.join(valid_statuses)}"
                })
            
            valid_impacts = ["critical", "high", "medium", "low"]
            if incident_data["impact"] not in valid_impacts:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid impact '{incident_data['impact']}'. Must be one of: {', '.join(valid_impacts)}"
                })
            
            valid_urgencies = ["critical", "high", "medium", "low"]
            if incident_data["urgency"] not in valid_urgencies:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid urgency '{incident_data['urgency']}'. Must be one of: {', '.join(valid_urgencies)}"
                })
            
            valid_categories = ["system_outage", "performance_degradation", "security_incident", "data_corruption", 
                              "integration_failure", "network_issue", "hardware_failure", "software_bug", 
                              "configuration_error", "capacity_issue", "backup_failure", "authentication_failure", 
                              "api_error", "database_issue", "service_unavailable"]
            if incident_data["category"] not in valid_categories:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid category '{incident_data['category']}'. Must be one of: {', '.join(valid_categories)}"
                })
            
            valid_detection_sources = ["client_reported", "internally_detected", "monitoring_alert", "vendor_reported", 
                                     "scheduled_maintenance", "emergency_maintenance"]
            if incident_data["detection_source"] not in valid_detection_sources:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid detection_source '{incident_data['detection_source']}'. Must be one of: {', '.join(valid_detection_sources)}"
                })
            
            # Validate boolean fields if provided
            if "rto_breach" in incident_data and not isinstance(incident_data["rto_breach"], bool):
                return json.dumps({
                    "success": False,
                    "error": "rto_breach must be a boolean (True/False)"
                })
            
            if "sla_breach" in incident_data and not isinstance(incident_data["sla_breach"], bool):
                return json.dumps({
                    "success": False,
                    "error": "sla_breach must be a boolean (True/False)"
                })
            
            if "is_recurring" in incident_data and not isinstance(incident_data["is_recurring"], bool):
                return json.dumps({
                    "success": False,
                    "error": "is_recurring must be a boolean (True/False)"
                })
            
            # Validate downtime_minutes if provided
            if "downtime_minutes" in incident_data:
                downtime = incident_data["downtime_minutes"]
                if downtime is not None and (not isinstance(downtime, int) or downtime < 0):
                    return json.dumps({
                        "success": False,
                        "error": "downtime_minutes must be a non-negative integer"
                    })
            
            # Generate new incident ID
            new_incident_id = generate_id(incidents)
            
            # Auto-generate incident_code
            max_seq = 0
            for existing_incident in incidents.values():
                code = existing_incident.get("incident_code")
                if code and code.startswith("INC-2025-"):
                    try:
                        seq_num = int(code.split("INC-2025-")[1])
                        if seq_num > max_seq:
                            max_seq = seq_num
                    except Exception:
                        continue
            seq = max_seq + 1
            generated_code = f"INC-2025-{seq:05d}"

            new_incident = {
                "incident_id": str(new_incident_id),
                "incident_code": generated_code,
                "title": incident_data["title"],
                "reporter_id": str(incident_data["reporter_id"]),
                "assigned_manager_id": str(incident_data.get("assigned_manager_id")) if incident_data.get("assigned_manager_id") else None,
                "client_id": str(incident_data["client_id"]),
                "component_id": str(incident_data.get("component_id")) if incident_data.get("component_id") else None,
                "severity": incident_data.get("severity"),
                "status": incident_data.get("status", "open"),
                "impact": incident_data["impact"],
                "urgency": incident_data["urgency"],
                "category": incident_data["category"],
                "detection_source": incident_data["detection_source"],
                "detected_at": incident_data["detected_at"],
                "resolved_at": incident_data.get("resolved_at"),
                "closed_at": incident_data.get("closed_at"),
                "rto_breach": incident_data.get("rto_breach", False),
                "sla_breach": incident_data.get("sla_breach", False),
                "is_recurring": incident_data.get("is_recurring", False),
                "downtime_minutes": incident_data.get("downtime_minutes"),
                "created_at": "2025-10-01T00:00:00",
                "updated_at": "2025-10-01T00:00:00"
            }
            
            incidents[str(new_incident_id)] = new_incident
            
            return json.dumps({
                "success": True,
                "action": "create",
                "incident_id": str(new_incident_id),
                "incident_data": new_incident
            })
        
        elif action == "update":
            if not incident_id:
                return json.dumps({
                    "success": False,
                    "error": "incident_id is required for update action"
                })
            
            if incident_id not in incidents:
                return json.dumps({
                    "success": False,
                    "error": f"Incident record {incident_id} not found"
                })
            
            if not incident_data:
                return json.dumps({
                    "success": False,
                    "error": "incident_data is required for update action"
                })
            
            # Validate at least one field is provided for update
            if not incident_data:
                return json.dumps({
                    "success": False,
                    "error": "At least one field must be provided for update"
                })
            
            # Validate only allowed fields are present for updates
            allowed_update_fields = ["title", "incident_code", "assigned_manager_id", "component_id", "severity", "status", "impact", 
                                   "urgency", "category", "detection_source", "resolved_at", "closed_at", 
                                   "rto_breach", "sla_breach", "is_recurring", "downtime_minutes"]
            invalid_fields = [field for field in incident_data.keys() if field not in allowed_update_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for incident update: {', '.join(invalid_fields)}. Cannot update reporter_id, client_id, or detected_at."
                })
            
            # Validate incident_code uniqueness if provided
            if "incident_code" in incident_data and incident_data["incident_code"]:
                new_code = incident_data["incident_code"]
                for existing_id, existing in incidents.items():
                    if existing_id != incident_id and existing.get("incident_code") == new_code:
                        return json.dumps({
                            "success": False,
                            "error": f"Incident with code '{new_code}' already exists"
                        })
            
            # Validate enum fields if provided
            if "severity" in incident_data:
                valid_severities = ["P1", "P2", "P3", "P4"]
                if incident_data["severity"] not in valid_severities:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid severity '{incident_data['severity']}'. Must be one of: {', '.join(valid_severities)}"
                    })
            
            if "status" in incident_data:
                valid_statuses = ["open", "in_progress", "resolved", "closed"]
                if incident_data["status"] not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid status '{incident_data['status']}'. Must be one of: {', '.join(valid_statuses)}"
                    })
            
            if "impact" in incident_data:
                valid_impacts = ["critical", "high", "medium", "low"]
                if incident_data["impact"] not in valid_impacts:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid impact '{incident_data['impact']}'. Must be one of: {', '.join(valid_impacts)}"
                    })
            
            if "urgency" in incident_data:
                valid_urgencies = ["critical", "high", "medium", "low"]
                if incident_data["urgency"] not in valid_urgencies:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid urgency '{incident_data['urgency']}'. Must be one of: {', '.join(valid_urgencies)}"
                    })
            
            if "category" in incident_data:
                valid_categories = ["system_outage", "performance_degradation", "security_incident", "data_corruption", 
                                  "integration_failure", "network_issue", "hardware_failure", "software_bug", 
                                  "configuration_error", "capacity_issue", "backup_failure", "authentication_failure", 
                                  "api_error", "database_issue", "service_unavailable"]
                if incident_data["category"] not in valid_categories:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid category '{incident_data['category']}'. Must be one of: {', '.join(valid_categories)}"
                    })
            
            if "detection_source" in incident_data:
                valid_detection_sources = ["client_reported", "internally_detected", "monitoring_alert", "vendor_reported", 
                                         "scheduled_maintenance", "emergency_maintenance"]
                if incident_data["detection_source"] not in valid_detection_sources:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid detection_source '{incident_data['detection_source']}'. Must be one of: {', '.join(valid_detection_sources)}"
                    })
            
            # Validate boolean fields if provided
            if "rto_breach" in incident_data and not isinstance(incident_data["rto_breach"], bool):
                return json.dumps({
                    "success": False,
                    "error": "rto_breach must be a boolean (True/False)"
                })
            
            if "sla_breach" in incident_data and not isinstance(incident_data["sla_breach"], bool):
                return json.dumps({
                    "success": False,
                    "error": "sla_breach must be a boolean (True/False)"
                })
            
            if "is_recurring" in incident_data and not isinstance(incident_data["is_recurring"], bool):
                return json.dumps({
                    "success": False,
                    "error": "is_recurring must be a boolean (True/False)"
                })
            
            # Validate downtime_minutes if provided
            if "downtime_minutes" in incident_data:
                downtime = incident_data["downtime_minutes"]
                if downtime is not None and (not isinstance(downtime, int) or downtime < 0):
                    return json.dumps({
                        "success": False,
                        "error": "downtime_minutes must be a non-negative integer"
                    })
            
            # Get current incident data
            current_incident = incidents[incident_id].copy()
            
            # Validate status transitions
            current_status = current_incident.get("status")
            new_status = incident_data.get("status")
            
            if new_status and current_status == "closed" and new_status != "closed":
                return json.dumps({
                    "success": False,
                    "error": "Cannot reopen a closed incident"
                })
            
            # Auto-set resolved_at when status changes to resolved
            if new_status == "resolved" and current_status != "resolved" and "resolved_at" not in incident_data:
                incident_data["resolved_at"] = "2025-10-01T00:00:00"
            
            # Auto-set closed_at when status changes to closed
            if new_status == "closed" and current_status != "closed" and "closed_at" not in incident_data:
                incident_data["closed_at"] = "2025-10-01T00:00:00"
            
            # Update incident record
            updated_incident = current_incident.copy()
            for key, value in incident_data.items():
                if key in ["assigned_manager_id", "component_id"] and value is not None:
                    updated_incident[key] = str(value)
                else:
                    updated_incident[key] = value
            
            updated_incident["updated_at"] = "2025-10-01T00:00:00"
            incidents[incident_id] = updated_incident
            
            return json.dumps({
                "success": True,
                "action": "update",
                "incident_id": str(incident_id),
                "incident_data": updated_incident
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "process_incidents",
                "description": "Create or update incident records in the incident management system. This tool manages the complete incident lifecycle from initial reporting through resolution and closure. For creation, establishes new incident records with auto-generated incident codes and comprehensive validation to ensure proper categorization, severity assessment, and tracking information. For updates, modifies existing incident records while maintaining data integrity and enforcing proper status transitions. Use update action to resolve (set status='resolved') or close (set status='closed') incidents. Essential for incident tracking, SLA compliance monitoring, and operational reporting.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' to establish new incident record with auto-generated incident_code, 'update' to modify existing incident record (including resolving or closing)",
                            "enum": ["create", "update"]
                        },
                        "incident_data": {
                            "type": "object",
                            "description": "Incident data object. For create: requires title, reporter_id, client_id, category, impact, detection_source, urgency, detected_at, with optional assigned_manager_id, component_id, severity, status, is_recurring, downtime_minutes, sla_breach, rto_breach, closed_at, resolved_at. incident_code is auto-generated. For update: requires at least one field from title, incident_code, assigned_manager_id, component_id, severity, status, impact, urgency, category, detection_source, resolved_at, closed_at, rto_breach, sla_breach, is_recurring, downtime_minutes. Cannot update reporter_id, client_id, or detected_at. SYNTAX: {\"key\": \"value\"}",
                            "properties": {
                                "title": {
                                    "type": "string",
                                    "description": "Brief description of the incident (required for create)"
                                },
                                "reporter_id": {
                                    "type": "string",
                                    "description": "User ID who reported the incident (required for create only, cannot be updated)"
                                },
                                "assigned_manager_id": {
                                    "type": "string",
                                    "description": "User ID of assigned incident manager (optional)"
                                },
                                "client_id": {
                                    "type": "string",
                                    "description": "Client affected by the incident (required for create only, cannot be updated)"
                                },
                                "component_id": {
                                    "type": "string",
                                    "description": "Infrastructure component involved in the incident (optional)"
                                },
                                "severity": {
                                    "type": "string",
                                    "description": "Incident severity level: 'P1', 'P2', 'P3', 'P4' (optional)",
                                    "enum": ["P1", "P2", "P3", "P4"]
                                },
                                "status": {
                                    "type": "string",
                                    "description": "Current incident status: 'open', 'in_progress', 'resolved', 'closed' (optional, defaults to 'open' on create. Closed incidents cannot be reopened)",
                                    "enum": ["open", "in_progress", "resolved", "closed"]
                                },
                                "impact": {
                                    "type": "string",
                                    "description": "Business impact level: 'critical', 'high', 'medium', 'low' (required for create)",
                                    "enum": ["critical", "high", "medium", "low"]
                                },
                                "urgency": {
                                    "type": "string",
                                    "description": "Business urgency level: 'critical', 'high', 'medium', 'low' (required for create)",
                                    "enum": ["critical", "high", "medium", "low"]
                                },
                                "category": {
                                    "type": "string",
                                    "description": "Technical incident category: 'system_outage', 'performance_degradation', 'security_incident', 'data_corruption', 'integration_failure', 'network_issue', 'hardware_failure', 'software_bug', 'configuration_error', 'capacity_issue', 'backup_failure', 'authentication_failure', 'api_error', 'database_issue', 'service_unavailable' (required for create)",
                                    "enum": ["system_outage", "performance_degradation", "security_incident", "data_corruption", "integration_failure", "network_issue", "hardware_failure", "software_bug", "configuration_error", "capacity_issue", "backup_failure", "authentication_failure", "api_error", "database_issue", "service_unavailable"]
                                },
                                "detection_source": {
                                    "type": "string",
                                    "description": "How the incident was detected: 'client_reported', 'internally_detected', 'monitoring_alert', 'vendor_reported', 'scheduled_maintenance', 'emergency_maintenance' (required for create)",
                                    "enum": ["client_reported", "internally_detected", "monitoring_alert", "vendor_reported", "scheduled_maintenance", "emergency_maintenance"]
                                },
                                "detected_at": {
                                    "type": "string",
                                    "description": "Timestamp when incident was detected (required for create only, cannot be updated)"
                                },
                                "resolved_at": {
                                    "type": "string",
                                    "description": "Timestamp when incident was resolved (optional, auto-set when status changes to 'resolved')"
                                },
                                "closed_at": {
                                    "type": "string",
                                    "description": "Timestamp when incident was closed (optional, auto-set when status changes to 'closed')"
                                },
                                "incident_code": {
                                    "type": "string",
                                    "description": "Unique incident identifier code (auto-generated on create, can be updated)"
                                },
                                "rto_breach": {
                                    "type": "boolean",
                                    "description": "Whether Recovery Time Objective was breached (True/False, optional, defaults to False)"
                                },
                                "sla_breach": {
                                    "type": "boolean",
                                    "description": "Whether Service Level Agreement was breached (True/False, optional, defaults to False)"
                                },
                                "is_recurring": {
                                    "type": "boolean",
                                    "description": "Whether this is a recurring incident (True/False, optional, defaults to False)"
                                },
                                "downtime_minutes": {
                                    "type": "integer",
                                    "description": "Total downtime in minutes (non-negative integer, optional)"
                                }
                            }
                        },
                        "incident_id": {
                            "type": "string",
                            "description": "Unique identifier of the incident record (required for update action only)"
                        }
                    },
                    "required": ["action"]
                }
            }
        }