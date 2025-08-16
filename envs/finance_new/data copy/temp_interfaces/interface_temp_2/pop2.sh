#!/bin/bash

# Create directory for tools
mkdir -p fund_tools
cd fund_tools

# Create subscribe_investor_to_fund.py
cat > subscribe_investor_to_fund.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class SubscribeInvestorToFund(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str, investor_id: str, 
               amount: str, request_assigned_to: str, request_date: str,
               payment_id: Optional[str] = None, status: str = "pending") -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        funds = data.get("funds", {})
        investors = data.get("investors", {})
        users = data.get("users", {})
        subscriptions = data.get("subscriptions", {})
        
        # Validate fund exists
        if str(fund_id) not in funds:
            raise ValueError(f"Fund {fund_id} not found")
        
        # Validate investor exists
        if str(investor_id) not in investors:
            raise ValueError(f"Investor {investor_id} not found")
        
        # Validate assigned user exists
        if str(request_assigned_to) not in users:
            raise ValueError(f"User {request_assigned_to} not found")
        
        # Validate status
        valid_statuses = ["pending", "approved", "cancelled"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        subscription_id = generate_id(subscriptions)
        timestamp = "2025-10-01T00:00:00"
        
        new_subscription = {
            "subscription_id": subscription_id,
            "fund_id": fund_id,
            "investor_id": investor_id,
            "payment_id": payment_id,
            "amount": amount,
            "status": status,
            "request_assigned_to": request_assigned_to,
            "request_date": request_date,
            "approval_date": None,
            "updated_at": timestamp
        }
        
        subscriptions[str(subscription_id)] = new_subscription
        return json.dumps({"subscription_id": subscription_id})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "subscribe_investor_to_fund",
                "description": "Subscribe an investor to a fund",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "ID of the fund"},
                        "investor_id": {"type": "string", "description": "ID of the investor"},
                        "amount": {"type": "string", "description": "Subscription amount"},
                        "request_assigned_to": {"type": "string", "description": "ID of the user assigned to process the request"},
                        "request_date": {"type": "string", "description": "Date of the subscription request"},
                        "payment_id": {"type": "string", "description": "ID of the payment (optional)"},
                        "status": {"type": "string", "description": "Status of subscription (pending, approved, cancelled), defaults to pending"}
                    },
                    "required": ["fund_id", "investor_id", "amount", "request_assigned_to", "request_date"]
                }
            }
        }
EOF

# Create get_subscriptions.py
cat > get_subscriptions.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetSubscriptions(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: Optional[str] = None, 
               investor_id: Optional[str] = None, status: Optional[str] = None,
               request_assigned_to: Optional[str] = None) -> str:
        subscriptions = data.get("subscriptions", {})
        results = []
        
        for subscription in subscriptions.values():
            if fund_id and subscription.get("fund_id") != fund_id:
                continue
            if investor_id and subscription.get("investor_id") != investor_id:
                continue
            if status and subscription.get("status") != status:
                continue
            if request_assigned_to and subscription.get("request_assigned_to") != request_assigned_to:
                continue
            results.append(subscription)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_subscriptions",
                "description": "Get subscriptions with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "Filter by fund ID"},
                        "investor_id": {"type": "string", "description": "Filter by investor ID"},
                        "status": {"type": "string", "description": "Filter by status (pending, approved, cancelled)"},
                        "request_assigned_to": {"type": "string", "description": "Filter by assigned user ID"}
                    },
                    "required": []
                }
            }
        }
EOF

# Create update_subscription.py
cat > update_subscription.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateSubscription(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], subscription_id: str, 
               status: Optional[str] = None, approval_date: Optional[str] = None,
               amount: Optional[str] = None, payment_id: Optional[str] = None) -> str:
        
        subscriptions = data.get("subscriptions", {})
        
        # Validate subscription exists
        if str(subscription_id) not in subscriptions:
            raise ValueError(f"Subscription {subscription_id} not found")
        
        subscription = subscriptions[str(subscription_id)]
        
        # Validate status if provided
        if status:
            valid_statuses = ["pending", "approved", "cancelled"]
            if status not in valid_statuses:
                raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
            subscription["status"] = status
        
        # Update fields if provided
        if approval_date:
            subscription["approval_date"] = approval_date
        if amount:
            subscription["amount"] = amount
        if payment_id:
            subscription["payment_id"] = payment_id
        
        # Update timestamp
        subscription["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps(subscription)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_subscription",
                "description": "Update a subscription record",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "subscription_id": {"type": "string", "description": "ID of the subscription to update"},
                        "status": {"type": "string", "description": "New status (pending, approved, cancelled)"},
                        "approval_date": {"type": "string", "description": "Date of approval"},
                        "amount": {"type": "string", "description": "New subscription amount"},
                        "payment_id": {"type": "string", "description": "ID of associated payment"}
                    },
                    "required": ["subscription_id"]
                }
            }
        }
