import json
from typing import Any, Dict, Optional
from collections import defaultdict
from tau_bench.envs.tool import Tool

class SummarizeInstrumentAnalysis(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], price_date: Optional[str] = None,
               instrument_type: Optional[str] = None) -> str:
        instruments = data.get("instruments", {})
        instrument_prices = data.get("instrument_prices", {})
        
        # Group by instrument type
        summary = defaultdict(lambda: {
            "count": 0,
            "avg_close_price": 0.0,
            "min_close_price": float('inf'),
            "max_close_price": 0.0,
            "total_close_price": 0.0,
            "instruments": []
        })
        
        for analysis_price in instrument_prices.values():
            # Filter by date if specified
            if price_date and analysis_price.get("price_date") != price_date:
                continue
            
            analysis_instrument_id = analysis_price.get("analysis_instrument_id")
            if not analysis_instrument_id or str(analysis_instrument_id) not in instruments:
                continue
            
            instrument = instruments[str(analysis_instrument_id)]
            inst_type = instrument.get("instrument_type")
            
            # Filter by instrument type if specified
            if instrument_type and inst_type != instrument_type:
                continue
            
            close_price = float(analysis_price.get("close_price", 0))
            
            summary[inst_type]["count"] += 1
            summary[inst_type]["total_close_price"] += close_price
            summary[inst_type]["min_close_price"] = min(summary[inst_type]["min_close_price"], close_price)
            summary[inst_type]["max_close_price"] = max(summary[inst_type]["max_close_price"], close_price)
            
            # Track instrument details
            summary[inst_type]["instruments"].append({
                "analysis_instrument_id": analysis_instrument_id,
                "ticker": instrument.get("ticker"),
                "name": instrument.get("name"),
                "close_price": close_price,
                "price_date": analysis_price.get("price_date")
            })
        
        # Calculate averages and clean up
        result = {}
        for inst_type, data_dict in summary.items():
            if data_dict["count"] > 0:
                data_dict["avg_close_price"] = round(data_dict["total_close_price"] / data_dict["count"], 4)
                if data_dict["min_close_price"] == float('inf'):
                    data_dict["min_close_price"] = 0.0
                # Remove total_close_price as it's not needed in output
                del data_dict["total_close_price"]
                result[inst_type] = data_dict
        
        return json.dumps(result, indent=2)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "summary_of_instrument_types_by_prices",
                "description": "Get a summary of instrument types with pricing statistics",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "price_date": {"type": "string", "description": "Filter by specific analysis_price date (YYYY-MM-DD)"},
                        "instrument_type": {"type": "string", "description": "Filter by specific instrument type"}
                    },
                    "required": []
                }
            }
        }
