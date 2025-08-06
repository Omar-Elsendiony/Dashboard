from tau_bench.types import Action, Task

INTERFACE_3_TEST = [
    Task(
        annotator="0",
        user_id="1",
        instruction=(
            "You are John Johnson with the email \"johnjohnson@gmail.com\", a financial analyst. "
            "You need to manage portfolio holdings and instrument data. First, verify your user profile "
            "and find information about available instruments. Then, add a new instrument to the system "
            "called 'Microsoft Corporation' with symbol 'MSFT'. After that, add pricing information for this instrument, "
            "create a new portfolio holding, and generate a performance report. Finally, email the user "
            "with a summary of the portfolio activities."
        ),
        actions=[
            Action(name="find_user", kwargs={
                "email": "johnjohnson@gmail.com"
            }),
            Action(name="retrieve_instruments", kwargs={
                "status": "active"
            }),
            Action(name="add_new_instrument", kwargs={
                "symbol": "MSFT",
                "name": "Microsoft Corporation",
                "instrument_type": "stock",
                "currency": "USD"
            }),
            Action(name="add_new_instrument_price", kwargs={
                "instrument_id": "1",
                "price": 335.75,
                "currency": "USD"
            }),
            Action(name="add_new_holding", kwargs={
                "portfolio_id": "1",
                "instrument_id": "1",
                "quantity": 50,
                "unit_cost": 335.75
            }),
            Action(name="generate_report", kwargs={
                "report_type": "performance",
                "fund_id": "2",
                "report_date": "2025-08-06"
            }),
            Action(name="email_user", kwargs={
                "user_id": "1",
                "subject": "Portfolio Holdings Update",
                "message": "New instrument added and portfolio holdings updated successfully"
            })
        ],
        outputs=[]
    )
]