EOF

# Create create_commitment.py
cat > create_commitment.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateCommitment(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str, investor_id: str,
               commitment_amount: str, commitment_date: str, 
               status: str = "pending") -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        funds = data.get("funds", {})
        investors = data.get("investors", {})
        commitments = data.get("commitments", {})
        
        # Validate fund exists
        if str(fund_id) not in funds:
            raise ValueError(f"Fund {fund_id} not found")
        
        # Validate investor exists
        if str(investor_id) not in investors:
            raise ValueError(f"Investor {investor_id} not found")
        
        # Validate status
        valid_statuses = ["pending", "fulfilled"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        commitment_id = generate_id(commitments)
        timestamp = "2025-10-01T00:00:00"
        
        new_commitment = {
            "commitment_id": commitment_id,
            "fund_id": fund_id,
            "investor_id": investor_id,
            "commitment_amount": commitment_amount,
            "commitment_date": commitment_date,
            "status": status,
            "updated_at": timestamp
        }
        
        commitments[str(commitment_id)] = new_commitment
        return json.dumps({"commitment_id": commitment_id})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_commitment",
                "description": "Create a new commitment for capital raising",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "ID of the fund"},
                        "investor_id": {"type": "string", "description": "ID of the investor"},
                        "commitment_amount": {"type": "string", "description": "Amount of the commitment"},
                        "commitment_date": {"type": "string", "description": "Date of the commitment"},
                        "status": {"type": "string", "description": "Status of commitment (pending, fulfilled), defaults to pending"}
                    },
                    "required": ["fund_id", "investor_id", "commitment_amount", "commitment_date"]
                }
            }
        }
EOF

# Create get_commitments.py
cat > get_commitments.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetCommitments(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: Optional[str] = None,
               investor_id: Optional[str] = None, status: Optional[str] = None) -> str:
        commitments = data.get("commitments", {})
        results = []
        
        for commitment in commitments.values():
            if fund_id and commitment.get("fund_id") != fund_id:
                continue
            if investor_id and commitment.get("investor_id") != investor_id:
                continue
            if status and commitment.get("status") != status:
                continue
            results.append(commitment)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_commitments",
                "description": "Get commitments with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "Filter by fund ID"},
                        "investor_id": {"type": "string", "description": "Filter by investor ID"},
                        "status": {"type": "string", "description": "Filter by status (pending, fulfilled)"}
                    },
                    "required": []
                }
            }
        }
EOF

# Create check_commitment_fulfillment_status.py
cat > check_commitment_fulfillment_status.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CheckCommitmentFulfillmentStatus(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], commitment_id: str) -> str:
        commitments = data.get("commitments", {})
        subscriptions = data.get("subscriptions", {})
        
        # Validate commitment exists
        if str(commitment_id) not in commitments:
            raise ValueError(f"Commitment {commitment_id} not found")
        
        commitment = commitments[str(commitment_id)]
        commitment_amount = float(commitment.get("commitment_amount", 0))
        fund_id = commitment.get("fund_id")
        investor_id = commitment.get("investor_id")
        
        # Calculate fulfilled amount from approved subscriptions
        fulfilled_amount = 0
        related_subscriptions = []
        
        for subscription in subscriptions.values():
            if (subscription.get("fund_id") == fund_id and 
                subscription.get("investor_id") == investor_id and
                subscription.get("status") == "approved"):
                fulfilled_amount += float(subscription.get("amount", 0))
                related_subscriptions.append(subscription["subscription_id"])
        
        # Calculate fulfillment percentage
        fulfillment_percentage = (fulfilled_amount / commitment_amount * 100) if commitment_amount > 0 else 0
        
        # Determine if fully fulfilled
        is_fully_fulfilled = fulfillment_percentage >= 100
        
        result = {
            "commitment_id": commitment_id,
            "commitment_amount": commitment_amount,
            "fulfilled_amount": fulfilled_amount,
            "remaining_amount": commitment_amount - fulfilled_amount,
            "fulfillment_percentage": round(fulfillment_percentage, 2),
            "is_fully_fulfilled": is_fully_fulfilled,
            "status": commitment.get("status"),
            "related_subscriptions": related_subscriptions
        }
        
        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "check_commitment_fulfillment_status",
                "description": "Check the fulfillment status of a commitment including calculation of fulfilled amounts",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "commitment_id": {"type": "string", "description": "ID of the commitment to check"}
                    },
                    "required": ["commitment_id"]
                }
            }
        }
