from tau_bench.types import Action, Task

INTERFACE_3_TEST = [
    Task(
        annotator="0",
        user_id="67",
        instruction=(
            "You are a technical support specialist who discovered a critical payment gateway error. "
            "While testing the payment system, you encountered a 504 gateway timeout error that prevents "
            "customers from completing transactions. You need to register this as a new incident with "
            "high priority due to its impact on revenue. The incident affects the payment processing "
            "component for client Rice Inc. You should also register a communication to notify stakeholders "
            "about the ongoing issue and create an escalation if this incident requires immediate attention "
            "from senior management. Additionally, you want to document a workaround for merchants to use "
            "an alternative payment method while the issue is being resolved."
        ),
        actions=[
            Action(name="retrieve_users", kwargs={
                "user_id": "67"
            }),
            Action(name="retrieve_clients", kwargs={
                "client_name_contains": "Rice"
            }),
            Action(name="retrieve_components", kwargs={
                "component_type": "payment_gateway"
            }),
            Action(name="register_incident", kwargs={
                "title": "Payment Gateway 504 Timeout Error",
                "category": "system_outage",
                "impact": "critical",
                "client_id": "2",
                "reporter_id": "67",
                "component_id": "1",
                "detected_at": "2025-09-01T09:30:00",
                "p1_wide_enterprise_or_5plus_customers": True
            }),
            Action(name="register_escalation", kwargs={
                "incident_id": "501",
                "escalation_level": "senior_management",
                "escalated_by": "67",
                "reason": "Critical payment system outage affecting revenue"
            }),
            Action(name="register_communication", kwargs={
                "incident_id": "501",
                "communication_type": "stakeholder_notification",
                "message": "Payment gateway experiencing 504 timeout errors. Alternative payment methods available.",
                "recipient_type": "client_stakeholders",
                "sent_by": "67"
            }),
            Action(name="register_workaround", kwargs={
                "incident_id": "501",
                "description": "Direct customers to use bank transfer or check payment options",
                "workaround_type": "temporary_alternative",
                "effectiveness": "medium",
                "created_by": "67"
            }),
            Action(name="register_incident_update_record", kwargs={
                "incident_id": "501",
                "update_type": "status_change",
                "description": "Initial incident registration and stakeholder notification completed",
                "updated_by": "67"
            })
        ],
        outputs=[]
    )
]
