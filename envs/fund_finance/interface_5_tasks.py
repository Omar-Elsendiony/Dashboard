from tau_bench.types import Action, Task

INTERFACE_5_TEST = [
    Task(
        annotator="5",
        user_id="5",
        instruction=(
            "You are Lisa Rodriguez, an Investor Relations Manager. You need to manage investor communications "
            "and document storage. Check approval, generate investor records, process portfolio data, and store documents."
        ),
        actions=[
            Action(name="authorization_check", kwargs={
                "action": "investor_communication",
                "requester_email": "lisa.rodriguez@company.com"
            }),
            Action(name="generate_investor", kwargs={
                "legal_name": "Sovereign Wealth Partners",
                "source_of_funds": "sovereign_funds",
                "contact_email": "contact@swpartners.com",
                "accreditation_status": "accredited",
                "country_of_incorporation": "Norway",
                "tax_id": "SWP789123456"
            }),
            Action(name="process_portfolio", kwargs={
                "action": "create",
                "portfolio_data": {
                    "investor_id": "13",
                    "name": "Sovereign Growth Portfolio",
                    "status": "active"
                }
            }),
            Action(name="process_notifications", kwargs={
                "action": "create",
                "notification_data": {
                    "email": "contact@swpartners.com",
                    "type": "report",
                    "message": "Your quarterly report is ready"
                }
            }),
            Action(name="store_document", kwargs={
                "document_name": "Quarterly Report Q3 2025",
                "document_type": "pdf",
                "uploaded_by": "5",
                "status": "available"
            })
        ],
        outputs=[]
    )
]