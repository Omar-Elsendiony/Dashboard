from tau_bench.types import Action, Task

INTERFACE_3_TEST = [
    Task(
        annotator="0",
        user_id="admin_001",
        instruction=(
            "You are an administrator with user email 'jennifer.harris@tech.org'. You need to onboard a new employee "
            "named Alice Johnson with email 'alice.johnson@company.com'. To do this, you would need to conduct some actions. You would need first to create her user account and make her display name the concatenation of her first name and surname. Furthermore, you need to add her to the oldest group that had the permission to the 'SilverData Space' space. Not only that, you want to grant her a specific permission to read the space apart from the group permissions. The kind of permission will be the same as the group's one."
        ),
        actions=[
            Action(name="get_user_by_email", kwargs={
                "email": "jennifer.harris@tech.org"
            }),
            Action(name="create_user", kwargs={
                "username": "alice.johnson",
                "email": "alice.johnson@company.com",
                "first_name": "Alice",
                "last_name": "Johnson",
                "display_name": "Alice Johnson"
            }),
            Action(name="get_spaces_by_filters", kwargs={
                "name": "SilverData Space"
            }),
            Action(name="get_space_permissions", kwargs={
                "id": 70
            }),
            Action(name="add_user_to_group", kwargs={
                "user_id": 351,  # This would be the ID returned from create_user
                "group_id": 36,  # Assuming group ID 1 is the SilverData Space group
                "added_by": 4
            }),
            Action(name="get_user_groups", kwargs={
                "user_id": 351  # Verify Alice's group membership
            }),
            Action(name="assign_permission_to_user", kwargs={
                "space_id": 70,
                "user_id": 351,  # This would be the ID returned from create_user
                "permission_id": 13
            })
        ],
        outputs=[]
    )
]
