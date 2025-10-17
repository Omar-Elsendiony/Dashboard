#!/bin/bash

# Create discover_change_control.py
cat > discover_change_control.py << 'EOF'
import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class DiscoverChangeControl(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover change control entities (change_requests, rollback_requests). The entity to discover is decided by entity_type.
        Optionally, filters can be applied to narrow down the search results.
        
        Supported entities:
        - change_requests: Change Request records
        - rollback_requests: Rollback Request records
        """
        if entity_type not in ["change_requests", "rollback_requests"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'change_requests' or 'rollback_requests'"
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
                    if entity_type == "change_requests":
                        id_field = "change_id"
                    else:  # rollback_requests
                        id_field = "rollback_id"
                    results.append({**entity_data, id_field: entity_id})
            else:
                if entity_type == "change_requests":
                    id_field = "change_id"
                else:  # rollback_requests
                    id_field = "rollback_id"
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
                "name": "discover_change_control",
                "description": "Discover change control entities (change requests, rollback requests). The entity to discover is decided by entity_type. Optional filters can be applied to narrow down the search results.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'change_requests' or 'rollback_requests'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters to narrow down search results. Only exact matches are supported (AND logic for multiple filters).",
                            "properties": {
                                "change_id": {
                                    "type": "string",
                                    "description": "Change request ID (for change_requests)"
                                },
                                "change_number": {
                                    "type": "string",
                                    "description": "Change request number, e.g., CHG0001234 (for change_requests)"
                                },
                                "incident_id": {
                                    "type": "string",
                                    "description": "Associated incident ID"
                                },
                                "title": {
                                    "type": "string",
                                    "description": "Change/rollback title"
                                },
                                "description": {
                                    "type": "string",
                                    "description": "Change description (for change_requests)"
                                },
                                "change_type": {
                                    "type": "string",
                                    "description": "Type of change: 'standard', 'normal', 'emergency' (for change_requests)"
                                },
                                "risk_level": {
                                    "type": "string",
                                    "description": "Risk level of change: 'low', 'medium', 'high', 'critical' (for change_requests)"
                                },
                                "requested_by": {
                                    "type": "string",
                                    "description": "User ID who requested the change/rollback"
                                },
                                "approved_by": {
                                    "type": "string",
                                    "description": "User ID who approved the change (for change_requests)"
                                },
                                "status": {
                                    "type": "string",
                                    "description": "Status of the change/rollback"
                                },
                                "implementation_date": {
                                    "type": "string",
                                    "description": "Implementation date in YYYY-MM-DD format (for change_requests)"
                                },
                                "rollback_id": {
                                    "type": "string",
                                    "description": "Rollback request ID (for rollback_requests)"
                                },
                                "rollback_number": {
                                    "type": "string",
                                    "description": "Rollback request number, e.g., RBK0001234 (for rollback_requests)"
                                },
                                "rollback_reason": {
                                    "type": "string",
                                    "description": "Reason for rollback (for rollback_requests)"
                                },
                                "executed_at": {
                                    "type": "string",
                                    "description": "Execution timestamp in YYYY-MM-DD format (for rollback_requests)"
                                },
                                "created_at": {
                                    "type": "string",
                                    "description": "Creation timestamp in YYYY-MM-DD format"
                                },
                                "updated_at": {
                                    "type": "string",
                                    "description": "Update timestamp in YYYY-MM-DD format (for change_requests)"
                                }
                            }
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
EOF

echo "✓ Created discover_change_control.py"

# Create discover_workflows.py
cat > discover_workflows.py << 'EOF'
import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class DiscoverWorkflows(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover workflow entities (communications, approval_requests). The entity to discover is decided by entity_type.
        Optionally, filters can be applied to narrow down the search results.
        
        Supported entities:
        - communications: Communication records
        - approval_requests: Approval Request records
        """
        if entity_type not in ["communications", "approval_requests"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'communications' or 'approval_requests'"
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
                    if entity_type == "communications":
                        id_field = "communication_id"
                    else:  # approval_requests
                        id_field = "approval_id"
                    results.append({**entity_data, id_field: entity_id})
            else:
                if entity_type == "communications":
                    id_field = "communication_id"
                else:  # approval_requests
                    id_field = "approval_id"
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
                "name": "discover_workflows",
                "description": "Discover workflow entities (communications, approval requests). The entity to discover is decided by entity_type. Optional filters can be applied to narrow down the search results.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'communications' or 'approval_requests'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters to narrow down search results. Only exact matches are supported (AND logic for multiple filters).",
                            "properties": {
                                "communication_id": {
                                    "type": "string",
                                    "description": "Communication ID (for communications)"
                                },
                                "incident_id": {
                                    "type": "string",
                                    "description": "Associated incident ID"
                                },
                                "communication_type": {
                                    "type": "string",
                                    "description": "Type of communication: 'status_update', 'resolution_notice', 'escalation_notice', 'bridge_invitation' (for communications)"
                                },
                                "recipient_type": {
                                    "type": "string",
                                    "description": "Type of recipient: 'client', 'internal', 'vendor', 'executive' (for communications)"
                                },
                                "sender": {
                                    "type": "string",
                                    "description": "User ID of sender (for communications)"
                                },
                                "recipient": {
                                    "type": "string",
                                    "description": "User ID of recipient (for communications)"
                                },
                                "delivery_method": {
                                    "type": "string",
                                    "description": "Delivery method: 'email', 'portal', 'sms', 'phone' (for communications)"
                                },
                                "message_content": {
                                    "type": "string",
                                    "description": "Message content (for communications)"
                                },
                                "delivery_status": {
                                    "type": "string",
                                    "description": "Delivery status: 'pending', 'sent', 'delivered', 'failed' (for communications)"
                                },
                                "sent_at": {
                                    "type": "string",
                                    "description": "Sent timestamp in YYYY-MM-DD format (for communications)"
                                },
                                "approval_id": {
                                    "type": "string",
                                    "description": "Approval request ID (for approval_requests)"
                                },
                                "reference_id": {
                                    "type": "string",
                                    "description": "ID of the record requiring approval (for approval_requests)"
                                },
                                "reference_type": {
                                    "type": "string",
                                    "description": "Type of record requiring approval: 'escalation', 'bridge', 'change', 'rollback', 'incident_closure', 'rca' (for approval_requests)"
                                },
                                "requested_by": {
                                    "type": "string",
                                    "description": "User ID who requested approval (for approval_requests)"
                                },
                                "requested_action": {
                                    "type": "string",
                                    "description": "Action being requested (for approval_requests)"
                                },
                                "approver": {
                                    "type": "string",
                                    "description": "User ID of approver (for approval_requests)"
                                },
                                "status": {
                                    "type": "string",
                                    "description": "Approval status: 'pending', 'approved', 'denied' (for approval_requests)"
                                },
                                "requested_at": {
                                    "type": "string",
                                    "description": "Request timestamp in YYYY-MM-DD format (for approval_requests)"
                                },
                                "responded_at": {
                                    "type": "string",
                                    "description": "Response timestamp in YYYY-MM-DD format (for approval_requests)"
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

echo "✓ Created discover_workflows.py"

# Create discover_performance.py
cat > discover_performance.py << 'EOF'
import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class DiscoverPerformance(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover performance entities (performance_metrics). The entity to discover is decided by entity_type.
        Optionally, filters can be applied to narrow down the search results.
        
        Supported entities:
        - performance_metrics: Performance Metric records
        """
        if entity_type not in ["performance_metrics"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'performance_metrics'"
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
                    results.append({**entity_data, "metric_id": entity_id})
            else:
                results.append({**entity_data, "metric_id": entity_id})
        
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
                "name": "discover_performance",
                "description": "Discover performance entities (performance metrics). The entity to discover is decided by entity_type. Optional filters can be applied to narrow down the search results.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'performance_metrics'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters to narrow down search results. Only exact matches are supported (AND logic for multiple filters).",
                            "properties": {
                                "metric_id": {
                                    "type": "string",
                                    "description": "Performance metric ID"
                                },
                                "incident_id": {
                                    "type": "string",
                                    "description": "Associated incident ID"
                                },
                                "metric_type": {
                                    "type": "string",
                                    "description": "Type of metric: 'MTTA', 'MTTD', 'MTTR', 'MTTM', 'FTR'"
                                },
                                "calculated_value_minutes": {
                                    "type": "integer",
                                    "description": "Calculated value in minutes"
                                },
                                "sla_target_minutes": {
                                    "type": "integer",
                                    "description": "SLA target in minutes"
                                },
                                "recorded_by": {
                                    "type": "string",
                                    "description": "User ID who recorded the metric"
                                },
                                "recorded_date": {
                                    "type": "string",
                                    "description": "Recording timestamp in YYYY-MM-DD format"
                                }
                            }
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
EOF

echo "✓ Created discover_performance.py"

# Create discover_improvement.py
cat > discover_improvement.py << 'EOF'
import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class DiscoverImprovement(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover improvement entities (root_cause_analyses, post_incident_reviews). The entity to discover is decided by entity_type.
        Optionally, filters can be applied to narrow down the search results.
        
        Supported entities:
        - root_cause_analyses: Root Cause Analysis records
        - post_incident_reviews: Post Incident Review records
        """
        if entity_type not in ["root_cause_analyses", "post_incident_reviews"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'root_cause_analyses' or 'post_incident_reviews'"
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
                    if entity_type == "root_cause_analyses":
                        id_field = "rca_id"
                    else:  # post_incident_reviews
                        id_field = "review_id"
                    results.append({**entity_data, id_field: entity_id})
            else:
                if entity_type == "root_cause_analyses":
                    id_field = "rca_id"
                else:  # post_incident_reviews
                    id_field = "review_id"
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
                "name": "discover_improvement",
                "description": "Discover improvement entities (root cause analyses, post incident reviews). The entity to discover is decided by entity_type. Optional filters can be applied to narrow down the search results.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'root_cause_analyses' or 'post_incident_reviews'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters to narrow down search results. Only exact matches are supported (AND logic for multiple filters).",
                            "properties": {
                                "rca_id": {
                                    "type": "string",
                                    "description": "Root cause analysis ID (for root_cause_analyses)"
                                },
                                "rca_number": {
                                    "type": "string",
                                    "description": "RCA number, e.g., RCA0001234 (for root_cause_analyses)"
                                },
                                "rca_title": {
                                    "type": "string",
                                    "description": "RCA title (for root_cause_analyses)"
                                },
                                "incident_id": {
                                    "type": "string",
                                    "description": "Associated incident ID"
                                },
                                "assigned_to": {
                                    "type": "string",
                                    "description": "User ID assigned to the RCA (for root_cause_analyses)"
                                },
                                "analysis_method": {
                                    "type": "string",
                                    "description": "Analysis method: '5_whys', 'fishbone', 'timeline', 'fault_tree', 'kepner_tregoe' (for root_cause_analyses)"
                                },
                                "root_cause_summary": {
                                    "type": "string",
                                    "description": "Summary of root cause findings (for root_cause_analyses)"
                                },
                                "status": {
                                    "type": "string",
                                    "description": "Status of RCA or review"
                                },
                                "due_date": {
                                    "type": "string",
                                    "description": "Due date in YYYY-MM-DD format (for root_cause_analyses)"
                                },
                                "completed_at": {
                                    "type": "string",
                                    "description": "Completion timestamp in YYYY-MM-DD format (for root_cause_analyses)"
                                },
                                "approved_by": {
                                    "type": "string",
                                    "description": "User ID who approved the RCA (for root_cause_analyses)"
                                },
                                "review_id": {
                                    "type": "string",
                                    "description": "Post incident review ID (for post_incident_reviews)"
                                },
                                "scheduled_date": {
                                    "type": "string",
                                    "description": "Scheduled date in YYYY-MM-DD format (for post_incident_reviews)"
                                },
                                "facilitator": {
                                    "type": "string",
                                    "description": "User ID of facilitator (for post_incident_reviews)"
                                },
                                "review_notes": {
                                    "type": "string",
                                    "description": "Notes from the review (for post_incident_reviews)"
                                },
                                "lessons_learned": {
                                    "type": "string",
                                    "description": "Lessons learned (for post_incident_reviews)"
                                },
                                "action_items": {
                                    "type": "string",
                                    "description": "Action items from the review (for post_incident_reviews)"
                                },
                                "created_at": {
                                    "type": "string",
                                    "description": "Creation timestamp in YYYY-MM-DD format"
                                },
                                "updated_at": {
                                    "type": "string",
                                    "description": "Update timestamp in YYYY-MM-DD format (for root_cause_analyses)"
                                }
                            }
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
EOF

echo "✓ Created discover_improvement.py"

# Create discover_audit.py
cat > discover_audit.py << 'EOF'
import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class DiscoverAudit(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover audit entities (audit_trails). The entity to discover is decided by entity_type.
        Optionally, filters can be applied to narrow down the search results.
        
        Supported entities:
        - audit_trails: Audit Trail records
        """
        if entity_type not in ["audit_trails"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'audit_trails'"
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
                    results.append({**entity_data, "audit_id": entity_id})
            else:
                results.append({**entity_data, "audit_id": entity_id})
        
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
                "name": "discover_audit",
                "description": "Discover audit entities (audit trails). The entity to discover is decided by entity_type. Optional filters can be applied to narrow down the search results.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'audit_trails'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters to narrow down search results. Only exact matches are supported (AND logic for multiple filters).",
                            "properties": {
                                "audit_id": {
                                    "type": "string",
                                    "description": "Audit trail ID"
                                },
                                "reference_id": {
                                    "type": "string",
                                    "description": "ID of the record that was changed"
                                },
                                "reference_type": {
                                    "type": "string",
                                    "description": "Type of record: 'user', 'client', 'vendor', 'subscription', 'sla', 'product', 'ci', 'incident', 'problem', 'escalation', 'bridge', 'change', 'rollback', 'work_order', 'communication', 'metric', 'report', 'rca'"
                                },
                                "action": {
                                    "type": "string",
                                    "description": "Action performed: 'create', 'update', 'delete'"
                                },
                                "user_id": {
                                    "type": "string",
                                    "description": "User ID who performed the action"
                                },
                                "field_name": {
                                    "type": "string",
                                    "description": "Name of the field that was changed"
                                },
                                "old_value": {
                                    "type": "string",
                                    "description": "Previous value before change"
                                },
                                "new_value": {
                                    "type": "string",
                                    "description": "New value after change"
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

echo "✓ Created discover_audit.py"

echo ""
echo "All discovery tool files have been created successfully!"
echo ""
echo "Files created:"
echo "  - discover_change_control.py"
echo "  - discover_workflows.py"
echo "  - discover_performance.py"
echo "  - discover_improvement.py"
echo "  - discover_audit.py"