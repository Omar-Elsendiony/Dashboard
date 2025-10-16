#!/bin/bash

# Create discover_parties.py
cat > discover_parties.py << 'EOF'
import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class DiscoverParties(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover party entities (clients, vendors, users). The entity to discover is decided by entity_type.
        Optionally, filters can be applied to narrow down the search results.
        
        Supported entities:
        - clients: Client records
        - vendors: Vendor records
        - users: User records
        """
        if entity_type not in ["clients", "vendors", "users"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'clients', 'vendors', or 'users'"
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
                    if entity_type == "clients":
                        id_field = "client_id"
                    elif entity_type == "vendors":
                        id_field = "vendor_id"
                    else:  # users
                        id_field = "user_id"
                        # Remove role field from user data
                        entity_data = {k: v for k, v in entity_data.items() if k != "role"}
                    results.append({**entity_data, id_field: entity_id})
            else:
                if entity_type == "clients":
                    id_field = "client_id"
                elif entity_type == "vendors":
                    id_field = "vendor_id"
                else:  # users
                    id_field = "user_id"
                    # Remove role field from user data
                    entity_data = {k: v for k, v in entity_data.items() if k != "role"}
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
                "name": "discover_parties",
                "description": "Discover party entities (clients, vendors, users). The entity to discover is decided by entity_type. Optional filters can be applied to narrow down the search results.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'clients', 'vendors', or 'users'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters to narrow down search results. Only exact matches are supported (AND logic for multiple filters).",
                            "properties": {
                                "client_id": {
                                    "type": "string",
                                    "description": "Client ID (for clients)"
                                },
                                "client_name": {
                                    "type": "string",
                                    "description": "Client name (for clients)"
                                },
                                "registration_number": {
                                    "type": "string",
                                    "description": "Registration number (for clients)"
                                },
                                "company_type": {
                                    "type": "string",
                                    "description": "Company type: 'enterprise', 'mid_market', 'smb', 'startup' (for clients)"
                                },
                                "address": {
                                    "type": "string",
                                    "description": "Client address (for clients)"
                                },
                                "contact_phone": {
                                    "type": "string",
                                    "description": "Contact phone number"
                                },
                                "contact_email": {
                                    "type": "string",
                                    "description": "Contact email address"
                                },
                                "support_coverage": {
                                    "type": "string",
                                    "description": "Support coverage: '24x7', 'business_hours', 'on_call' (for clients)"
                                },
                                "preferred_communication": {
                                    "type": "string",
                                    "description": "Preferred communication method: 'email', 'portal', 'phone', 'slack' (for clients)"
                                },
                                "status": {
                                    "type": "string",
                                    "description": "Status of the entity"
                                },
                                "vendor_id": {
                                    "type": "string",
                                    "description": "Vendor ID (for vendors)"
                                },
                                "vendor_name": {
                                    "type": "string",
                                    "description": "Vendor name (for vendors)"
                                },
                                "user_id": {
                                    "type": "string",
                                    "description": "User ID (for users)"
                                },
                                "first_name": {
                                    "type": "string",
                                    "description": "User first name (for users)"
                                },
                                "last_name": {
                                    "type": "string",
                                    "description": "User last name (for users)"
                                },
                                "email": {
                                    "type": "string",
                                    "description": "User email address (for users)"
                                },
                                "timezone": {
                                    "type": "string",
                                    "description": "User timezone (for users)"
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
EOF

echo "✓ Created discover_parties.py"

# Create discover_assets.py
cat > discover_assets.py << 'EOF'
import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class DiscoverAssets(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover asset entities (products, configuration_items). The entity to discover is decided by entity_type.
        Optionally, filters can be applied to narrow down the search results.
        
        Supported entities:
        - products: Product records
        - configuration_items: Configuration Item (CI) records
        """
        if entity_type not in ["products", "configuration_items"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'products' or 'configuration_items'"
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
                    if entity_type == "products":
                        id_field = "product_id"
                    else:  # configuration_items
                        id_field = "ci_id"
                    results.append({**entity_data, id_field: entity_id})
            else:
                if entity_type == "products":
                    id_field = "product_id"
                else:  # configuration_items
                    id_field = "ci_id"
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
                "name": "discover_assets",
                "description": "Discover asset entities (products, configuration items). The entity to discover is decided by entity_type. Optional filters can be applied to narrow down the search results.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'products' or 'configuration_items'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters to narrow down search results. Only exact matches are supported (AND logic for multiple filters).",
                            "properties": {
                                "product_id": {
                                    "type": "string",
                                    "description": "Product ID (for products)"
                                },
                                "product_name": {
                                    "type": "string",
                                    "description": "Product name (for products)"
                                },
                                "product_code": {
                                    "type": "string",
                                    "description": "Product code (for products)"
                                },
                                "description": {
                                    "type": "string",
                                    "description": "Product description (for products)"
                                },
                                "status": {
                                    "type": "string",
                                    "description": "Status: 'active', 'deprecated', 'retired' (for products)"
                                },
                                "ci_id": {
                                    "type": "string",
                                    "description": "Configuration Item ID (for configuration_items)"
                                },
                                "ci_name": {
                                    "type": "string",
                                    "description": "Configuration Item name (for configuration_items)"
                                },
                                "ci_type": {
                                    "type": "string",
                                    "description": "CI type: 'server', 'application', 'database', 'network', 'storage', 'service' (for configuration_items)"
                                },
                                "environment": {
                                    "type": "string",
                                    "description": "Environment: 'production', 'staging', 'development', 'testing' (for configuration_items)"
                                },
                                "location": {
                                    "type": "string",
                                    "description": "Physical or logical location (for configuration_items)"
                                },
                                "operational_status": {
                                    "type": "string",
                                    "description": "Operational status: 'operational', 'degraded', 'down', 'maintenance' (for configuration_items)"
                                },
                                "created_at": {
                                    "type": "string",
                                    "description": "Creation timestamp in YYYY-MM-DD format"
                                },
                                "updated_at": {
                                    "type": "string",
                                    "description": "Update timestamp in YYYY-MM-DD format (for configuration_items)"
                                }
                            }
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
EOF

echo "✓ Created discover_assets.py"

# Create discover_contracts.py
cat > discover_contracts.py << 'EOF'
import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class DiscoverContracts(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover contract entities (subscriptions, sla_agreements). The entity to discover is decided by entity_type.
        Optionally, filters can be applied to narrow down the search results.
        
        Supported entities:
        - subscriptions: Subscription records
        - sla_agreements: SLA Agreement records
        """
        if entity_type not in ["subscriptions", "sla_agreements"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'subscriptions' or 'sla_agreements'"
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
                    if entity_type == "subscriptions":
                        id_field = "subscription_id"
                    else:  # sla_agreements
                        id_field = "sla_id"
                    results.append({**entity_data, id_field: entity_id})
            else:
                if entity_type == "subscriptions":
                    id_field = "subscription_id"
                else:  # sla_agreements
                    id_field = "sla_id"
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
                "name": "discover_contracts",
                "description": "Discover contract entities (subscriptions, SLA agreements). The entity to discover is decided by entity_type. Optional filters can be applied to narrow down the search results.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'subscriptions' or 'sla_agreements'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters to narrow down search results. Only exact matches are supported (AND logic for multiple filters).",
                            "properties": {
                                "subscription_id": {
                                    "type": "string",
                                    "description": "Subscription ID (for subscriptions)"
                                },
                                "client_id": {
                                    "type": "string",
                                    "description": "Client ID (for subscriptions)"
                                },
                                "tier": {
                                    "type": "string",
                                    "description": "Subscription tier: 'premium', 'standard', 'basic' (for subscriptions)"
                                },
                                "start_date": {
                                    "type": "string",
                                    "description": "Start date in YYYY-MM-DD format (for subscriptions)"
                                },
                                "end_date": {
                                    "type": "string",
                                    "description": "End date in YYYY-MM-DD format (for subscriptions)"
                                },
                                "status": {
                                    "type": "string",
                                    "description": "Status: 'active', 'expired', 'cancelled' (for subscriptions)"
                                },
                                "sla_id": {
                                    "type": "string",
                                    "description": "SLA agreement ID (for sla_agreements)"
                                },
                                "severity_level": {
                                    "type": "string",
                                    "description": "Severity level: 'P1', 'P2', 'P3', 'P4' (for sla_agreements)"
                                },
                                "response_time_minutes": {
                                    "type": "integer",
                                    "description": "Response time in minutes (for sla_agreements)"
                                },
                                "resolution_time_minutes": {
                                    "type": "integer",
                                    "description": "Resolution time in minutes (for sla_agreements)"
                                },
                                "availability_guarantee": {
                                    "type": "number",
                                    "description": "Availability guarantee percentage, e.g., 99.9 (for sla_agreements)"
                                },
                                "created_by": {
                                    "type": "string",
                                    "description": "User ID who created the SLA (for sla_agreements)"
                                },
                                "created_at": {
                                    "type": "string",
                                    "description": "Creation timestamp in YYYY-MM-DD format"
                                },
                                "updated_at": {
                                    "type": "string",
                                    "description": "Update timestamp in YYYY-MM-DD format (for subscriptions)"
                                }
                            }
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
EOF

echo "✓ Created discover_contracts.py"

# Create discover_incident_tracking.py
cat > discover_incident_tracking.py << 'EOF'
import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class DiscoverIncidentTracking(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover incident tracking entities (incidents, problem_tickets, work_notes, attachments, incident_reports, work_orders). 
        The entity to discover is decided by entity_type. Optionally, filters can be applied to narrow down the search results.
        
        Supported entities:
        - incidents: Incident records
        - problem_tickets: Problem Ticket records
        - work_notes: Work Note records
        - attachments: Attachment records
        - incident_reports: Incident Report records
        - work_orders: Work Order records
        """
        if entity_type not in ["incidents", "problem_tickets", "work_notes", "attachments", "incident_reports", "work_orders"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be one of: 'incidents', 'problem_tickets', 'work_notes', 'attachments', 'incident_reports', 'work_orders'"
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
                    if entity_type == "incidents":
                        id_field = "incident_id"
                    elif entity_type == "problem_tickets":
                        id_field = "problem_id"
                    elif entity_type == "work_notes":
                        id_field = "note_id"
                    elif entity_type == "attachments":
                        id_field = "attachment_id"
                    elif entity_type == "incident_reports":
                        id_field = "report_id"
                    else:  # work_orders
                        id_field = "work_order_id"
                    results.append({**entity_data, id_field: entity_id})
            else:
                if entity_type == "incidents":
                    id_field = "incident_id"
                elif entity_type == "problem_tickets":
                    id_field = "problem_id"
                elif entity_type == "work_notes":
                    id_field = "note_id"
                elif entity_type == "attachments":
                    id_field = "attachment_id"
                elif entity_type == "incident_reports":
                    id_field = "report_id"
                else:  # work_orders
                    id_field = "work_order_id"
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
                "description": "Discover incident tracking entities (incidents, problem tickets, work notes, attachments, incident reports, work orders). The entity to discover is decided by entity_type. Optional filters can be applied to narrow down the search results.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'incidents', 'problem_tickets', 'work_notes', 'attachments', 'incident_reports', or 'work_orders'"
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
                                    "description": "Category: 'inquiry/help', 'software', 'hardware', 'Network', 'Database' (for incidents)"
                                },
                                "client_id": {
                                    "type": "string",
                                    "description": "Client ID"
                                },
                                "affected_ci_id": {
                                    "type": "string",
                                    "description": "Affected Configuration Item ID (for incidents)"
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
                                    "description": "User ID assigned to the incident or work order"
                                },
                                "detection_time": {
                                    "type": "string",
                                    "description": "Detection timestamp in YYYY-MM-DD format (for incidents)"
                                },
                                "acknowledged_at": {
                                    "type": "string",
                                    "description": "Acknowledgement timestamp in YYYY-MM-DD format (for incidents)"
                                },
                                "resolved_at": {
                                    "type": "string",
                                    "description": "Resolution timestamp in YYYY-MM-DD format (for incidents)"
                                },
                                "closed_at": {
                                    "type": "string",
                                    "description": "Closure timestamp in YYYY-MM-DD format (for incidents)"
                                },
                                "note_id": {
                                    "type": "string",
                                    "description": "Work note ID (for work_notes)"
                                },
                                "note_text": {
                                    "type": "string",
                                    "description": "Work note text content (for work_notes)"
                                },
                                "created_by": {
                                    "type": "string",
                                    "description": "User ID who created the note (for work_notes)"
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
EOF

echo "✓ Created discover_incident_tracking.py"

# Create discover_coordination.py
cat > discover_coordination.py << 'EOF'
import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class DiscoverCoordination(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover coordination entities (escalations, bridges, bridge_participants). The entity to discover is decided by entity_type.
        Optionally, filters can be applied to narrow down the search results.
        
        Supported entities:
        - escalations: Escalation records
        - bridges: Bridge records
        - bridge_participants: Bridge Participant records
        """
        if entity_type not in ["escalations", "bridges", "bridge_participants"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'escalations', 'bridges', or 'bridge_participants'"
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
                    if entity_type == "escalations":
                        id_field = "escalation_id"
                    elif entity_type == "bridges":
                        id_field = "bridge_id"
                    else:  # bridge_participants
                        id_field = "participant_id"
                    results.append({**entity_data, id_field: entity_id})
            else:
                if entity_type == "escalations":
                    id_field = "escalation_id"
                elif entity_type == "bridges":
                    id_field = "bridge_id"
                else:  # bridge_participants
                    id_field = "participant_id"
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
                "name": "discover_coordination",
                "description": "Discover coordination entities (escalations, bridges, bridge participants). The entity to discover is decided by entity_type. Optional filters can be applied to narrow down the search results.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'escalations', 'bridges', or 'bridge_participants'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters to narrow down search results. Only exact matches are supported (AND logic for multiple filters).",
                            "properties": {
                                "escalation_id": {
                                    "type": "string",
                                    "description": "Escalation ID (for escalations)"
                                },
                                "incident_id": {
                                    "type": "string",
                                    "description": "Associated incident ID"
                                },
                                "escalated_from": {
                                    "type": "string",
                                    "description": "User ID who requested escalation (for escalations)"
                                },
                                "escalated_to": {
                                    "type": "string",
                                    "description": "User ID receiving escalation (for escalations)"
                                },
                                "escalation_level": {
                                    "type": "string",
                                    "description": "Escalation level: 'L1_to_L2', 'L2_to_L3', 'L3_to_management', 'management_to_executive' (for escalations)"
                                },
                                "escalation_reason": {
                                    "type": "string",
                                    "description": "Reason for escalation (for escalations)"
                                },
                                "status": {
                                    "type": "string",
                                    "description": "Status of the escalation or bridge"
                                },
                                "requested_at": {
                                    "type": "string",
                                    "description": "Request timestamp in YYYY-MM-DD format (for escalations)"
                                },
                                "responded_at": {
                                    "type": "string",
                                    "description": "Response timestamp in YYYY-MM-DD format (for escalations)"
                                },
                                "bridge_id": {
                                    "type": "string",
                                    "description": "Bridge ID"
                                },
                                "bridge_number": {
                                    "type": "string",
                                    "description": "Bridge number, e.g., BRG0001234 (for bridges)"
                                },
                                "bridge_type": {
                                    "type": "string",
                                    "description": "Bridge type: 'major_incident', 'coordination', 'technical' (for bridges)"
                                },
                                "bridge_host": {
                                    "type": "string",
                                    "description": "User ID hosting the bridge (for bridges)"
                                },
                                "start_time": {
                                    "type": "string",
                                    "description": "Start timestamp in YYYY-MM-DD format (for bridges)"
                                },
                                "end_time": {
                                    "type": "string",
                                    "description": "End timestamp in YYYY-MM-DD format (for bridges)"
                                },
                                "participant_id": {
                                    "type": "string",
                                    "description": "Participant ID (for bridge_participants)"
                                },
                                "user_id": {
                                    "type": "string",
                                    "description": "User ID of the participant (for bridge_participants)"
                                },
                                "role_in_bridge": {
                                    "type": "string",
                                    "description": "Role in bridge: 'host', 'technical_support', 'account_manager', 'vendor', 'executive' (for bridge_participants)"
                                },
                                "joined_at": {
                                    "type": "string",
                                    "description": "Join timestamp in YYYY-MM-DD format (for bridge_participants)"
                                },
                                "created_at": {
                                    "type": "string",
                                    "description": "Creation timestamp in YYYY-MM-DD format"
                                }
                            }
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
EOF

echo "✓ Created discover_coordination.py"

echo ""
echo "All discovery tool files have been created successfully!"
echo ""
echo "Files created:"
echo "  - discover_parties.py (clients, vendors, users - without user role field)"
echo "  - discover_assets.py (products, configuration_items)"
echo "  - discover_contracts.py (subscriptions, sla_agreements)"
echo "  - discover_incident_tracking.py (incidents, problem_tickets, work_notes, attachments, incident_reports, work_orders)"
