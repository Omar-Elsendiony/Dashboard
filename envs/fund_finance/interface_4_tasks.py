from tau_bench.types import Action, Task

INTERFACE_4_TEST = [
    Task(
        annotator="4",
        user_id="4",
        instruction=(
            "You are Michael Chen, a Risk Manager. You need to analyze fund performance and manage risk. "
            "Verify approval, record investor data, address portfolio issues, and produce analysis reports."
        ),
        actions=[
            Action(name="verify_approval", kwargs={
                "action": "portfolio_update",
                "requester_email": "michael.chen@company.com"
            }),
            Action(name="record_investor", kwargs={
                "legal_name": "Pension Fund Associates",
                "source_of_funds": "pension_contributions",
                "contact_email": "contact@pensionfund.com",
                "accreditation_status": "accredited",
                "country_of_incorporation": "Canada",
                "tax_id": "PFA456789123"
            }),
            Action(name="address_portfolio", kwargs={
                "action": "update",
                "portfolio_data": {
                    "portfolio_id": "12",
                    "status": "active",
                    "risk_level": "moderate"
                }
            }),
            Action(name="address_nav_record", kwargs={
                "action": "create",
                "nav_data": {
                    "fund_id": "3",
                    "nav_value": 105.75,
                    "nav_date": "2025-09-22"
                }
            }),
            Action(name="compile_report", kwargs={
                "report_type": "risk",
                "fund_id": "3"
            })
        ],
        outputs=[]
    )
]