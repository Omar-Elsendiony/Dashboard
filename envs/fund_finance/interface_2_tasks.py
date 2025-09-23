from tau_bench.types import Action, Task

INTERFACE_2_TEST = [
    Task(
        annotator="2",
        user_id="3",
        instruction=(
            "You are Sarah Wilson, a Portfolio Manager. You need to manage investor portfolios and subscriptions. "
            "Check approval, add an investor, handle portfolio operations, and process subscription."
        ),
        actions=[
            Action(name="check_approval", kwargs={
                "action": "investor_onboarding",
                "requester_email": "sarah.wilson@company.com"
            }),
            Action(name="add_investor", kwargs={
                "legal_name": "Global Investment Partners",
                "source_of_funds": "institutional_capital",
                "contact_email": "contact@globalip.com",
                "accreditation_status": "accredited",
                "country_of_incorporation": "UK",
                "tax_id": "GIP987654321"
            }),
            Action(name="handle_portfolio", kwargs={
                "action": "create",
                "portfolio_data": {
                    "investor_id": "11",
                    "name": "Global Growth Portfolio",
                    "status": "active"
                }
            }),
            Action(name="handle_subscription", kwargs={
                "action": "create",
                "subscription_data": {
                    "fund_id": "2",
                    "investor_id": "11",
                    "amount": 500000.00,
                    "currency": "USD",
                    "status": "pending"
                }
            }),
            Action(name="create_report", kwargs={
                "report_type": "portfolio",
                "investor_id": "11"
            })
        ],
        outputs=[]
    )
]