import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class ManagePerformanceMetrics(Tool):
    """
    Create and update performance metrics for incident management KPIs.
    """
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        action: str,
        metric_id: Optional[str] = None,
        incident_id: Optional[str] = None,
        metric_type: Optional[str] = None,
        calculated_value_minutes: Optional[int] = None,
        sla_target_minutes: Optional[int] = None,
        recorded_by: Optional[str] = None,
    ) -> str:
        """
        Create or update performance metric records for incident management KPIs.

        Actions:
        - create: Create new performance metric (requires incident_id, metric_type, calculated_value_minutes, recorded_by)
        - update: Update existing performance metric (requires metric_id and at least one field to update)
        """
        def generate_id(table: Dict[str, Any]) -> str:
            """Generates a new unique ID for a record."""
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        timestamp = "2025-10-01T12:00:00"
        metrics = data.get("performance_metrics", {})
        incidents = data.get("incidents", {})
        users = data.get("users", {})

        valid_metric_types = ["MTTA", "MTTD", "MTTR", "MTTM", "FTR"]
        
        if action not in ["create", "update"]:
            return json.dumps({
                "success": False,
                "error": "Invalid action. Must be 'create' or 'update'"
            })

        if action == "update" and not metric_id:
            return json.dumps({
                "success": False,
                "error": "metric_id is required for update action"
            })

        if action == "create":
            if not all([incident_id, metric_type, calculated_value_minutes is not None, recorded_by]):
                return json.dumps({
                    "success": False,
                    "error": "incident_id, metric_type, calculated_value_minutes, and recorded_by are required for create action"
                })

            # Validate incident exists
            if incident_id not in incidents:
                return json.dumps({
                    "success": False,
                    "error": f"Incident with ID {incident_id} not found"
                })

            # Validate user exists and is active
            if recorded_by not in users:
                return json.dumps({
                    "success": False,
                    "error": f"User with ID {recorded_by} not found"
                })
            if users[recorded_by]["status"] != "active":
                return json.dumps({
                    "success": False,
                    "error": f"User with ID {recorded_by} is not active"
                })

            if metric_type not in valid_metric_types:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid metric_type. Must be one of: {', '.join(valid_metric_types)}"
                })

            if calculated_value_minutes < 0:
                return json.dumps({
                    "success": False,
                    "error": "calculated_value_minutes cannot be negative"
                })

            if sla_target_minutes is not None and sla_target_minutes < 0:
                return json.dumps({
                    "success": False,
                    "error": "sla_target_minutes cannot be negative"
                })

            new_id = generate_id(metrics)
            new_metric = {
                "metric_id": new_id,
                "incident_id": incident_id,
                "metric_type": metric_type,
                "calculated_value_minutes": calculated_value_minutes,
                "sla_target_minutes": sla_target_minutes,
                "recorded_by": recorded_by,
                "recorded_date": timestamp,
                "created_at": timestamp,
                "updated_at": timestamp
            }
            metrics[new_id] = new_metric

            return json.dumps({
                "success": True,
                "action": "create",
                "metric_id": new_id,
                "metric_data": new_metric
            })

        if action == "update":
            if metric_id not in metrics:
                return json.dumps({
                    "success": False,
                    "error": f"Metric with ID {metric_id} not found"
                })

            # Validate at least one field is being updated
            if all(v is None for v in [metric_type, calculated_value_minutes, sla_target_minutes, recorded_by]):
                return json.dumps({
                    "success": False,
                    "error": "At least one field must be provided for update"
                })

            existing_metric = metrics[metric_id]

            if recorded_by is not None:
                if recorded_by not in users:
                    return json.dumps({
                        "success": False,
                        "error": f"User with ID {recorded_by} not found"
                    })
                if users[recorded_by]["status"] != "active":
                    return json.dumps({
                        "success": False,
                        "error": f"User with ID {recorded_by} is not active"
                    })

            if metric_type is not None:
                if metric_type not in valid_metric_types:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid metric_type. Must be one of: {', '.join(valid_metric_types)}"
                    })
                existing_metric["metric_type"] = metric_type

            if calculated_value_minutes is not None:
                if calculated_value_minutes < 0:
                    return json.dumps({
                        "success": False,
                        "error": "calculated_value_minutes cannot be negative"
                    })
                existing_metric["calculated_value_minutes"] = calculated_value_minutes

            if sla_target_minutes is not None:
                if sla_target_minutes < 0:
                    return json.dumps({
                        "success": False,
                        "error": "sla_target_minutes cannot be negative"
                    })
                existing_metric["sla_target_minutes"] = sla_target_minutes

            if recorded_by is not None:
                existing_metric["recorded_by"] = recorded_by
                existing_metric["recorded_date"] = timestamp

            existing_metric["updated_at"] = timestamp

            return json.dumps({
                "success": True,
                "action": "update",
                "metric_id": metric_id,
                "metric_data": existing_metric
            })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        """
        Returns comprehensive information about the tool's capabilities, parameters, and data schema.
        """
        return {
            "type": "function",
            "function": {
                "name": "manage_performance_metrics",
                "description": "Create/update performance metrics for incident management KPIs (MTTA, MTTD, MTTR, MTTM, FTR). Actions: 'create' (requires incident_id, metric_type, calculated_value_minutes, recorded_by; optional: sla_target_minutes), 'update' (requires metric_id; optional: metric_type, calculated_value_minutes, sla_target_minutes, recorded_by).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' or 'update'",
                            "enum": ["create", "update"]
                        },
                        "metric_id": {
                            "type": "string",
                            "description": "Required for update. ID of the metric to update"
                        },
                        "incident_id": {
                            "type": "string",
                            "description": "Required for create. ID of the incident this metric belongs to"
                        },
                        "metric_type": {
                            "type": "string",
                            "description": "Type of performance metric: MTTA (Mean Time To Acknowledge), MTTD (Mean Time To Detect), MTTR (Mean Time To Resolve), MTTM (Mean Time To Mitigate), FTR (First Time Resolution Rate)",
                            "enum": ["MTTA", "MTTD", "MTTR", "MTTM", "FTR"]
                        },
                        "calculated_value_minutes": {
                            "type": "integer",
                            "description": "Actual measured value of the metric in minutes (must be non-negative)"
                        },
                        "sla_target_minutes": {
                            "type": "integer",
                            "description": "Optional. Target value according to SLA in minutes (must be non-negative)"
                        },
                        "recorded_by": {
                            "type": "string",
                            "description": "ID of the active user recording the metric"
                        }
                    },
                    "required": ["action"]
                }
            }
        }