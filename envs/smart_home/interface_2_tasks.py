from tau_bench.types import Action, Task

INTERFACE_2_TEST = [
    Task(
        annotator="0",
        user_id="3",
        instruction=(
            "You are Karren Wheeler with the email \"alyssa.wilson@gmail.com\", a smart home administrator. "
            "You want to manage your smart home security system effectively. "
            "First, check your user profile to confirm your admin access. "
            "Then, get information about all the devices in your kitchen to see what smart devices are available. "
            "After that, you want to update a security camera device to turn it on for monitoring. "
            "You also want to check what rooms are available in your home. "
            "Finally, you want to create an automated routine that activates security monitoring daily at 10 PM."
        ),
        actions=[
            Action(name="get_user_info", kwargs={
                "user_id": "3"
            }),
            Action(name="get_devices_info", kwargs={
                "room_id": "8"
            }),
            Action(name="update_device_info", kwargs={
                "device_id": "26",
                "status": "on"
            }),
            Action(name="get_rooms_info", kwargs={
                "home_id": "2"
            }),
            Action(name="create_routine", kwargs={
                "user_id": 3,
                "home_id": 2,
                "action_time": "22:00",
                "start_action_date": "2025-08-01",
                "action_interval": "daily"
            }),
            Action(name="get_home_info", kwargs={
                "home_id": "2"
            })
        ],
        outputs=[]
    )
]
