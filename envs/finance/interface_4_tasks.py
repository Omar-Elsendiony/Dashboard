from tau_bench.types import Action, Task

INTERFACE_4_TEST = [
    Task(
        annotator="0",
        user_id="1",
        instruction=(
            "You are John Johnson, a fund analyst. You need to perform fund analysis and performance "
            "monitoring. First, add a new user, then get available funds and create a new fund for "
            "analysis. After that, calculate NAV, get performance history, and analyze daily profit/loss. "
            "Finally, generate analytical reports and create documentation."
        ),
        actions=[
            Action(name="add_new_user", kwargs={
                "first_name": "Michael",
                "last_name": "Chen",
                "email": "michael.chen@analytics.com",
                "role": "fund_manager",
                "timezone": "PST",
                "status": "active"
            }),
            Action(name="list_funds_with_filter", kwargs={"status": "open"}),
            Action(name="create_fund", kwargs={
                "fund_name": "Global Analytics Fund",
                "fund_type": "mutual_funds",
                "initial_size": 2000000.0,
                "manager_id": "1",
                "compliance_officer_review": True,
                "fund_manager_approval": True
            }),
            Action(name="calculate_nav", kwargs={
                "fund_id": "1",
                "calculation_date": "2025-08-17"
            }),
            Action(name="get_performance_history", kwargs={
                "fund_code": "1",
                "start_date": "2025-07-01",
                "end_date": "2025-08-17"
            }),
            Action(name="get_daily_profit_loss_by_fund", kwargs={
                "fund_id": "1",
                "trade_date": "2025-08-17"
            }),
            Action(name="generate_report", kwargs={
                "report_type": "performance",
                "period": "2025-08",
                "requester_role": "fund_manager",
                "fund_id": "1"
            })
        ],
        outputs=[]
    ),
    Task(
        annotator="1",
        user_id="2",
        instruction=(
            "You are William Robinson, a performance analyst. You need to analyze fund instruments "
            "and market data. First, get fund instruments and their pricing information, then "
            "get growth rates and calculate future values. After that, generate summary reports "
            "and update instrument pricing data."
        ),
        actions=[
            Action(name="get_fund_instruments", kwargs={"fund_id": "1"}),
            Action(name="get_instruments_prices", kwargs={}),
            Action(name="get_growth_rate", kwargs={
                "fund_type": "mutual_funds",
                "instrument_type": "equities"
            }),
            Action(name="calculate_future_value", kwargs={
                "closing_price_or_nav": 105.50,
                "growth_rate": 0.08,
                "years": 5
            }),
            Action(name="summary_of_instrument_types_by_prices", kwargs={}),
            Action(name="update_instrument_price", kwargs={
                "instrument_id": "1",
                "new_price": 160.25,
                "price_date": "2025-08-17"
            }),
            Action(name="get_nav_records", kwargs={"fund_id": "1"}),
            Action(name="add_audit_trail", kwargs={
                "reference_id": "1",
                "reference_type": "analytical_calculation",
                "action": "analyze"
            })
        ],
        outputs=[]
    )
]
