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
