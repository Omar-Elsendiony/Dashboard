import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

import json
from typing import Any, Dict, Optional

class fetch_investors_with_portfolio_holdings(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        investor_id: Optional[str] = None,
        name: Optional[str] = None,
        contact_email: Optional[str] = None,
        employee_id: Optional[str] = None
    ) -> str:
        investors = data.get("investors", {})
        portfolios = data.get("portfolios", {})
        holdings = data.get("portfolio_holdings", {})
        instruments = data.get("instruments", {})

        results = []
        for inv in investors.values():
            # Apply filters
            if investor_id and str(inv.get("investor_id")) != str(investor_id):
                continue
            if name and inv.get("name") != name:
                continue
            if contact_email and inv.get("contact_email") != contact_email:
                continue
            if employee_id and str(inv.get("employee_id")) != str(employee_id):
                continue

            inv_copy = inv.copy()
            inv_copy["portfolios"] = []

            # Gather this investor's portfolios
            for p in portfolios.values():
                if p.get("investor_id") != inv.get("investor_id"):
                    continue
                p_copy = p.copy()
                p_copy["holdings"] = []

                # Gather and enrich holdings
                for h in holdings.values():
                    if h.get("portfolio_id") != p.get("portfolio_id"):
                        continue
                    h_copy = h.copy()
                    if h_copy.get("instrument_id"):
                        del h_copy["instrument_id"]
                    instr = instruments.get(str(h.get("instrument_id")))
                    if instr:
                        h_copy["instrument"] = instr
                    p_copy["holdings"].append(h_copy)

                inv_copy["portfolios"].append(p_copy)

            results.append(inv_copy)

        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "fetch_investors_with_portfolio_holdings",
                "description": (
                    "Fetch investors (optionally filtered by investor_id, name, "
                    "contact_email, or employee_id) along with each investor’s "
                    "portfolios and their holdings enriched with instrument data."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {"type": "string", "description": "Filter by investor_id"},
                        "name": {"type": "string", "description": "Filter by investor name"},
                        "contact_email": {"type": "string", "description": "Filter by contact_email"},
                        "employee_id": {"type": "string", "description": "Filter by the employee_id (user) representing the investor"}
                    },
                    "required": []
                }
            }
        }