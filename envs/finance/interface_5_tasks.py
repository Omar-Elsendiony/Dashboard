from tau_bench.types import Action, Task

INTERFACE_5_TEST = [
    Task(
        annotator="0",
        user_id="1",
        instruction=(
            "You are John Johnson, an investor relations manager. You need to handle comprehensive "
            "investor services. First, find user information and get filtered investors, then "
            "onboard a new investor and create a subscription. After that, manage their portfolio "
            "and create invoices with payment processing."
        ),
        actions=[
            Action(name="find_user", kwargs={"email": "johnjohnson@gmail.com"}),
            Action(name="get_filtered_investors", kwargs={}),
            Action(name="investor_onboarding", kwargs={
                "legal_entity_name": "Global Investment Partners LLC",
                "incorporation_registration_number": "LLC789012",
                "date_of_incorporation": "2019-03-10",
                "country_of_incorporation": "United States",
                "registered_business_address": "456 Finance Street, New York, NY 10001",
                "tax_identification_number": "98-7654321",
                "source_of_funds_declaration": "Institutional investment capital",
                "compliance_officer_approval": True
            }),
            Action(name="create_subscription", kwargs={
                "investor_id": "1",
                "fund_id": "1",
                "amount": 1000000.0,
                "compliance_officer_approval": True
            }),
            Action(name="get_investor_portfolio", kwargs={"investor_id": "1"}),
            Action(name="create_invoice", kwargs={
                "investor_id": "1",
                "amount": 1000000.0,
                "due_date": "2025-09-17",
                "description": "Initial subscription payment"
            }),
            Action(name="send_email_notification", kwargs={
                "user_id": "1",
                "notification_type": "subscription_update",
                "notification_class": "investors"
            })
        ],
        outputs=[]
    ),
    Task(
        annotator="1",
        user_id="2",
        instruction=(
            "You are William Robinson, a portfolio manager. You need to manage investor portfolios "
            "and communication. First, get investor profile and portfolio holdings, then get "
            "transaction history and statements. After that, manage invoice configurations and "
            "deactivate/reactivate instruments as needed."
        ),
        actions=[
            Action(name="get_investor_profile", kwargs={"investor_id": "1"}),
            Action(name="get_investor_portfolio_holdings", kwargs={"investor_id": "1"}),
            Action(name="get_investor_transactions_history", kwargs={"investor_id": "1"}),
            Action(name="get_investor_statements", kwargs={"investor_id": "1"}),
            Action(name="modify_invoice_config", kwargs={
                "invoice_id": "1",
                "due_date": "2025-10-17"
            }),
            Action(name="deactivate_reactivate_instrument", kwargs={
                "instrument_id": "1",
                "action": "deactivate"
            }),
            Action(name="get_notifications", kwargs={
                "user_id": "2",
                "notification_class": "portfolios"
            }),
            Action(name="add_audit_trail", kwargs={
                "reference_id": "1",
                "reference_type": "investor",
                "action": "update"
            })
        ],
        outputs=[]
    )
]
