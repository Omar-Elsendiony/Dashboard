from tau_bench.types import Action, Task

INTERFACE_2_TEST = [
    Task(
        annotator="0",
        user_id="2",
        instruction=(
            "You are William Robinson with the email \"williamrobinson@gmail.com\", a fund manager. "
            "You need to manage fund operations and trading activities. First, verify your user profile "
            "and get information about funds you manage. Then, create a new fund called 'Emerging Markets "
            "Equity Fund' as an equity fund with USD base currency. After that, add a new trade for the "
            "fund, update the fund details, and create a NAV record. Finally, notify relevant users about "
            "the new fund creation and trading activity."
        ),
        actions=[
            Action(name="fetch_user_by_mail", kwargs={
                "email": "williamrobinson@gmail.com"
            }),
            Action(name="retrieve_funds_with_filter", kwargs={
                "manager_id": "2"
            }),
            Action(name="create_new_fund", kwargs={
                "name": "Emerging Markets Equity Fund",
                "fund_type": "equity",
                "base_currency": "USD",
                "manager_id": "2",
                "size": 1000000
            }),
            Action(name="add_new_trade_for_fund", kwargs={
                "fund_id": "1",
                "instrument_id": "1",
                "trade_type": "buy",
                "quantity": 1000,
                "price": 150.50
            }),
            Action(name="update_fund_details", kwargs={
                "fund_id": "1",
                "status": "open"
            }),
            Action(name="create_nav_record", kwargs={
                "fund_id": "1",
                "nav_value": 10.50,
                "total_assets": 1050000,
                "total_liabilities": 50000,
                "shares_outstanding": 100000
            }),
            Action(name="notify_user", kwargs={
                "user_id": "2",
                "message": "New fund created and trading activity initiated",
                "notification_type": "alert"
            })
        ],
        outputs=[]
    )
]
