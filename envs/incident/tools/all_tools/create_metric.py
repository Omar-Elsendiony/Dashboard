import json
from typing import Any, Dict, Optional
from datetime import datetime
from tau_bench.envs.tool import Tool

class CreateMetric(Tool):
    @staticmethod
    def _parse_iso(ts: Optional[str]) -> Optional[datetime]:
        if not ts:
            return None
        ts = ts.replace("Z", "+00:00")
        return datetime.fromisoformat(ts)

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        incident_id: str,
        metric_type: str,          # MTTA|MTTD|MTTR|MTTM|FTR
        value_minutes: int = None,
        target_minutes: int = None
    ) -> str:
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)

        try:
            metrics = data.setdefault("metrics", {})
            incidents = data.get("incidents", {})
            valid_types = {"MTTA","MTTD","MTTR","MTTM","FTR"}
            if metric_type not in valid_types:
                return json.dumps({"success": False, "error": f"Invalid metric_type. Must be one of {sorted(valid_types)}"})

            # Auto-compute MTTR if not provided
            computed_value = value_minutes
            if computed_value is None and metric_type == "MTTR":
                inc = None
                # incidents may be dict keyed by id; values have 'incident_id'
                if incident_id in incidents:
                    inc = incidents[incident_id]
                else:
                    # try to find by scanning
                    for v in incidents.values():
                        if v.get("incident_id") == incident_id:
                            inc = v
                            break
                if not inc:
                    return json.dumps({"success": False, "error": f"Incident {incident_id} not found to compute MTTR"})

                detected_at = CreateMetric._parse_iso(inc.get("detected_at"))
                end_at = CreateMetric._parse_iso(inc.get("resolved_at") or inc.get("closed_at"))
                if not detected_at or not end_at:
                    return json.dumps({"success": False, "error": "Cannot compute MTTR without detected_at and (resolved_at or closed_at)"})
                delta_minutes = int((end_at - detected_at).total_seconds() // 60)
                if delta_minutes < 0:
                    return json.dumps({"success": False, "error": "Computed negative MTTR; check incident timestamps"})
                computed_value = delta_minutes

            if computed_value is None:
                return json.dumps({"success": False, "error": "value_minutes is required for this metric_type or cannot be computed automatically"})

            metric_id = generate_id(metrics)
            timestamp = "2025-10-01T00:00:00"

            new_metric = {
                "metric_id": metric_id,
                "incident_id": incident_id,
                "metric_type": metric_type,
                "value_minutes": int(computed_value),
                "target_minutes": int(target_minutes) if target_minutes is not None else None,
                "recorded_at": timestamp,
                "created_at": timestamp
            }

            metrics[metric_id] = new_metric
            return json.dumps({
                "metric_id": metric_id,
                "metric_type": metric_type,
                "value_minutes": new_metric["value_minutes"],
                "target_minutes": new_metric["target_minutes"],
                "recorded_at": timestamp,
                "success": True
            })
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return  {
            "type": "function",
            "function": {
                "name": "create_metric",
                "description": "Create a metric; auto-computes MTTR from incident when value is not provided",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "incident_id": {"type": "string"},
                        "metric_type": {"type": "string", "description": "MTTA|MTTD|MTTR|MTTM|FTR"},
                        "value_minutes": {"type": "integer", "description": "Required unless metric_type=MTTR and timestamps are available"},
                        "target_minutes": {"type": "integer", "description": "Optional target for comparison"}
                    },
                    "required": ["incident_id","metric_type"]
                }
            }
        }
