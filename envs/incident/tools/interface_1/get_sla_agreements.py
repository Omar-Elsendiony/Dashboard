import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetSlaAgreements(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        sla_id: str = None,
        subscription_id: str = None,
        severity_level: str = None
    ) -> str:
        slas = data.get("sla_agreements", {})
        results = []

        for sla in slas.values():
            if sla_id and sla.get("sla_id") != sla_id:
                continue
            if subscription_id and sla.get("subscription_id") != subscription_id:
                continue
            if severity_level and sla.get("severity_level") != severity_level:
                continue
            results.append(sla)

        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_sla_agreements",
                "description": "Unified get/list for SLA agreements with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "sla_id": {"type": "string"},
                        "subscription_id": {"type": "string"},
                        "severity_level": {"type": "string", "description": "P1|P2|P3|P4"}
                    },
                    "required": []
                }
            }
        }
