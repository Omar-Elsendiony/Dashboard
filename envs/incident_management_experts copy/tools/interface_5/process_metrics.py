import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ProcessMetrics(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], metric_data: Dict[str, Any]) -> str:
        """
        Record incident performance metrics.

        metric_data must include:
        - incident_id (required)
        - metric_type (required): MTTA, MTTD, MTTR, MTTM, FTR
        - value_minutes (required)
        - target_minutes (optional)
        - recorded_at (optional)
        """

        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1

        # def check_approval(data: Dict[str, Any], required_roles: list) -> bool:
        #     approvals = data.get("approvals", {})
        #     return any(approvals.get(role) for role in required_roles)

        # Check approval
        # if not check_approval(data, ["incident_manager", "system_administrator"]):
        #     return json.dumps({
        #         "success": False,
        #         "error": "Missing approval for recording metrics. Required: incident_manager OR system_administrator"
        #     })

        metrics = data.get("metrics", {})
        incidents = data.get("incidents", {})

        incident_id = metric_data.get("incident_id")
        metric_type = metric_data.get("metric_type")
        value_minutes = metric_data.get("value_minutes")
        target_minutes = metric_data.get("target_minutes")
        recorded_at = metric_data.get("recorded_at")

        # Validate required fields
        if not all([incident_id, metric_type, value_minutes is not None]):
            return json.dumps({
                "success": False,
                "error": "Missing required fields: incident_id, metric_type, value_minutes"
            })

        # Validate incident exists and status
        if incident_id not in incidents:
            return json.dumps({"success": False, "error": f"Incident {incident_id} not found"})

        if incidents[incident_id].get("status") not in ["resolved", "closed"]:
            return json.dumps({
                "success": False,
                "error": f"Incident must be in 'resolved' or 'closed' status for metrics recording. Current status: {incidents[incident_id].get('status')}"
            })

        # Validate metric_type
        valid_metric_types = ["MTTA", "MTTD", "MTTR", "MTTM", "FTR"]
        if metric_type not in valid_metric_types:
            return json.dumps({
                "success": False,
                "error": f"Invalid metric_type. Must be one of: {', '.join(valid_metric_types)}"
            })

        # Validate value_minutes
        try:
            value_minutes = float(value_minutes)
            if value_minutes < 0:
                raise ValueError
        except (ValueError, TypeError):
            return json.dumps({
                "success": False,
                "error": "value_minutes must be a non-negative number"
            })

        # Validate target_minutes
        if target_minutes is not None:
            try:
                target_minutes = float(target_minutes)
                if target_minutes < 0:
                    raise ValueError
            except (ValueError, TypeError):
                return json.dumps({
                    "success": False,
                    "error": "target_minutes must be a non-negative number"
                })

        # Create new metric
        new_id = generate_id(metrics)
        new_metric = {
            "metric_id": str(new_id),
            "incident_id": incident_id,
            "metric_type": metric_type,
            "value_minutes": int(value_minutes),
            "target_minutes": int(target_minutes) if target_minutes is not None else None,
            "recorded_at": recorded_at if recorded_at else "2025-10-02T12:00:00",
            "created_at": "2025-10-02T12:00:00"
        }

        metrics[str(new_id)] = new_metric

        return json.dumps({
            "success": True,
            "action": "create",
            "metric_id": str(new_id),
            "message": f"Metrics {new_id} created successfully",
            "metric_data": new_metric
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "process_metrics",
                "description": "Create and record incident performance metrics in the incident management system. Supports MTTA, MTTD, MTTR, MTTM, FTR metrics.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "metric_data": {
                            "type": "object",
                            "description": "Metric data to record",
                            "properties": {
                                "incident_id": {"type": "string", "description": "ID of the incident (required)"},
                                "metric_type": {"type": "string", "enum": ["MTTA", "MTTD", "MTTR", "MTTM", "FTR"], "description": "Type of metric (required)"},
                                "value_minutes": {"type": "number", "description": "Metric value in minutes (required, non-negative)"},
                                "target_minutes": {"type": "number", "description": "Target value in minutes (optional, non-negative)"},
                                "recorded_at": {"type": "string", "description": "Timestamp of recording (optional)"}
                            },
                            "required": ["incident_id", "metric_type", "value_minutes"]
                        }
                    },
                    "required": ["metric_data"]
                }
            }
        }
