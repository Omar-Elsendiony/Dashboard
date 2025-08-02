from tau_bench.types import Action, Task

INTERFACE_2_TEST = [
    Task(
        annotator="0",
        user_id="emma_community_mgr_4521",
        instruction=(
            "You are a community manager with the email address kazuki.mahmoud@tech.org. "
            "You need to investigate a user with the email 'dorothy.young@company.com' and who has been "
            "recurrently complaining about the timeline feasibility decreasing the other employees morale. You want to check their recent comments in the 'General Discussion' space. If he has a comment related to the process, you would suspend their account "
            "and notify them about the suspension. You want also to remove any comment of this kind."
        ),
        actions=[
            # Step 1: Get your own user information
            Action(name="get_user_by_email", kwargs={
                "email": "emma@cm.com"
            }),
            
            # Step 2: Get the reported user information
            Action(name="get_user_by_email", kwargs={
                "email": "alex.developer@devhub.com"
            }),
            
            # Step 3: Find the General Discussion space
            Action(name="get_spaces_by_filters", kwargs={
                "name": "InnovateLab Space"
            }),
            
            # Step 4: Get pages in the space to investigate
            Action(name="get_space_pages", kwargs={
                "space_id": 48
            }),
            
            # Step 5: Check comments on the main page
            Action(name="get_page_comments", kwargs={
                "page_id": 595
            }),
            
            # Step 6: Get details of a specific problematic comment
            Action(name="get_comment_info", kwargs={
                "comment_id": 622
            }),
            
            # Step 7: Suspend the user account
            Action(name="update_user_status", kwargs={
                "user_id": 52,
                "status": "suspended"
            }),
            
            # Step 8: Create notification for the suspended user
            Action(name="create_notification", kwargs={
                "user_id": 1,
                "notification_type": "user_mentioned",
                "title": "Account Suspended",
                "message": "Your account has been suspended due to policy violations.",
                "created_by": 1,
                "target_type": "user",
                "target_id": 52
            }),
            
            # Step 9: Hide the problematic comment
            Action(name="update_comment_status", kwargs={
                "comment_id": 622,
                "status": "deleted"
            })
        ],
        outputs=[]
    )
]
