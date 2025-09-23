from tau_bench.types import Action, Task

INTERFACE_3_TEST = [
    Task(
        annotator="1",
        user_id="2",
        instruction=(
            "You are Maria Garcia, a Compliance Officer. You need to onboard a new institutional investor, "
            "create a new portfolio for them, and process their initial subscription to a fund. "
            "Separately, you must handle an approved redemption request for another investor."
        ),
        actions=[
            Action(name="register_investor", kwargs={
                "legal_name": "Venture Holdings Inc.",
                "source_of_funds": "shareholder_capital",
                "contact_email": "contact@ventureholdings.com",
                "accreditation_status": "accredited",
                "country_of_incorporation": "USA",
                "tax_id": "VH987654321"
            }),
            Action(name="manipulate_portfolio", kwargs={
                "action": "create",
                "portfolio_data": {
                    "investor_id": "10",
                    "status": "active",
                    "fund_manager_approval": True,
                    "compliance_officer_approval": True
                }
            }),
            Action(name="manipulate_subscription", kwargs={
                "action": "create",
                "subscription_data": {
                    "fund_id": "2",
                    "investor_id": "10",
                    "amount": 250000.00,
                    "request_assigned_to": "2",
                    "request_date": "2025-09-22",
                    "status": "approved",
                    "fund_manager_approval": True
                }
            }),
            Action(name="complete_redemption", kwargs={
                "redemption_id": "201",
                "status": "processed",
                "processed_date": "2025-09-22"
            })
        ],
        outputs=[]
    )
]