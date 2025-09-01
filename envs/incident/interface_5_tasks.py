from tau_bench.types import Action, Task

INTERFACE_5_TEST = [
    Task(
        annotator="0",
        user_id="agent_lina_3344",
        instruction=(
            "Incident INC_9010 (email delivery failure) was recently resolved; however, these kinds of incidents are happening regularly. "
            "As agent Lina Doe, you want to check how many times incidents in the same category and subcategory have been reported; "
            "if the count is greater than 5, you’ll need to document the fix in the knowledge base with a description outlining that "
            "'If an email bounces, we should wait 5 minutes and retry, doing this up to 3 times before alerting the user'. "
            "Linking needs to be done for this knowledge base article to the incident. Also analyze the CSAT report based on your overall rating, "
            "and if it's 3 or lower, list out the low-rated incidents."
        ),
        actions=[
            Action(name="filter_users", kwargs={
                "name": "Lina Doe",
                "role": "agent"
            }),
            Action(name="filter_incidents", kwargs={
                "incident_id": "inc_9010"
            }),
            Action(name="filter_incidents", kwargs={
                "category_id": "cat_email_03",
                "subcategory_id": "sub_bounce_07"
            }),
            Action(name="create_kb_article", kwargs={
                "description": "If an email bounces, wait 5 minutes then retry up to 3 times before alerting user.",
                "category_id": "cat_email_03",
                "subcategory_id": "sub_bounce_07",
                "created_by": "agent_lina_3344"
            }),
            Action(name="link_incident_to_kb", kwargs={
                "incident_id": "inc_9010",
                "knowledge_base_id": "kb_6010"
            }),
            Action(name="get_average_csat", kwargs={
                "agent_id": "agent_lina_3344"
            }),
            Action(name="list_low_rated_incidents", kwargs={})
        ],
        outputs=[]
    )
]
