from tau_bench.types import Action, Task

INTERFACE_1_TEST = [
    Task(
        annotator="1",
        user_id="1",
        instruction=(
            "You are John Johnson, a Fund Manager. You need to manage fund operations and trading activities. "
            "First, check your approval status, then create a new investor, manage a fund, execute a trade, "
            "and generate a report."
        ),
        actions=[
            Action(name="approval_lookup", kwargs={
                "action": "fund_management_setup",
                "requester_email": "johnjohnson@gmail.com"
            }),
            Action(name="create_investor", kwargs={
                "legal_name": "Technology Ventures Inc.",
                "source_of_funds": "corporate_capital",
                "contact_email": "contact@techventures.com",
                "accreditation_status": "accredited",
                "country_of_incorporation": "USA",
                "tax_id": "TV123456789"
            }),
            Action(name="manage_fund", kwargs={
                "action": "create",
                "fund_data": {
                    "name": "Tech Growth Fund",
                    "fund_type": "equity",
                    "base_currency": "USD",
                    "size": 10000000.0,
                    "status": "open",
                    "manager_id": "1"
                }
            }),
            Action(name="execute_trade", kwargs={
                "fund_id": "1",
                "instrument_id": "1",
                "quantity": 1000,
                "price": 150.50,
                "side": "buy"
            }),
            Action(name="generate_report", kwargs={
                "report_type": "performance",
                "fund_id": "1"
            })
        ],
        outputs=[]
    )
]