EOF

# Create register_payment.py
cat > register_payment.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class RegisterPayment(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], invoice_id: str, payment_date: str,
               amount: str, payment_method: str, status: str = "draft") -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        invoices = data.get("invoices", {})
        payments = data.get("payments", {})
        
        # Validate invoice exists
        if str(invoice_id) not in invoices:
            raise ValueError(f"Invoice {invoice_id} not found")
        
        # Validate payment method
        valid_methods = ["wire", "cheque", "credit_card", "bank_transfer"]
        if payment_method not in valid_methods:
            raise ValueError(f"Invalid payment method. Must be one of {valid_methods}")
        
        # Validate status
        valid_statuses = ["draft", "completed", "failed"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        payment_id = generate_id(payments)
        timestamp = "2025-10-01T00:00:00"
        
        new_payment = {
            "payment_id": payment_id,
            "invoice_id": invoice_id,
            "payment_date": payment_date,
            "amount": amount,
            "payment_method": payment_method,
            "status": status,
            "created_at": timestamp
        }
        
        payments[str(payment_id)] = new_payment
        return json.dumps({"payment_id": payment_id})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "register_payment",
                "description": "Register a new payment against an invoice",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "invoice_id": {"type": "string", "description": "ID of the invoice"},
                        "payment_date": {"type": "string", "description": "Date of payment"},
                        "amount": {"type": "string", "description": "Payment amount"},
                        "payment_method": {"type": "string", "description": "Payment method (wire, cheque, credit_card, bank_transfer)"},
                        "status": {"type": "string", "description": "Payment status (draft, completed, failed), defaults to draft"}
                    },
                    "required": ["invoice_id", "payment_date", "amount", "payment_method"]
                }
            }
        }
EOF

# Create get_payment_history.py
cat > get_payment_history.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetPaymentHistory(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], invoice_id: Optional[str] = None,
               payment_method: Optional[str] = None, status: Optional[str] = None,
               start_date: Optional[str] = None, end_date: Optional[str] = None) -> str:
        payments = data.get("payments", {})
        results = []
        
        for payment in payments.values():
            if invoice_id and payment.get("invoice_id") != invoice_id:
                continue
            if payment_method and payment.get("payment_method") != payment_method:
                continue
            if status and payment.get("status") != status:
                continue
            if start_date and payment.get("payment_date", "") < start_date:
                continue
            if end_date and payment.get("payment_date", "") > end_date:
                continue
            results.append(payment)
        
        # Sort by payment_date descending (most recent first)
        results.sort(key=lambda x: x.get("payment_date", ""), reverse=True)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_payment_history",
                "description": "Get payment history with optional filters for reconciliation and audit",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "invoice_id": {"type": "string", "description": "Filter by invoice ID"},
                        "payment_method": {"type": "string", "description": "Filter by payment method (wire, cheque, credit_card, bank_transfer)"},
                        "status": {"type": "string", "description": "Filter by status (draft, completed, failed)"},
                        "start_date": {"type": "string", "description": "Filter payments from this date onwards"},
                        "end_date": {"type": "string", "description": "Filter payments up to this date"}
                    },
                    "required": []
                }
            }
        }
EOF

# Create record_payment.py
cat > record_payment.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class RecordPayment(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], payment_id: str, status: str) -> str:
        payments = data.get("payments", {})
        
        # Validate payment exists
        if str(payment_id) not in payments:
            raise ValueError(f"Payment {payment_id} not found")
        
        # Validate status
        valid_statuses = ["draft", "completed", "failed"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        payment = payments[str(payment_id)]
        payment["status"] = status
        
        # If completing payment, update related invoice status
        if status == "completed":
            invoices = data.get("invoices", {})
            invoice_id = payment.get("invoice_id")
            if invoice_id and str(invoice_id) in invoices:
                invoices[str(invoice_id)]["status"] = "paid"
                invoices[str(invoice_id)]["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps({
            "payment_id": payment_id,
            "status": status,
            "message": f"Payment {payment_id} status updated to {status}"
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "record_payment",
                "description": "Record the final status of a payment for transaction settlement",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "payment_id": {"type": "string", "description": "ID of the payment to update"},
                        "status": {"type": "string", "description": "Final payment status (draft, completed, failed)"}
                    },
                    "required": ["payment_id", "status"]
                }
            }
        }
