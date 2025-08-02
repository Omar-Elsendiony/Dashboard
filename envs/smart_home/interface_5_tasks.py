from tau_bench.types import Action, Task

INTERFACE_5_TEST = [
    Task(
        annotator="0",
        user_id="5",
        instruction=(
            "You are Jennifer Davis with the email \"brown1606@yahoo.com\", a smart home system user. "
            "You want to manage your smart home devices efficiently for your daily routine. "
            "First, you want to check your user profile and get information about your home. "
            "Then you want to see what rooms are available in your home and check what devices are in your kitchen. "
            "After that, you want to turn on a refrigerator device and update a bulb device for better lighting. "
            "You also want to turn on a thermostat for temperature control. "
            "Finally, you want to create an automated routine that will help with your morning activities."
        ),
        actions=[
            Action(name="get_user_info", kwargs={
                "user_id": "5"
            }),
            Action(name="get_home_info", kwargs={
                "home_id": "5"
            }),
            Action(name="get_rooms_info", kwargs={
                "home_id": "5"
            }),
            Action(name="get_devices_info", kwargs={
                "room_id": "21"
            }),
            Action(name="update_device_info", kwargs={
                "device_id": "92",
                "status": "on"
            }),
            Action(name="update_device_info", kwargs={
                "device_id": "85",
                "status": "on",
                "brightness_level": "70"
            }),
            Action(name="update_device_info", kwargs={
                "device_id": "93",
                "status": "on"
            }),
            Action(name="create_routine", kwargs={
                "user_id": 5,
                "home_id": 5,
                "action_time": "07:00",
                "start_action_date": "2025-08-01",
                "action_interval": "daily"
            })
        ],
        outputs=[]
    )
]
