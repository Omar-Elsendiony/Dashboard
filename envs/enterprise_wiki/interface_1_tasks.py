from tau_bench.types import Action, Task

INTERFACE_1_TEST = [
    Task(
        annotator="0",
        user_id="john_docs_1001",
        instruction=(
            "Your user email is charles.johnson@enterprise.biz. You are a documentation manager setting up "
            "a new project wiki. You want to reate a space called 'General Documentation' if there is None. In it, you would set up a basic page structure with a main overview page with the title 'Development Guidelines Overview' and markdown content: '# Development Guidelines Overview\n\nWelcome to our development guidelines wiki. This space contains all coding standards, best practices, and project workflows.\n\n## Quick Links\n- [Coding Standards](#)\n- [Code Review Process](#)\n- [Testing Guidelines](#)\n\n## Getting Started\nNew team members should start with the coding standards page.'. Also, you want to create a coding standards sub-page with the title 'Coding Standards' and markdown content: '# Coding Standards\n\nThis page outlines the coding standards and conventions used in our projects.\n\n## General Principles\n1. Write clean, readable code\n2. Follow consistent naming conventions\n3. Comment complex logic\n4. Write unit tests\n\n## Language-Specific Guidelines\n- [Python Standards](#)\n- [JavaScript Standards](#)\n- [Java Standards](#)'. In both of those pages, you would like to use the template 'Documentation Template 1' for consistency. Also, you would version both pages in case you want to roll back to this initial change. The comment for the main page version should be 'Initial creation of main overview page' and for the coding standards sub-page version should be 'Initial creation of coding standards page'. Finally, you want to add a label 'important' to the main page."
        ),
        actions=[
            # Step 1: Get user information by email
            Action(name="get_user_by_email", kwargs={
                "email": "charles.johnson@enterprise.biz"
            }),
            
            # Step 2: Check if space already exists
            Action(name="get_spaces_by_filters", kwargs={
                "name": "Development Guidelines"
            }),
            
            # Step 3: Find the project template
            Action(name="search_page_template_by_name", kwargs={
                "name": "Project Template"
            }),
            
            # Step 4: Create main overview page
            Action(name="create_page", kwargs={
                "space_id": 1,
                "title": "Development Guidelines Overview",
                "content": "# Development Guidelines Overview\n\nWelcome to our development guidelines wiki. This space contains all coding standards, best practices, and project workflows.\n\n## Quick Links\n- [Coding Standards](#)\n- [Code Review Process](#)\n- [Testing Guidelines](#)\n\n## Getting Started\nNew team members should start with the coding standards page.",
                "content_format": "markdown",
                "created_by": 1,
                "template_id": 1
            }),
            
            # Step 5: Create a version for the main page
            Action(name="create_page_version", kwargs={
                "page_id": 596,
                "title": "Development Guidelines Overview",
                "content": "# Development Guidelines Overview\n\nWelcome to our development guidelines wiki. This space contains all coding standards, best practices, and project workflows.\n\n## Quick Links\n- [Coding Standards](#)\n- [Code Review Process](#)\n- [Testing Guidelines](#)\n\n## Getting Started\nNew team members should start with the coding standards page.",
                "content_format": "markdown",
                "change_comment": "Initial creation of main overview page",
                "change_type": "major",
                "created_by": "john_docs_1001"
            }),
            
            # Step 6: Create coding standards sub-page
            Action(name="create_page", kwargs={
                "space_id": "1",
                "title": "Coding Standards",
                "content": "# Coding Standards\n\nThis page outlines the coding standards and conventions used in our projects.\n\n## General Principles\n1. Write clean, readable code\n2. Follow consistent naming conventions\n3. Comment complex logic\n4. Write unit tests\n\n## Language-Specific Guidelines\n- [Python Standards](#)\n- [JavaScript Standards](#)\n- [Java Standards](#)",
                "content_format": "markdown",
                "created_by": "john_docs_1001",
                "parent_id": 596,
                "template_id": 1
            }),
            
            # Step 7: Create version for sub-page
            Action(name="create_page_version", kwargs={
                "page_id": 597,
                "title": "Coding Standards",
                "content": "# Coding Standards\n\nThis page outlines the coding standards and conventions used in our projects.\n\n## General Principles\n1. Write clean, readable code\n2. Follow consistent naming conventions\n3. Comment complex logic\n4. Write unit tests\n\n## Language-Specific Guidelines\n- [Python Standards](#)\n- [JavaScript Standards](#)\n- [Java Standards](#)",
                "content_format": "markdown",
                "change_comment": "Initial creation of coding standards page",
                "change_type": "major",
                "created_by": 1
            }),
            
            # Step 8: Find the guidelines label
            Action(name="get_labels_by_name", kwargs={
                "label_name": "guidelines"
            }),
            
            # Step 9: Add label to main page
            Action(name="add_page_label", kwargs={
                "page_id": 596,
                "label_id": 2,
                "added_by": 1
            })
        ],
        outputs=[]
    )
]
