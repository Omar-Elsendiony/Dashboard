tasks = [
    {
        "annotator": 0,
        "user_id": "1",
        "instruction": (
            "You are John Johnson, a fund manager with the email 'johnjohnson@gmail.com'. You need to "
            "manage fund operations and trading activities. First, get information about available funds "
            "and create a new fund called 'Tech Growth Fund' as a hedge fund with initial size of 5,000,000. "
            "After that, get available instruments and execute a buy trade for the new fund. Then calculate "
            "the NAV for the fund and add an audit trail for the operations."
        ),
        "actions": [
            {"name": "get_available_funds", "arguments": {}},
            {"name": "create_fund", "arguments": {
                "fund_name": "Tech Growth Fund",
                "fund_type": "hedge_funds",
                "initial_size": 5000000.0,
                "manager_id": "1",
                "compliance_officer_review": True,
                "fund_manager_approval": True
            }},
            {"name": "get_instruments", "arguments": {}},
            {"name": "execute_trade", "arguments": {
                "fund_id": "1",
                "instrument_id": "1",
                "trade_type": "buy",
                "quantity": 1000,
                "price": 150.50
            }},
            {"name": "calculate_nav", "arguments": {
                "fund_id": "1",
                "calculation_date": "2025-08-17"
            }},
            {"name": "add_audit_trail", "arguments": {
                "reference_id": "1",
                "reference_type": "fund",
                "action": "create"
            }}
        ],
    },
    {
        "annotator": 1,
        "user_id": "2",
        "instruction": (
            "You are William Robinson, a fund manager. You need to monitor fund performance and trading "
            "activities. First, list available funds and get the daily profit/loss for a specific fund. "
            "Then check fund instruments and their pricing information. Update an instrument price and "
            "get the fund's NAV history."
        ),
        "actions": [
            {"name": "list_funds_with_filter", "arguments": {"status": "open"}},
            {"name": "get_daily_profit_loss_by_fund", "arguments": {
                "fund_id": "1",
                "trade_date": "2025-08-17"
            }},
            {"name": "get_fund_instruments", "arguments": {"fund_id": "1"}},
            {"name": "get_instruments_prices", "arguments": {}},
            {"name": "update_instrument_price", "arguments": {
                "instrument_id": "1",
                "new_price": 155.75,
                "price_date": "2025-08-17"
            }},
            {"name": "get_fund_nav_history", "arguments": {"fund_id": "1"}}
        ],
    }
]
