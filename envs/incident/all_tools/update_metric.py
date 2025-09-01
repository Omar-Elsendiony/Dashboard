import json
from typing import Any, Dict
from datetime import datetime
from tau_bench.envs.tool import Tool

class UpdateMetric(Tool):
    @staticmethod
    def _is_iso(ts: str) -> bool:
        try:
            datetime.fromisoformat(ts.replace("Z","+00:00"))
            return True
        except Exception:
            return False

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        metric_id: str,
        incident_id: str = None,
        metric_type: str = None,    # MTTA|MTTD|MTTR|MTTM|FTR
        value_minutes: int = None,
        target_minutes: int = None,
        recorded_at: str = None
    ) -> str:
        try:
            metrics = data.get("metrics", {})
            if metric_id not in metrics:
                return json.dumps({"success": False, "error": f"Metric {metric_id} not found"})

            valid_types = {"MTTA","MTTD","MTTR","MTTM","FTR"}
            if metric_type and metric_type not in valid_types:
                return json.dumps({"success": False, "error": f"Invalid metric_type. Must be one of {sorted(valid_types)}"})
            if value_minutes is not None and value_minutes < 0:
                return json.dumps({"success": False, "error": "value_minutes must be non-negative"})
            if target_minutes is not None and target_minutes < 0:
                return json.dumps({"success": False, "error": "target_minutes must be non-negative"})
            if recorded_at is not None and not UpdateMetric._is_iso(recorded_at):
                return json.dumps({"success": False, "error": "recorded_at must be ISO timestamp"})

            m = metrics[metric_id]
            if incident_id is not None: m["incident_id"] = incident_id
            if metric_type is not None: m["metric_type"] = metric_type
            if value_minutes is not None: m["value_minutes"] = value_minutes
            if target_minutes is not None: m["target_minutes"] = target_minutes
            if recorded_at is not None: m["recorded_at"] = recorded_at

            return json.dumps(m)
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"update_metric",
                "description":"Update a metric; validates enum/non-negative integers/timestamp",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "metric_id":{"type":"string"},
                        "incident_id":{"type":"string"},
                        "metric_type":{"type":"string","description":"MTTA|MTTD|MTTR|MTTM|FTR"},
                        "value_minutes":{"type":"integer"},
                        "target_minutes":{"type":"integer"},
                        "recorded_at":{"type":"string","description":"ISO timestamp"}
                    },
                    "required":["metric_id"]
                }
            }
        }
