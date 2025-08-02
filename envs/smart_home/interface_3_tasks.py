from tau_bench.types import Action, Task

INTERFACE_3_TEST = [
    Task(
        annotator="0",
        user_id="3",
        instruction=(
            "You are Karren Wheeler with the email \"alyssa.wilson@gmail.com\", a smart home system manager. "
            "You're managing your smart home system and want to optimize device usage. "
            "First, you need to check your user profile and get information about your home. "
            "Then you want to see what devices are available in your bedroom area. "
            "After that, you want to turn on a bulb device and adjust a thermostat for comfortable temperature. "
            "You also want to check what rooms are available in your home for future device management. "
            "Finally, you want to create an automated routine that will help manage your daily home automation."
        ),
        actions=[
            Action(name="get_user_info", kwargs={
                "user_id": "3"
            }),
            Action(name="get_home_info", kwargs={
                "home_id": "3"
            }),
            Action(name="get_devices_info", kwargs={
                "room_id": "10"
            }),
            Action(name="update_device_info", kwargs={
                "device_id": "41",
                "status": "on",
                "brightness_level": "80"
            }),
            Action(name="update_device_info", kwargs={
                "device_id": "46",
                "status": "on"
            }),
            Action(name="get_rooms_info", kwargs={
                "home_id": "3"
            }),
            Action(name="create_routine", kwargs={
                "user_id": 3,
                "home_id": 3,
                "action_time": "19:30",
                "start_action_date": "2025-08-01",
                "action_interval": "daily"
            })
        ],
        outputs=[]
    )
]
