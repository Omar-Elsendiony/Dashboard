from tau_bench.types import Action, Task

INTERFACE_4_TEST = [
    Task(
        annotator="0",
        user_id="5",
        instruction=(
            "You are Jennifer Davis with the email \"brown1606@yahoo.com\", a smart home user. "
            "You want to manage your smart home system effectively for daily living. "
            "First, you want to check your user profile to confirm your details. "
            "Then, you want to get information about your home and see what rooms are available. "
            "After that, you want to check all the devices in your bedroom and update some device settings. "
            "You want to turn on a camera device for security and adjust a bulb for better lighting. "
            "Finally, you want to create an automated routine for your evening activities."
        ),
        actions=[
            Action(name="get_user_info", kwargs={
                "user_id": "5"
            }),
            Action(name="get_home_info", kwargs={
                "home_id": "4"
            }),
            Action(name="get_rooms_info", kwargs={
                "home_id": "4"
            }),
            Action(name="get_devices_info", kwargs={
                "room_id": "14"
            }),
            Action(name="update_device_info", kwargs={
                "device_id": "56",
                "status": "on"
            }),
            Action(name="update_device_info", kwargs={
                "device_id": "57",
                "status": "on",
                "brightness_level": "60"
            }),
            Action(name="create_routine", kwargs={
                "user_id": 5,
                "home_id": 4,
                "action_time": "21:00",
                "start_action_date": "2025-08-01",
                "action_interval": "daily"
            })
        ],
        outputs=[]
    )
]
