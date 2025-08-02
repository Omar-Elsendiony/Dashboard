tasks = [
    {
        "annotator": 0,
        "user_id": "user_john_homeowner_001",
        "instruction": (
            "You are John Smith, a homeowner with the email 'john.smith@email.com'. You want to set up energy "
            "monitoring for your smart home. First, you need to verify your user profile and get your home details. "
            "Then, you want to check all the devices in your home and see their current energy consumption. "
            "After that, you want to create a routine that automatically turns off all lights at 11 PM to save energy. "
            "Finally, you want to add feedback about the energy monitoring system with a rating of 4 stars and "
            "comment 'Great energy tracking feature, helps me save on electricity bills'."
        ),
        "actions": [
            {"name": "get_user_info", "arguments": {"user_id": "user_john_homeowner_001"}},
            {"name": "get_home_info", "arguments": {"home_id": "home_suburban_001"}},
            {"name": "get_devices_info", "arguments": {"home_id": "home_suburban_001"}},
            {"name": "get_historical_energy_consumption_by_device", "arguments": {"device_id": "device_smart_bulb_001", "start_date": "2025-07-01", "end_date": "2025-07-31"}},
            {"name": "create_routine", "arguments": {"user_id": "user_john_homeowner_001", "name": "Nightly Energy Saver", "description": "Turn off all lights at 11 PM", "trigger_time": "23:00", "actions": [{"device_id": "device_smart_bulb_001", "action": "turn_off"}]}},
            {"name": "add_feedback", "arguments": {"user_id": "user_john_homeowner_001", "device_id": "energy_monitor_001", "rating": 4, "comment": "Great energy tracking feature, helps me save on electricity bills"}},
        ],
    }
]
