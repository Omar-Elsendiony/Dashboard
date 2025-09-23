import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class AddressInstrument(Tool):
    """
    A tool to create or update a financial instrument.
    """

    @staticmethod
    def invoke(data: Dict[str, Any], ticker: str, name: str, instrument_type: str, instrument_id: Optional[str] = None, status: str = "active") -> str:
        """
        Creates a new financial instrument or updates an existing one.

        Args:
            data: The database json.
            ticker: The unique ticker symbol for the instrument.
            name: The name of the instrument.
            instrument_type: The type of the instrument.
            instrument_id: The ID of the instrument to update. If None, a new one is created.
            status: The status of the instrument.

        Returns:
            A json string of the created/updated instrument or an error.
        """
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1

        instruments = data.get("instruments", {})

        valid_statuses = ["active", "inactive"]
        if status not in valid_statuses:
            return json.dumps({"error": f"Invalid status. Must be one of {valid_statuses}"})

        # In a real scenario, this list would be more robustly checked or loaded from a config.
        valid_instrument_types = [
            'equities_common_shares','equities_preferred_shares','equities_indexed','equities_domestic','equities_international','bonds_corporate','bonds_municipal','bonds_government','bonds_inflation_linked','bonds_high_yield','bonds_distressed','money_market_treasury_bills','money_market_commercial_paper','certificates_of_deposit','repurchase_agreements','short_term_municipal_notes','bankers_acceptances','commodities_gold_oil_futures','commodities_spot','commodities_futures','derivatives_options','derivatives_futures','derivatives_swaps','real_estate_direct_property','real_estate_reits','mortgage_backed_securities','property_development_loans','private_equity','equity_stakes_private_companies','equity_stakes_infrastructure_assets','mezzanine_financing','convertible_preferred_stock','leveraged_buyout_debt','distressed_debt','project_finance_debt','infrastructure_bonds','ppp_investments','infrastructure_debt_equity','infrastructure_projects','alternative_assets_hedge_funds','alternative_assets_commodities'
        ]
        if instrument_type not in valid_instrument_types:
            return json.dumps({"error": f"Invalid instrument_type '{instrument_type}' provided."})

        # Update logic
        if instrument_id:
            if instrument_id not in instruments:
                return json.dumps({"error": f"Instrument {instrument_id} not found"})

            # Check for ticker uniqueness if it's being changed
            if instruments[instrument_id].get('ticker') != ticker:
                for inst_id, inst_data in instruments.items():
                    if inst_id != instrument_id and inst_data.get('ticker') == ticker:
                        return json.dumps({"error": f"Ticker '{ticker}' already exists for another instrument."})
            
            instrument = instruments[instrument_id]
            instrument.update({
                "ticker": ticker,
                "name": name,
                "instrument_type": instrument_type,
                "status": status,
                "updated_at": "2025-10-01T00:00:00"
            })
            return json.dumps(instrument)

        # Create logic
        else:
            # Check for ticker uniqueness
            for inst in instruments.values():
                if inst.get('ticker') == ticker:
                    return json.dumps({"error": f"Ticker '{ticker}' already exists."})

            new_id = str(generate_id(instruments))
            timestamp = "2025-10-01T00:00:00"
            new_instrument = {
                "instrument_id": new_id,
                "ticker": ticker,
                "name": name,
                "instrument_type": instrument_type,
                "status": status,
                "created_at": timestamp,
                "updated_at": timestamp
            }
            instruments[new_id] = new_instrument
            return json.dumps(new_instrument)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        """
        Returns the schema for the AddressInstrument tool.
        """
        return {
            "type": "function",
            "function": {
                "name": "address_instrument",
                "description": "Creates a new financial instrument or updates an existing one.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "instrument_id": {
                            "type": "string",
                            "description": "ID of the instrument to update. If omitted, a new instrument is created."
                        },
                        "ticker": {
                            "type": "string",
                            "description": "The unique ticker symbol for the instrument."
                        },
                        "name": {
                            "type": "string",
                            "description": "The name of the instrument."
                        },
                        "instrument_type": {
                            "type": "string",
                            "description": "The type of instrument, e.g., 'equities_common_shares', 'bonds_corporate'."
                        },
                        "status": {
                            "type": "string",
                            "description": "The status of the instrument. Allowed values: active, inactive. Defaults to 'active'."
                        }
                    },
                    "required": ["ticker", "name", "instrument_type"]
                }
            }
        }
