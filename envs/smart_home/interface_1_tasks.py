from tau_bench.types import Action, Task

INTERFACE_1_TEST = [
    Task(
        annotator="0",
        user_id="1",
        instruction=(
            "You are Zachary Potts with the email \"zachary.potts@outlook.com\", the owner of a smart home. "
            "You just got home and want to set up your evening routine. First, you want to check your user profile "
            "to confirm your details. Then, you want to get information about your home and see what rooms are available. "
            "After that, you want to check all the devices in your bedroom and turn on a smart bulb to create "
            "a cozy atmosphere. You also want to adjust the thermostat in your bedroom. "
            "Finally, you want to create an automated routine for your home that will run daily at 8 PM."
        ),
        actions=[
            Action(name="get_user_info", kwargs={
                "user_id": "1"
            }),
            Action(name="get_home_info", kwargs={
                "home_id": "1"
            }),
            Action(name="get_rooms_info", kwargs={
                "home_id": "1"
            }),
            Action(name="get_devices_info", kwargs={
                "room_id": "1"
            }),
            Action(name="update_device_info", kwargs={
                "device_id": "1",
                "status": "on",
                "brightness_level": "75"
            }),
            Action(name="update_device_info", kwargs={
                "device_id": "11",
                "status": "on"
            }),
            Action(name="create_routine", kwargs={
                "user_id": 1,
                "home_id": 1,
                "action_time": "20:00",
                "start_action_date": "2025-08-01",
                "action_interval": "daily"
            })
        ],
        outputs=[]
    )
]
