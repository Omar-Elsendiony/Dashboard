import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class HandleInstrument(Tool):
    """
    A tool to create or update a financial instrument.
    """

    @staticmethod
    def invoke(data: Dict[str, Any], fund_manager_approval: bool = False, 
               compliance_officer_approval: bool = False,
               instrument_id: Optional[str] = None, ticker: Optional[str] = None, 
               name: Optional[str] = None, instrument_type: Optional[str] = None, 
               status: Optional[str] = None) -> str:
        """
        Creates a new financial instrument or updates an existing one.

        Args:
            data: The database json.
            fund_manager_approval: Fund Manager approval (required for creation and updates).
            compliance_officer_approval: Compliance Officer approval (required for creation and critical updates).
            instrument_id: The ID of the instrument to update. If None, a new one is created.
            ticker: The unique ticker symbol for the instrument.
            name: The name of the instrument.
            instrument_type: The type of the instrument.
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
        valid_instrument_types = [
            'equities_common_shares','equities_preferred_shares','equities_indexed','equities_domestic','equities_international','bonds_corporate','bonds_municipal','bonds_government','bonds_inflation_linked','bonds_high_yield','bonds_distressed','money_market_treasury_bills','money_market_commercial_paper','certificates_of_deposit','repurchase_agreements','short_term_municipal_notes','bankers_acceptances','commodities_gold_oil_futures','commodities_spot','commodities_futures','derivatives_options','derivatives_futures','derivatives_swaps','real_estate_direct_property','real_estate_reits','mortgage_backed_securities','property_development_loans','private_equity','equity_stakes_private_companies','equity_stakes_infrastructure_assets','mezzanine_financing','convertible_preferred_stock','leveraged_buyout_debt','distressed_debt','project_finance_debt','infrastructure_bonds','ppp_investments','infrastructure_debt_equity','infrastructure_projects','alternative_assets_hedge_funds','alternative_assets_commodities'
        ]

        # Update logic
        if instrument_id:
            if instrument_id not in instruments:
                return json.dumps({
                    "success": False,
                    "error": f"Instrument {instrument_id} not found"
                })

            # Fund Manager approval always required for updates
            if not fund_manager_approval:
                return json.dumps({
                    "success": False,
                    "error": "Fund Manager approval is required for instrument updates"
                })

            instrument = instruments[instrument_id]
            critical_change = False
            
            # Check if this is a critical change (ticker or instrument_type)
            if ticker is not None and instrument.get('ticker') != ticker:
                critical_change = True
            if instrument_type is not None and instrument.get('instrument_type') != instrument_type:
                critical_change = True
            
            # Compliance Officer approval required for critical changes
            if critical_change and not compliance_officer_approval:
                return json.dumps({
                    "success": False,
                    "error": "Compliance Officer approval is required for ticker or instrument type changes"
                })

            # Validate and update ticker if provided
            if ticker is not None:
                if not ticker.strip():
                    return json.dumps({
                        "success": False,
                        "error": "Ticker cannot be empty"
                    })
                
                # Check for ticker uniqueness if it's being changed
                if instrument.get('ticker') != ticker:
                    for inst_id, inst_data in instruments.items():
                        if inst_id != instrument_id and inst_data.get('ticker') == ticker:
                            return json.dumps({
                                "success": False,
                                "error": f"Ticker '{ticker}' already exists for another instrument."
                            })
                
                instrument['ticker'] = ticker

            # Validate and update name if provided
            if name is not None:
                if not name.strip():
                    return json.dumps({
                        "success": False,
                        "error": "Name cannot be empty"
                    })
                instrument['name'] = name

            # Validate and update instrument_type if provided
            if instrument_type is not None:
                if instrument_type not in valid_instrument_types:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid instrument_type '{instrument_type}' provided."
                    })
                instrument['instrument_type'] = instrument_type

            # Validate and update status if provided
            if status is not None:
                if status not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid status. Must be one of {valid_statuses}"
                    })
                instrument['status'] = status

            instrument['updated_at'] = "2025-10-01T00:00:00"
            return json.dumps(instrument)

        # Create logic
        else:
            # For creation, both approvals are required
            if not fund_manager_approval:
                return json.dumps({
                    "success": False,
                    "error": "Fund Manager approval is required for instrument creation"
                })
            
            if not compliance_officer_approval:
                return json.dumps({
                    "success": False,
                    "error": "Compliance Officer approval is required for instrument creation"
                })

            # All fields required for creation
            if not ticker or not ticker.strip():
                return json.dumps({
                    "success": False,
                    "error": "Ticker is required for instrument creation"
                })
            
            if not name or not name.strip():
                return json.dumps({
                    "success": False,
                    "error": "Name is required for instrument creation"
                })

            if not instrument_type:
                return json.dumps({
                    "success": False,
                    "error": "Instrument type is required for instrument creation"
                })

            if instrument_type not in valid_instrument_types:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid instrument_type '{instrument_type}' provided."
                })

            if status and status not in valid_statuses:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid status. Must be one of {valid_statuses}"
                })

            # Check for ticker uniqueness
            for inst in instruments.values():
                if inst.get('ticker') == ticker:
                    return json.dumps({
                        "success": False,
                        "error": f"Ticker '{ticker}' already exists."
                    })

            new_id = str(generate_id(instruments))
            timestamp = "2025-10-01T00:00:00"
            new_instrument = {
                "instrument_id": str(new_id),
                "ticker": ticker,
                "name": name,
                "instrument_type": instrument_type,
                "status": status or "active",
                "created_at": timestamp,
                "updated_at": timestamp
            }
            instruments[new_id] = new_instrument
            return json.dumps(new_instrument)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        """
        Returns the schema for the ManageInstrument tool.
        """
        return {
            "type": "function",
            "function": {
                "name": "handle_instrument",
                "description": "Creates a new financial instrument or updates an existing one. For creation: requires ticker, name, instrument_type, and both Fund Manager and Compliance Officer approvals. For updates: requires instrument_id and Fund Manager approval (Compliance Officer approval also required if changing ticker or instrument_type). Only provide the fields you want to update - all update fields are optional except instrument_id.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "instrument_id": {
                            "type": "string",
                            "description": "ID of the instrument to update. If omitted, a new instrument is created."
                        },
                        "ticker": {
                            "type": "string",
                            "description": "The unique ticker symbol for the instrument. Required for creation, optional for updates."
                        },
                        "name": {
                            "type": "string",
                            "description": "The name of the instrument. Required for creation, optional for updates."
                        },
                        "instrument_type": {
                            "type": "string",
                            "description": "The type of instrument, e.g., 'equities_common_shares', 'bonds_corporate'. Required for creation, optional for updates. Changing this requires Compliance Officer approval."
                        },
                        "fund_manager_approval": {
                            "type": "boolean",
                            "description": "Fund Manager approval (True/False). Required for all creation and update operations."
                        },
                        "compliance_officer_approval": {
                            "type": "boolean",
                            "description": "Compliance Officer approval (True/False). Required for creation and for updates that change ticker or instrument_type."
                        },
                        "status": {
                            "type": "string",
                            "description": "The status of the instrument. Allowed values: active, inactive. Optional for both creation and updates."
                        }
                    },
                    "required": ["fund_manager_approval", "compliance_officer_approval"]
                }
            }
        }