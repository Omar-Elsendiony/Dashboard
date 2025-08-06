tasks = [
    {
        "annotator": 0,
        "user_id": "1",
        "instruction": (
            "You are John Johnson, a finance admin with the email 'johnjohnson@gmail.com'. You want to set up "
            "portfolio management for a new investor. First, you need to verify your user profile and get information "
            "about available funds. Then, you want to onboard a new investor 'Smith & Associates' with email "
            "'contact@smithassociates.com' as a retail investor. After that, you want to create a portfolio for this "
            "investor and subscribe them to the 'Global Alpha Opportunities Fund I'. Finally, you want to send a "
            "notification to confirm their successful onboarding."
        ),
        "actions": [
            {"name": "get_user", "arguments": {"user_id": "1"}},
            {"name": "get_funds", "arguments": {"status": "open"}},
            {"name": "onboard_new_investor", "arguments": {"name": "Smith & Associates", "email": "contact@smithassociates.com", "investor_type": "retail", "accreditation_status": "accredited"}},
            {"name": "create_portfolio", "arguments": {"investor_id": "created_investor_id", "name": "Smith & Associates Portfolio"}},
            {"name": "subscribe_investor_to_fund", "arguments": {"investor_id": "created_investor_id", "fund_id": "1", "amount": 100000}},
            {"name": "send_notification", "arguments": {"user_id": "1", "message": "Successfully onboarded Smith & Associates and created their investment portfolio", "notification_type": "update"}},
        ],
    }
]
