import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ManipulateSlaAgreements(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, sla_data: Dict[str, Any] = None, sla_id: str = None) -> str:
        """
        Create or update SLA agreement records.
        
        Actions:
        - create: Create new SLA agreement record (requires sla_data with subscription_id, severity_level, response_time_minutes, resolution_time_hours)
        - update: Update existing SLA agreement record (requires sla_id and sla_data with changes)
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
        
        # Access sla_agreements data
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for sla_agreements"
            })
        
        sla_agreements = data.get("sla_agreements", {})
        
        if action == "create":
            if not sla_data:
                return json.dumps({
                    "success": False,
                    "error": "sla_data is required for create action"
                })
            
            # Validate required fields for creation
            required_fields = ["subscription_id", "severity_level", "response_time_minutes", "resolution_time_hours"]
            missing_fields = [field for field in required_fields if field not in sla_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields for SLA agreement creation: {', '.join(missing_fields)}"
                })
            
            # Validate only allowed fields are present
            allowed_fields = ["subscription_id", "severity_level", "response_time_minutes", "resolution_time_hours", "availability_percentage"]
            invalid_fields = [field for field in sla_data.keys() if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for SLA agreement creation: {', '.join(invalid_fields)}"
                })
            
            # Validate enum fields
            valid_severity_levels = ["P1", "P2", "P3", "P4"]
            if sla_data["severity_level"] not in valid_severity_levels:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid severity_level '{sla_data['severity_level']}'. Must be one of: {', '.join(valid_severity_levels)}"
                })
            
            # Validate response time minutes
            response_time = sla_data["response_time_minutes"]
            if not isinstance(response_time, int) or response_time <= 0:
                return json.dumps({
                    "success": False,
                    "error": "response_time_minutes must be a positive integer"
                })
            
            # Validate resolution time hours
            resolution_time = sla_data["resolution_time_hours"]
            if not isinstance(resolution_time, int) or resolution_time <= 0:
                return json.dumps({
                    "success": False,
                    "error": "resolution_time_hours must be a positive integer"
                })
            
            # Validate availability percentage if provided
            if "availability_percentage" in sla_data:
                availability = sla_data["availability_percentage"]
                if not isinstance(availability, (int, float)) or availability < 0 or availability > 100:
                    return json.dumps({
                        "success": False,
                        "error": "availability_percentage must be a number between 0 and 100"
                    })
            
            # Check for duplicate SLA agreement for same subscription and severity level
            subscription_id = sla_data["subscription_id"]
            severity_level = sla_data["severity_level"]
            for existing_sla in sla_agreements.values():
                if (existing_sla.get("subscription_id") == subscription_id and 
                    existing_sla.get("severity_level") == severity_level):
                    return json.dumps({
                        "success": False,
                        "error": f"SLA agreement already exists for subscription {subscription_id} with severity level {severity_level}"
                    })
            
            # Generate new SLA ID
            new_sla_id = generate_id(sla_agreements)
            
            # Create new SLA agreement record
            new_sla = {
                "sla_id": str(new_sla_id),
                "subscription_id": str(sla_data["subscription_id"]),
                "severity_level": sla_data["severity_level"],
                "response_time_minutes": sla_data["response_time_minutes"],
                "resolution_time_hours": sla_data["resolution_time_hours"],
                "availability_percentage": sla_data.get("availability_percentage"),
                "created_at": "2025-10-01T00:00:00"
            }
            
            sla_agreements[str(new_sla_id)] = new_sla
            
            return json.dumps({
                "success": True,
                "action": "create",
                "sla_id": str(new_sla_id),
                "sla_data": new_sla
            })
        
        elif action == "update":
            if not sla_id:
                return json.dumps({
                    "success": False,
                    "error": "sla_id is required for update action"
                })
            
            if sla_id not in sla_agreements:
                return json.dumps({
                    "success": False,
                    "error": f"SLA agreement record {sla_id} not found"
                })
            
            if not sla_data:
                return json.dumps({
                    "success": False,
                    "error": "sla_data is required for update action"
                })
            
            # Validate only allowed fields are present for updates
            allowed_update_fields = ["response_time_minutes", "resolution_time_hours", "availability_percentage"]
            invalid_fields = [field for field in sla_data.keys() if field not in allowed_update_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for SLA agreement update: {', '.join(invalid_fields)}. Cannot update subscription_id or severity_level."
                })
            
            # Validate response time minutes if provided
            if "response_time_minutes" in sla_data:
                response_time = sla_data["response_time_minutes"]
                if not isinstance(response_time, int) or response_time <= 0:
                    return json.dumps({
                        "success": False,
                        "error": "response_time_minutes must be a positive integer"
                    })
            
            # Validate resolution time hours if provided
            if "resolution_time_hours" in sla_data:
                resolution_time = sla_data["resolution_time_hours"]
                if not isinstance(resolution_time, int) or resolution_time <= 0:
                    return json.dumps({
                        "success": False,
                        "error": "resolution_time_hours must be a positive integer"
                    })
            
            # Validate availability percentage if provided
            if "availability_percentage" in sla_data:
                availability = sla_data["availability_percentage"]
                if availability is not None and (not isinstance(availability, (int, float)) or availability < 0 or availability > 100):
                    return json.dumps({
                        "success": False,
                        "error": "availability_percentage must be a number between 0 and 100"
                    })
            
            # Get current SLA data
            current_sla = sla_agreements[sla_id].copy()
            
            # Update SLA agreement record
            updated_sla = current_sla.copy()
            for key, value in sla_data.items():
                updated_sla[key] = value
            
            sla_agreements[sla_id] = updated_sla
            
            return json.dumps({
                "success": True,
                "action": "update",
                "sla_id": str(sla_id),
                "sla_data": updated_sla
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manipulate_sla_agreements",
                "description": "Create or update SLA agreement records in the incident management system. This tool manages service level agreements that define response and resolution time commitments for different incident severity levels. For creation, establishes new SLA agreement records with comprehensive validation to ensure proper time commitments and prevent duplicate agreements for the same subscription-severity combination. For updates, modifies existing SLA agreement records while maintaining data integrity. Validates severity levels, time commitments, and availability percentages according to business requirements. Essential for incident response planning, performance measurement, and client expectation management.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' to establish new SLA agreement record, 'update' to modify existing SLA agreement record",
                            "enum": ["create", "update"]
                        },
                        "sla_data": {
                            "type": "object",
                            "description": "SLA agreement data object. For create: requires subscription_id, severity_level, response_time_minutes (positive integer), resolution_time_hours (positive integer), with optional availability_percentage (0-100). For update: includes SLA fields to change (subscription_id and severity_level cannot be updated). SYNTAX: {\"key\": \"value\"}",
                            "properties": {
                                "subscription_id": {
                                    "type": "string",
                                    "description": "Reference to client subscription record (required for create only, cannot be updated, unique with severity_level)"
                                },
                                "severity_level": {
                                    "type": "string",
                                    "description": "Incident severity level: 'P1', 'P2', 'P3', 'P4' (required for create only, cannot be updated)",
                                    "enum": ["P1", "P2", "P3", "P4"]
                                },
                                "response_time_minutes": {
                                    "type": "integer",
                                    "description": "Maximum response time in minutes (positive integer)"
                                },
                                "resolution_time_hours": {
                                    "type": "integer",
                                    "description": "Maximum resolution time in hours (positive integer)"
                                },
                                "availability_percentage": {
                                    "type": "number",
                                    "description": "Service availability commitment as percentage (0-100, optional)"
                                }
                            }
                        },
                        "sla_id": {
                            "type": "string",
                            "description": "Unique identifier of the SLA agreement record (required for update action only)"
                        }
                    },
                    "required": ["action"]
                }
            }
        }
