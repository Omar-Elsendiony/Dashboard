#!/bin/bash

# Create invoice management tools

# create_invoice.py
cat > create_invoice.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class CreateInvoice(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], commitment_id: str, invoice_date: str,
               due_date: str, amount: float, status: str = "issued") -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        commitments = data.get("commitments", {})
        invoices = data.get("invoices", {})
        
        # Validate commitment exists
        if str(commitment_id) not in commitments:
            raise ValueError(f"Commitment {commitment_id} not found")
        
        # Validate status
        valid_statuses = ["issued", "paid"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        # Validate amount is positive
        if amount <= 0:
            raise ValueError("Amount must be positive")
        
        invoice_id = generate_id(invoices)
        timestamp = "2025-10-01T00:00:00"
        
        new_invoice = {
            "invoice_id": str(invoice_id),
            "commitment_id": commitment_id,
            "invoice_date": invoice_date,
            "due_date": due_date,
            "amount": amount,
            "status": status,
            "updated_at": timestamp
        }
        
        invoices[str(invoice_id)] = new_invoice
        return json.dumps(new_invoice)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_invoice",
                "description": "Create a new invoice for a commitment",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "commitment_id": {"type": "string", "description": "ID of the commitment"},
                        "invoice_date": {"type": "string", "description": "Invoice date in YYYY-MM-DD format"},
                        "due_date": {"type": "string", "description": "Due date in YYYY-MM-DD format"},
                        "amount": {"type": "number", "description": "Invoice amount"},
                        "status": {"type": "string", "description": "Invoice status (issued, paid), defaults to issued"}
                    },
                    "required": ["commitment_id", "invoice_date", "due_date", "amount"]
                }
            }
        }
EOF

# delete_invoice.py
cat > delete_invoice.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class DeleteInvoice(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], invoice_id: str) -> str:
        invoices = data.get("invoices", {})
        payments = data.get("payments", {})
        
        # Validate invoice exists
        if str(invoice_id) not in invoices:
            raise ValueError(f"Invoice {invoice_id} not found")
        
        # Check if invoice has associated payments
        for payment in payments.values():
            if payment.get("invoice_id") == invoice_id:
                raise ValueError(f"Cannot delete invoice {invoice_id} - it has associated payments")
        
        # Delete the invoice
        deleted_invoice = invoices.pop(str(invoice_id))
        
        return json.dumps({
            "status": "deleted",
            "deleted_invoice": deleted_invoice
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "delete_invoice",
                "description": "Delete an invoice (only if no payments are associated)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "invoice_id": {"type": "string", "description": "ID of the invoice to delete"}
                    },
                    "required": ["invoice_id"]
                }
            }
        }
EOF

# get_invoices.py
cat > get_invoices.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetInvoices(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], commitment_id: Optional[str] = None,
               status: Optional[str] = None, due_date_from: Optional[str] = None,
               due_date_to: Optional[str] = None) -> str:
        invoices = data.get("invoices", {})
        results = []
        
        for invoice in invoices.values():
            if commitment_id and invoice.get("commitment_id") != commitment_id:
                continue
            if status and invoice.get("status") != status:
                continue
            if due_date_from and invoice.get("due_date") < due_date_from:
                continue
            if due_date_to and invoice.get("due_date") > due_date_to:
                continue
            results.append(invoice)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_invoices",
                "description": "Get invoices with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "commitment_id": {"type": "string", "description": "Filter by commitment ID"},
                        "status": {"type": "string", "description": "Filter by status (issued, paid)"},
                        "due_date_from": {"type": "string", "description": "Filter invoices due from this date (YYYY-MM-DD)"},
                        "due_date_to": {"type": "string", "description": "Filter invoices due until this date (YYYY-MM-DD)"}
                    },
                    "required": []
                }
            }
        }
EOF

