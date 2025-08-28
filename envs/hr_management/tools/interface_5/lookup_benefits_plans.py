import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class LookupBenefitsPlans(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], plan_id: Optional[str] = None,
               plan_type: Optional[str] = None, plan_name: Optional[str] = None, status: Optional[str] = None) -> str:
        benefits_plans = data.get("benefits_plans", {})
        results = []
        
        for plan in benefits_plans.values():
            if plan_id and plan.get("plan_id") != plan_id:
                continue
            if plan_type and plan.get("plan_type") != plan_type:
                continue
            if status and plan.get("status") != status:
                continue
            if plan_name:
                if plan.get("plan_name").lower() != plan_name.lower():
                    continue
            results.append(plan)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "lookup_benefits_plans",
                "description": "Get benefits plans with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "plan_id": {"type": "string", "description": "Filter by plan ID"},
                        "plan_type": {"type": "string", "description": "Filter by plan type (health_insurance, dental, vision, life_insurance, disability, retirement_401k, pto, flexible_spending)"},
                        "plan_name": {"type": "string", "description": "Filter by plan name case insensitively"},
                        "status": {"type": "string", "description": "Filter by status (active, inactive)"}
                    },
                    "required": []
                }
            }
        }
