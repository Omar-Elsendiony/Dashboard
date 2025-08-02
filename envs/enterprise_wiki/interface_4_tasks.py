from tau_bench.types import Action, Task

INTERFACE_4_TEST = [
    Task(
        annotator="0",
        user_id="sarah_manager_1234",
        instruction=(
            "You are a project manager with the email 'linda.hussein@company.com'. "
            "You need to create a new workspace called 'Team Projects' for your development team. This space will be used for project management and collaboration. "
            "You want to create this space with the key 'TEAMPROJ' and a description 'Workspace for development team project management'. "
            "You also want to ensure that the space is not publicly accessible."
            "After creating the space, you want to add a 'Priority' label system with three levels named: "
            "High (with color red), Medium (with color orange), and Low (with color green) and no description so that you add the the High priority label to a welcome page that you are yet to create titled 'Welcome to Team Projects' and its content the same as the title for now."
        ),
        actions=[
            # Step 1: Get your user information
            Action(name="get_user_by_email", kwargs={
                "email": "sarah@company.com"
            }),
            
            # Step 2: Create the new workspace
            Action(name="create_space", kwargs={
                "key": "TEAMPROJ",
                "name": "Team Projects",
                "created_by": 76,
                "description": "Workspace for development team project management",
                "space_type": "global",
                "anonymous_access": False
            }),
            
            # Step 3: Create High priority label
            Action(name="create_label", kwargs={
                "name": "High",
                "space_id": 76,
                "created_by": 309,
                "color": "red",
                "description": None
            }),
            
            # Step 4: Create Medium priority label
            Action(name="create_label", kwargs={
                "name": "Medium",
                "space_id": 76,
                "created_by": 309,
                "color": "orange",
                "description": None
            }),
            
            # Step 5: Create Low priority label
            Action(name="create_label", kwargs={
                "name": "Low",
                "space_id": 76,
                "created_by": 309,
                "color": "green",
                "description": None
            }),
            
            # Step 6: Create welcome page
            Action(name="create_page", kwargs={
                "space_id": 76,
                "title": "Welcome to Team Projects",
                "content": "Welcome to Team Projects",
                "content_format": "markdown",
                "created_by": 309
            }),
            
            # Step 7: Add High priority label to the welcome page
            Action(name="add_page_label", kwargs={
                "page_id": 506,
                "label_id": 101,
                "added_by": 76
            }),
            
            # Step 8: Verify labels were created correctly
            Action(name="get_space_labels", kwargs={
                "space_id": 76
            })
        ],
        outputs=[]
    )
]
