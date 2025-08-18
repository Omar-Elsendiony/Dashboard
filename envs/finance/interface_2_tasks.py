from tau_bench.types import Action, Task

INTERFACE_2_TEST = [
    Task(
        annotator="0",
        user_id="1",
        instruction=(
            "You are John Johnson, a compliance officer. You need to manage investor onboarding "
            "and portfolio operations. First, find your user information, then get available funds "
            "and filtered investors. Onboard a new investor 'Tech Innovations LLC' and create a "
            "subscription for them. After that, check their portfolio and add holdings."
        ),
        actions=[
            Action(name="find_user", kwargs={"email": "johnjohnson@gmail.com"}),
            Action(name="get_filtered_investors", kwargs={}),
            Action(name="investor_onboarding", kwargs={
                "legal_entity_name": "Tech Innovations LLC",
                "incorporation_registration_number": "LLC123456",
                "date_of_incorporation": "2020-01-15",
                "country_of_incorporation": "United States",
                "registered_business_address": "123 Innovation Drive, Silicon Valley, CA 94025",
                "tax_identification_number": "12-3456789",
                "source_of_funds_declaration": "Revenue from technology consulting services",
                "compliance_officer_approval": True
            }),
            Action(name="create_subscription", kwargs={
                "investor_id": "1",
                "fund_id": "1",
                "amount": 500000.0,
                "compliance_officer_approval": True
            }),
            Action(name="get_investor_portfolio", kwargs={"investor_id": "1"}),
            Action(name="add_new_holding", kwargs={
                "portfolio_id": "1",
                "fund_id": "1",
                "quantity": 1000,
                "cost_basis": 500.0
            })
        ],
        outputs=[]
    ),
    Task(
        annotator="1",
        user_id="2",
        instruction=(
            "You are William Robinson, a fund manager. You need to manage investor portfolios "
            "and subscriptions. First, get investor profile information and their portfolio holdings. "
            "Then process a redemption for an investor and update their subscription details. "
            "Finally, get investor statements and transaction history."
        ),
        actions=[
            Action(name="get_investor_profile", kwargs={"investor_id": "1"}),
            Action(name="get_investor_portfolio_holdings", kwargs={"investor_id": "1"}),
            Action(name="process_redemption", kwargs={
                "investor_id": "1",
                "fund_id": "1",
                "amount_or_units": 100000.0,
                "compliance_approval": True,
                "finance_approval": True
            }),
            Action(name="update_subscription", kwargs={
                "subscription_id": "1",
                "amount": 400000.0
            }),
            Action(name="get_investor_statements", kwargs={"investor_id": "1"}),
            Action(name="get_investor_transactions_history", kwargs={"investor_id": "1"})
        ],
        outputs=[]
    )
]