# update_invoice.py
cat > update_invoice.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateInvoice(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], invoice_id: str, 
               invoice_date: Optional[str] = None, due_date: Optional[str] = None,
               amount: Optional[float] = None, status: Optional[str] = None) -> str:
        invoices = data.get("invoices", {})
        
        # Validate invoice exists
        if str(invoice_id) not in invoices:
            raise ValueError(f"Invoice {invoice_id} not found")
        
        invoice = invoices[str(invoice_id)]
        
        # Validate status if provided
        if status:
            valid_statuses = ["issued", "paid"]
            if status not in valid_statuses:
                raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        # Validate amount if provided
        if amount is not None and amount <= 0:
            raise ValueError("Amount must be positive")
        
        # Update fields
        if invoice_date:
            invoice["invoice_date"] = invoice_date
        if due_date:
            invoice["due_date"] = due_date
        if amount is not None:
            invoice["amount"] = amount
        if status:
            invoice["status"] = status
        
        invoice["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps(invoice)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_invoice",
                "description": "Update an existing invoice",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "invoice_id": {"type": "string", "description": "ID of the invoice to update"},
                        "invoice_date": {"type": "string", "description": "New invoice date in YYYY-MM-DD format"},
                        "due_date": {"type": "string", "description": "New due date in YYYY-MM-DD format"},
                        "amount": {"type": "number", "description": "New invoice amount"},
                        "status": {"type": "string", "description": "New status (issued, paid)"}
                    },
                    "required": ["invoice_id"]
                }
            }
        }
EOF

# retrieve_invoices.py
cat > retrieve_invoices.py << 'EOF'
import json
from typing import Any, Dict, Optional, List
from tau_bench.envs.tool import Tool

class RetrieveInvoices(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], invoice_ids: Optional[List[str]] = None) -> str:
        invoices = data.get("invoices", {})
        results = []
        
        if invoice_ids:
            # Retrieve specific invoices
            for invoice_id in invoice_ids:
                if str(invoice_id) in invoices:
                    results.append(invoices[str(invoice_id)])
        else:
            # Retrieve all invoices
            results = list(invoices.values())
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "retrieve_invoices",
                "description": "Retrieve specific invoices by IDs or all invoices",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "invoice_ids": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of invoice IDs to retrieve. If not provided, returns all invoices"
                        }
                    },
                    "required": []
                }
            }
        }
EOF

# summary_of_instrument_types_by_prices.py
cat > summary_of_instrument_types_by_prices.py << 'EOF'
import json
from typing import Any, Dict, Optional
from collections import defaultdict
from tau_bench.envs.tool import Tool

class SummaryOfInstrumentTypesByPrices(Tool):
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
        
        for price in instrument_prices.values():
            # Filter by date if specified
            if price_date and price.get("price_date") != price_date:
                continue
            
            instrument_id = price.get("instrument_id")
            if not instrument_id or str(instrument_id) not in instruments:
                continue
            
            instrument = instruments[str(instrument_id)]
            inst_type = instrument.get("instrument_type")
            
            # Filter by instrument type if specified
            if instrument_type and inst_type != instrument_type:
                continue
            
            close_price = float(price.get("close_price", 0))
            
            summary[inst_type]["count"] += 1
            summary[inst_type]["total_close_price"] += close_price
            summary[inst_type]["min_close_price"] = min(summary[inst_type]["min_close_price"], close_price)
            summary[inst_type]["max_close_price"] = max(summary[inst_type]["max_close_price"], close_price)
            
            # Track instrument details
            summary[inst_type]["instruments"].append({
                "instrument_id": instrument_id,
                "ticker": instrument.get("ticker"),
                "name": instrument.get("name"),
                "close_price": close_price,
                "price_date": price.get("price_date")
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
                        "price_date": {"type": "string", "description": "Filter by specific price date (YYYY-MM-DD)"},
                        "instrument_type": {"type": "string", "description": "Filter by specific instrument type"}
                    },
                    "required": []
                }
            }
        }
EOF

# remove_holding.py
cat > remove_holding.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class RemoveHolding(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], holding_id: str) -> str:
        portfolio_holdings = data.get("portfolio_holdings", {})
        
        # Validate holding exists
        if str(holding_id) not in portfolio_holdings:
            raise ValueError(f"Holding {holding_id} not found")
        
        # Get holding details before deletion
        deleted_holding = portfolio_holdings.pop(str(holding_id))
        
        return json.dumps({
            "status": "removed",
            "removed_holding": deleted_holding
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "remove_holding",
                "description": "Remove a holding from a portfolio",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "holding_id": {"type": "string", "description": "ID of the holding to remove"}
                    },
                    "required": ["holding_id"]
                }
            }
        }
EOF

echo "All fund management tools have been created successfully!"
echo "Created files:"
echo "- create_invoice.py"
echo "- delete_invoice.py" 
echo "- get_invoices.py"
echo "- update_invoice.py"
echo "- retrieve_invoices.py"
echo "- summary_of_instrument_types_by_prices.py"
echo "- remove_holding.py"