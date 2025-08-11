from tau_bench.types import Action, Task

INTERFACE_3_TEST = [
    Task(
        annotator="0",
        user_id="john_doe_502",
        instruction=(
            "You are John Doe from the Marketing department at Shopify. Your email is ‘john.doe@outlook.com’. "
            "While working, you encountered a sub-gateway payment error: ‘Error 504 when submitting payment for order #12345.’ "
            "There is this screenshot for reference: https://cdn.example.com/inc8001/shot.png and you want to attach it to the incident as evidence. "
            "Title the incident as ‘Error 504 at Checkout’. You recall that Sara with the email ‘sara.doe@outlook.com’ assisted with these kinds of incidents previously, "
            "and you would like the same agent to be assigned to this case. Please treat this with high priority."
        ),
        actions=[
            Action(name="filter_users", kwargs={
                "filters": {"email": "sara.doe@outlook.com"}
            }),
            Action(name="filter_users", kwargs={
                "filters": {"email": "john.doe@outlook.com"}
            }),
            Action(name="get_company_by_name", kwargs={
                "name": "Shopify"
            }),
            Action(name="filter_departments", kwargs={
                "filters": {
                    "company_id": "org_shopify_010",
                    "name": "Marketing"
                }
            }),
            Action(name="get_category_by_name", kwargs={
                "name": "Payment"
            }),
            Action(name="filter_subcategories", kwargs={
                "filters": {
                    "category_id": "cat_payments_02"
                }
            }),
            Action(name="create_incident", kwargs={
                "title": "Error 504 at Checkout",
                "description": "Error 504 when submitting payment for order #12345.",
                "category_id": "cat_payments_02",
                "subcategory_id": "sub_gateway_05",
                "reported_by": "user_john_doe_502",
                "company_id": "org_shopify_010",
                "department_id": "dept_marketing_03",
                "priority": "high",
                "assigned_to": "sara_id"
            }),
            Action(name="create_attachment", kwargs={
                "incident_id": "inc_8002",
                "uploaded_by": "john_id",
                "file_name": "shot.png",
                "file_url": "https://cdn.example.com/inc8001/shot.png"
            })
        ],
        outputs=[]
    )
]
