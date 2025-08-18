from tau_bench.types import Action, Task

INTERFACE_3_TEST = [
    Task(
        annotator="0",
        user_id="1",
        instruction=(
            "You are John Johnson, a finance officer. You need to manage commitments and financial "
            "operations. First, add a new user to the system, then get available funds and create "
            "a commitment for an investor. After that, create an invoice for the commitment and "
            "register a payment. Finally, generate a report and send an email notification."
        ),
        actions=[
            Action(name="add_new_user", kwargs={
                "first_name": "Sarah",
                "last_name": "Wilson",
                "email": "sarah.wilson@investment.com",
                "role": "finance_officer",
                "timezone": "EST",
                "status": "active"
            }),
            Action(name="get_available_funds", kwargs={}),
            Action(name="create_commitment", kwargs={
                "investor_id": "1",
                "fund_id": "1",
                "committed_amount": 750000.0,
                "compliance_officer_approval": True
            }),
            Action(name="create_invoice", kwargs={
                "investor_id": "1",
                "amount": 750000.0,
                "due_date": "2025-09-17",
                "description": "Investment commitment payment"
            }),
            Action(name="register_payment", kwargs={
                "invoice_id": "1",
                "amount": 750000.0,
                "payment_method": "wire_transfer",
                "payment_date": "2025-08-17"
            }),
            Action(name="generate_report", kwargs={
                "report_type": "financial",
                "period": "2025-08",
                "requester_role": "finance_officer"
            }),
            Action(name="send_email_notification", kwargs={
                "user_id": "1",
                "notification_type": "payment_confirmation",
                "notification_class": "invoices"
            })
        ],
        outputs=[]
    ),
    Task(
        annotator="1",
        user_id="2",
        instruction=(
            "You are William Robinson, a compliance officer. You need to manage investor commitments "
            "and track fulfillment. First, get investor profile and commitments, then fulfill a "
            "commitment and update invoice details. After that, get payment history and generate "
            "a performance report with document upload."
        ),
        actions=[
            Action(name="get_investor_profile", kwargs={"investor_id": "1"}),
            Action(name="get_investor_commitments", kwargs={"investor_id": "1"}),
            Action(name="fulfill_commitment", kwargs={
                "commitment_id": "1",
                "fulfillment_amount": 750000.0,
                "fulfillment_date": "2025-08-17"
            }),
            Action(name="update_invoice", kwargs={
                "invoice_id": "1",
                "status": "paid"
            }),
            Action(name="get_payment_history", kwargs={"investor_id": "1"}),
            Action(name="generate_report", kwargs={
                "report_type": "performance",
                "period": "2025-08",
                "requester_role": "fund_manager",
                "fund_id": "1"
            }),
            Action(name="create_upload_document", kwargs={
                "user_id": "2",
                "size_bytes": 2048576,
                "confidentiality_level": "confidential",
                "file_name": "commitment_report_august_2025.pdf",
                "file_format": "pdf"
            })
        ],
        outputs=[]
    )
]
