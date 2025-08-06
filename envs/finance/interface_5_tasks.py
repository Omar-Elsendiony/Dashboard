from tau_bench.types import Action, Task

INTERFACE_5_TEST = [
    Task(
        annotator="0",
        user_id="5",
        instruction=(
            "You are James Lindsay with the email \"jameslindsay@yahoo.com\", a finance operations manager. "
            "You need to handle comprehensive investor services and support. First, get your user information "
            "and retrieve available funds. Then, create a new investor profile and add a subscription for them. "
            "After that, fetch the investor's portfolio, create an invoice, record a payment, and submit a "
            "support ticket. Finally, send email updates about the completed operations."
        ),
        actions=[
            Action(name="get_user_information", kwargs={
                "user_id": "5"
            }),
            Action(name="list_funds_with_filter", kwargs={
                "status": "open",
                "fund_type": "hedge"
            }),
            Action(name="create_investor", kwargs={
                "name": "Global Investment Partners",
                "contact_email": "contact@globalinvestment.com",
                "investor_type": "institutional",
                "accreditation_status": "accredited"
            }),
            Action(name="add_subscription", kwargs={
                "investor_id": "2",
                "fund_id": "3",
                "amount": 750000,
                "subscription_date": "2025-08-06"
            }),
            Action(name="fetch_investor_portfolio", kwargs={
                "investor_id": "2"
            }),
            Action(name="create_invoice", kwargs={
                "investor_id": "2",
                "amount": 750000,
                "currency": "USD",
                "due_date": "2025-09-06"
            }),
            Action(name="record_payment", kwargs={
                "invoice_id": "1",
                "amount": 750000,
                "currency": "USD",
                "payment_method": "wire_transfer"
            }),
            Action(name="submit_ticket", kwargs={
                "user_id": "5",
                "subject": "New Investor Onboarding Completed",
                "description": "Successfully onboarded Global Investment Partners with subscription and payment processing",
                "priority": "medium"
            }),
            Action(name="send_updates_via_email", kwargs={
                "user_id": "5",
                "recipient_email": "allen.ltd@yahoo.com",
                "subject": "Welcome to Our Investment Platform",
                "message": "Your investment account has been successfully created and your subscription is now active"
            })
        ],
        outputs=[]
    )
]
