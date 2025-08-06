from tau_bench.types import Action, Task

INTERFACE_1_TEST = [
    Task(
        annotator="0",
        user_id="1",
        instruction=(
            "You are John Johnson with the email \"johnjohnson@gmail.com\", a finance administrator. "
            "You need to manage a new investor onboarding process. First, verify your user profile to confirm "
            "your admin access. Then, get information about available funds to show investment options. "
            "After that, onboard a new investor named 'Tech Innovations LLC' with email 'info@techinnovations.com' "
            "as an institutional investor. Once onboarded, create a portfolio for this investor and get their "
            "portfolio information. Finally, subscribe them to an available fund and send a notification to "
            "confirm successful onboarding."
        ),
        actions=[
            Action(name="get_user", kwargs={
                "user_id": "1"
            }),
            Action(name="get_funds", kwargs={
                "status": "open"
            }),
            Action(name="onboard_new_investor", kwargs={
                "name": "Tech Innovations LLC",
                "contact_email": "info@techinnovations.com",
                "investor_type": "institutional",
                "accreditation_status": "accredited"
            }),
            Action(name="create_portfolio", kwargs={
                "investor_id": "1",
                "name": "Tech Innovations Portfolio"
            }),
            Action(name="get_investor_portfolio", kwargs={
                "investor_id": "1"
            }),
            Action(name="subscribe_investor_to_fund", kwargs={
                "investor_id": "1",
                "fund_id": "2",
                "amount": 500000
            }),
            Action(name="send_notification", kwargs={
                "user_id": "1",
                "message": "Successfully onboarded Tech Innovations LLC and created investment portfolio",
                "notification_type": "update"
            })
        ],
        outputs=[]
    )
]
