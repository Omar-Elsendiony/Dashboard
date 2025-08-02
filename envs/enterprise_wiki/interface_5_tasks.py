from tau_bench.types import Action, Task

INTERFACE_5_TEST = [
    Task(
        annotator="0",
        user_id="content_manager_789",
        instruction=(
            "It's Monday morning, and you've just arrived at your desk with your usual coffee when you notice "
            "an urgent notification from your team lead. Apparently, John Smith from the development team "
            "(donald.young1@company.com) submitted his page in the 'GreenSoft Space' space over the weekend, but it's "
            "a complete mess. The page has no labels, making it impossible to find, the content is poorly "
            "formatted, and there are no guidelines for other developers who need to contribute. Your manager "
            "wants this fixed before the stakeholder review at 2 PM today. As the content manager "
            "(lisa.thomas@company.com), you know exactly what needs to be done. You need to quickly add "
            "the right labels (tutorial label with ID 7 and guide label with ID 8) so people can actually find this documentation. Also, you want to leave a helpful comment explaining how others should contribute (using markdown format). Its content will be: '## Guidelines for Contributors\n\nPlease follow these guidelines when updating this documentation:\n- Use clear section headings\n- Include code examples where applicable\n- Update the changelog at the bottom\n\nThanks for your contributions!'. Moreover, you would like to attach the standard project guidelines PDF (project_guidelines.pdf, originally named Project_Guidelines_v2.pdf, 524KB size) that everyone seems to forget about. Furthermore, You do not want to forget to create a properly formatted version of this page with its current content so that you open the room to roll back to this version of the page if necessary with the comment 'Improved formatting and added structured sections'. You want to validate that all of the aforementioned actions were conducted correctly by listing the comments, attachments and versions related to the page."
        ),
        actions=[
            # Step 1: Get your own user information
            Action(name="get_user_by_email", kwargs={
                "email": "lisa.thomas@company.com"
            }),
            Action(name="get_user_by_email", kwargs={
                "email": "donald.young1@company.com"
            }),
            # Step 3: Get label information for "Documentation"
            Action(name="get_label_info", kwargs={
                "label_id": 1
            }),
            # Step 4: Add "Documentation" label to the page
            Action(name="add_page_label", kwargs={
                "page_id": 166,
                "label_id": 1,
                "added_by": 333  # content manager user ID
            }),
            
            # Step 5: Add "Project" label to the page
            Action(name="add_page_label", kwargs={
                "page_id": 166,
                "label_id": 2,
                "added_by": 333
            }),
            
            # Step 6: Create a structured comment to guide contributors
            Action(name="create_comment", kwargs={
                "page_id": 166,
                "content": "## Guidelines for Contributors\n\nPlease follow these guidelines when updating this documentation:\n- Use clear section headings\n- Include code examples where applicable\n- Update the changelog at the bottom\n\nThanks for your contributions!",
                "created_by": 333,
                "content_format": "markdown"
            }),
            
            # Step 7: Create an attachment with project guidelines
            Action(name="create_attachment", kwargs={
                "page_id": 166,
                "filename": "project_guidelines.pdf",
                "original_filename": "Project_Guidelines_v2.pdf",
                "mime_type": "application/pdf",
                "file_size": 524288,
                "storage_path": "/attachments/guidelines/project_guidelines.pdf",
                "uploaded_by": 333
            }),
            
            # Step 8: Create a new version of the page with better formatting
            Action(name="create_page_version", kwargs={
                "page_id": 166,
                "title": "Integration Guide - Part 141",
                "content": "# Integration Guide - Part 141\n\nIntegration guide for connecting external systems.\n\n## Prerequisites\n\nThis section covers prerequisites related information and guidelines. Follow the procedures outlined here to ensure proper prerequisites implementation.\n\n## Setup\n\nThis section covers setup related information and guidelines. Follow the procedures outlined here to ensure proper setup implementation.\n\n## Configuration\n\nThis section covers configuration related information and guidelines. Follow the procedures outlined here to ensure proper configuration implementation.\n\n## Testing\n\nThis section covers testing related information and guidelines. Follow the procedures outlined here to ensure proper testing implementation.\n\n## Troubleshooting\n\nThis section covers troubleshooting related information and guidelines. Follow the procedures outlined here to ensure proper troubleshooting implementation.\n\n## Additional Resources\n\n- Related documentation links\n- Support contact information\n- Training materials\n",
                "content_format": "markdown",
                "change_comment": "Improved formatting and added structured sections",
                "change_type": "major",
                "created_by": 333
            }),
            
            # Step 9: Get all comments on the page to verify our additions
            Action(name="get_page_comments_by_thread_level", kwargs={
                "page_id": 166,
                "thread_level": 0
            }),
            
            # Step 10: Get all attachments on the page to verify upload
            Action(name="get_page_attachments", kwargs={
                "page_id": 166
            }),
            
            # Step 11: Get page versions to verify the new version was created
            Action(name="get_page_versions", kwargs={
                "page_id": 166
            })
        ],
        outputs=[]
    )
]
