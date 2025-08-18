from tau_bench.types import Action, Task

INTERFACE_1_TEST = [
    Task(
        annotator="0",
        user_id="1",
        instruction=(
            "You are John Johnson with the email \"johnjohnson@gmail.com\", a fund manager. "
            "You need to manage fund operations and trading activities. First, get information about "
            "available funds and create a new fund called 'Tech Growth Fund' as a hedge fund with "
            "initial size of 5,000,000. After that, get available instruments and execute a buy trade "
            "for the new fund. Then calculate the NAV for the fund and add an audit trail for the operations."
        ),
        actions=[
            Action(name="retrieve_available_funds", kwargs={}),
            Action(name="create_fund", kwargs={
                "fund_name": "Tech Growth Fund",
                "fund_type": "hedge_funds",
                "initial_size": 5000000.0,
                "manager_id": "1",
                "compliance_officer_review": True,
                "fund_manager_approval": True
            }),
            Action(name="retrieve_instruments", kwargs={}),
            Action(name="execute_trade", kwargs={
                "fund_id": "1",
                "instrument_id": "1",
                "trade_type": "buy",
                "quantity": 1000,
                "price": 150.50
            }),
            Action(name="compute_nav", kwargs={
                "fund_id": "1",
                "calculation_date": "2025-08-17"
            }),
            Action(name="add_audit_trail", kwargs={
                "reference_id": "1",
                "reference_type": "fund",
                "action": "create"
            })
        ],
        outputs=[]
    ),
    Task(
        annotator="1",
        user_id="2", 
        instruction=(
            "You are William Robinson, a fund manager. You need to monitor fund performance and "
            "trading activities. First, list available funds and get the daily profit/loss for "
            "a specific fund. Then check fund instruments and their pricing information. "
            "Update an instrument price and get the fund's NAV history."
        ),
        actions=[
            Action(name="list_funds_with_filter", kwargs={"status": "open"}),
            Action(name="get_daily_profit_loss_by_fund", kwargs={
                "fund_id": "1",
                "trade_date": "2025-08-17"
            }),
            Action(name="retrieve_fund_instruments", kwargs={"fund_id": "1"}),
            Action(name="retrieve_instruments_prices", kwargs={}),
            Action(name="update_instrument_price", kwargs={
                "instrument_id": "1",
                "new_price": 155.75,
                "price_date": "2025-08-17"
            }),
            Action(name="get_fund_nav_history", kwargs={"fund_id": "1"})
        ],
        outputs=[]
    )
]