EOF

# Create create_nav_record.py
cat > create_nav_record.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateNavRecord(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str, nav_date: str, nav_value: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        funds = data.get("funds", {})
        nav_records = data.get("nav_records", {})
        
        # Validate fund exists
        if str(fund_id) not in funds:
            raise ValueError(f"Fund {fund_id} not found")
        
        # Check if NAV record already exists for this fund and date
        for nav_record in nav_records.values():
            if (nav_record.get("fund_id") == fund_id and 
                nav_record.get("nav_date") == nav_date):
                raise ValueError(f"NAV record already exists for fund {fund_id} on date {nav_date}")
        
        nav_id = generate_id(nav_records)
        timestamp = "2025-10-01T00:00:00"
        
        new_nav_record = {
            "nav_id": nav_id,
            "fund_id": fund_id,
            "nav_date": nav_date,
            "nav_value": nav_value,
            "updated_at": timestamp
        }
        
        nav_records[str(nav_id)] = new_nav_record
        return json.dumps({"nav_id": nav_id})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_nav_record",
                "description": "Create a new NAV record for daily valuation (regulatory requirement)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "ID of the fund"},
                        "nav_date": {"type": "string", "description": "Date of NAV calculation"},
                        "nav_value": {"type": "string", "description": "Net Asset Value"}
                    },
                    "required": ["fund_id", "nav_date", "nav_value"]
                }
            }
        }
EOF

# Create get_nav_records.py
cat > get_nav_records.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetNavRecords(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: Optional[str] = None,
               start_date: Optional[str] = None, end_date: Optional[str] = None,
               nav_date: Optional[str] = None) -> str:
        nav_records = data.get("nav_records", {})
        results = []
        
        for nav_record in nav_records.values():
            if fund_id and nav_record.get("fund_id") != fund_id:
                continue
            if nav_date and nav_record.get("nav_date") != nav_date:
                continue
            if start_date and nav_record.get("nav_date", "") < start_date:
                continue
            if end_date and nav_record.get("nav_date", "") > end_date:
                continue
            results.append(nav_record)
        
        # Sort by nav_date descending (most recent first)
        results.sort(key=lambda x: x.get("nav_date", ""), reverse=True)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_nav_records",
                "description": "Get NAV records for performance tracking and reporting",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "Filter by fund ID"},
                        "start_date": {"type": "string", "description": "Filter NAV records from this date onwards"},
                        "end_date": {"type": "string", "description": "Filter NAV records up to this date"},
                        "nav_date": {"type": "string", "description": "Filter by specific NAV date"}
                    },
                    "required": []
                }
            }
        }
EOF

# Create update_nav_record_value.py
cat > update_nav_record_value.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdateNavRecordValue(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], nav_id: str, nav_value: str) -> str:
        nav_records = data.get("nav_records", {})
        
        # Validate NAV record exists
        if str(nav_id) not in nav_records:
            raise ValueError(f"NAV record {nav_id} not found")
        
        nav_record = nav_records[str(nav_id)]
        old_value = nav_record.get("nav_value")
        
        # Update NAV value and timestamp
        nav_record["nav_value"] = nav_value
        nav_record["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps({
            "nav_id": nav_id,
            "fund_id": nav_record.get("fund_id"),
            "nav_date": nav_record.get("nav_date"),
            "old_nav_value": old_value,
            "new_nav_value": nav_value,
            "updated_at": nav_record.get("updated_at")
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_nav_record_value",
                "description": "Update NAV record value for valuation adjustments",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "nav_id": {"type": "string", "description": "ID of the NAV record to update"},
                        "nav_value": {"type": "string", "description": "New NAV value"}
                    },
                    "required": ["nav_id", "nav_value"]
                }
            }
        }
EOF

echo "Fund management tools have been created successfully!"
echo "Created files:"
echo "- subscribe_investor_to_fund.py"
echo "- get_subscriptions.py" 
echo "- update_subscription.py"
echo "- create_commitment.py"
echo "- get_commitments.py"
echo "- check_commitment_fulfillment_status.py"
echo "- register_payment.py"
echo "- get_payment_history.py"
echo "- record_payment.py"
echo "- create_nav_record.py"
echo "- get_nav_records.py"
echo "- update_nav_record_value.py"