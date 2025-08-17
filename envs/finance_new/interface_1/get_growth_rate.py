import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class GetGrowthRate(Tool):
    # Growth rate mapping

    @staticmethod
    def invoke(data: Dict[str, Any], fund_type: str, instrument_type: str) -> str:
        """Return growth rate for a given fund type and instrument type."""
        FUND_GROWTH_RATES: Dict[str, Dict[str, str]] = {
            "mutual_funds": {
                "equities": "8%",
                "bonds": "3.50%",
                "money_market_instruments": "2%",
                "hybrid_securities": "5.50%",
                "fund_units": "6.50%"
            },
            "exchange_traded_funds": {
                "equities": "8%",
                "bonds": "3%",
                "commodities": "5%",
                "derivatives": "-20% to 20%"
            },
            "pension_funds": {
                "equities": "7%",
                "bonds": "3%",
                "real_estate": "6.50%",
                "private_equity": "16%",
                "financing_and_debt": "16%",
                "alternative_assets": "7.50%"
            },
            "private_equity_funds": {
                "private_equity": "20%",
                "financing_and_debt": "16% - 18.50%"  # grouped similar debt instruments
            },
            "hedge_funds": {
                "equities": "10%",
                "bonds": "8%",
                "derivatives": "-15% to 15%",
                "commodities": "2.50%",
                "structured_products": "8.50%"
            },
            "sovereign_wealth_funds": {
                "equities": "7%",
                "bonds": "3%",
                "private_equity": "16%",
                "real_estate": "6.50%",
                "financing_and_debt": "8%",
                "alternative_assets": "7.50%"
            },
            "money_market_funds": {
                "money_market_instruments": "1.50% - 2%"
            },
            "real_estate_investment_trusts": {
                "real_estate": "6.50% - 8%"
            },
            "infrastructure_funds": {
                "private_equity": "8%",
                "financing_and_debt": "6.50% - 8%"
            },
            "multi_asset_funds": {
                "equities": "8%",
                "bonds": "3.50%",
                "real_estate": "6.50%",
                "commodities": "5%"
            }
        }
        fund_data = FUND_GROWTH_RATES.get(fund_type.lower())
        if not fund_data:
            return json.dumps({"error": "Invalid fund type"})
        
        growth_rate = fund_data.get(instrument_type.lower())
        if not growth_rate:
            return json.dumps({"error": "Invalid instrument type for this fund"})
        
        return json.dumps({
            "fund_type": fund_type,
            "instrument_type": instrument_type,
            "growth_rate": growth_rate
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_growth_rate",
                "description": "Get expected growth rate for a given fund type and instrument type",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_type": {
                            "type": "string",
                            "description": (
                                "The fund type. "
                                "Valid values: mutual_funds, exchange_traded_funds, pension_funds, "
                                "private_equity_funds, hedge_funds, sovereign_wealth_funds, "
                                "money_market_funds, real_estate_investment_trusts, "
                                "infrastructure_funds, multi_asset_funds"
                            )
                        },
                        "instrument_type": {
                            "type": "string",
                            "description": (
                                "The instrument type. "
                                "Valid values: equities, bonds, money_market_instruments, hybrid_securities, fund_units, "
                                "commodities, derivatives, real_estate, private_equity, financing_and_debt, "
                                "alternative_assets, structured_products"
                            )
                        }
                    },
                    "required": ["fund_type", "instrument_type"]
                }
            }
        }

