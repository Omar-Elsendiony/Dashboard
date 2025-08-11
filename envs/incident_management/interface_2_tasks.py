from tau_bench.types import Action, Task

INTERFACE_2_TEST = [
    Task(
        annotator="0",
        user_id="user_sla_admin_999",
        instruction=(
            "You are an SLA admin, and an incident was recently created regarding the network. This incident "
            "was assigned to Martin with the email ‘mart@gmail.com’ and it was the only incident assigned to him. "
            "You found out that there is an incorrect category assigned to it due to which an incorrect SLA policy "
            "was attached. You need to categorize this incident correctly under ‘Network’, with `VPN` included as "
            "one of its subcategories. This is a high-priority issue and should have an associated SLA policy, "
            "requiring a response within 30 minutes and resolution within 240 minutes. You want to create these "
            "categories if not available. You want to attach this new categorization and SLA to the incident and "
            "add a comment stating 'Incident SLA Modified' for the same."
        ),
        actions=[
            Action(name="filter_users", kwargs={
                "email": "mart@gmail.com"
            }),
            Action(name="filter_incidents", kwargs={
                "assigned_to": "mart_id"
            }),
            Action(name="get_category_by_name", kwargs={
                "name": "Network"
            }),
            Action(name="create_category", kwargs={
                "name": "Network"
            }),
            Action(name="create_subcategory", kwargs={
                "category_id": "cat_network_101",
                "name": "VPN"
            }),
            Action(name="create_sla_policy", kwargs={
                "name": "Network - High Priority",
                "priority": "high",
                "category_id": "cat_network_101",
                "response_time": 30,
                "resolve_time": 240
            }),
            Action(name="update_attached_incident_sla", kwargs={
                "incident_id": "INC_5005",
                "sla_id": "sla_network_high_101"
            }),
            Action(name="update_incident", kwargs={
                "incident_id": "INC_5005",
                "category_id": "cat_network_101",
                "subcategory_id": "subcat_vpn_101"
            }),
            Action(name="add_incident_comment", kwargs={
                "incident_id": "INC_5005",
                "user_id": "user_sla_admin_999",
                "comment_text": "Incident SLA Modified",
                "is_public": True
            }),
            Action(name="log_incident_change", kwargs={
                "incident_id": "INC_5005",
                "changed_by": "user_sla_admin_999"
            })
        ],
        outputs=[]
    )
]
