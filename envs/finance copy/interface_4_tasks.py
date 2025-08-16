from tau_bench.types import Action, Task

INTERFACE_4_TEST = [
    Task(
        annotator="0",
        user_id="2",
        instruction=(
            "You are William Robinson with the email \"williamrobinson@gmail.com\", a finance administrator. "
            "You need to manage investor commitments and payment processing. First, verify your user "
            "identity and get information about existing funds. Then, create a new commitment for an "
            "investor, check the commitment fulfillment status, and issue an invoice for the commitment. "
            "After that, register a payment for the invoice and send an email notification to the investor "
            "about the successful payment processing."
        ),
        actions=[
            Action(name="identify_user", kwargs={
                "email": "williamrobinson@gmail.com"
            }),
            Action(name="get_funds", kwargs={
                "status": "open"
            }),
            Action(name="create_commitment", kwargs={
                "investor_id": "1",
                "fund_id": "2",
                "committed_amount": 500000,
                "commitment_date": "2025-08-06"
            }),
            Action(name="check_commitment_fulfillment_status", kwargs={
                "commitment_id": "1"
            }),
            Action(name="issue_invoice", kwargs={
                "investor_id": "1",
                "amount": 500000,
                "currency": "USD",
                "due_date": "2025-09-06"
            }),
            Action(name="register_payment", kwargs={
                "invoice_id": "1",
                "amount": 500000,
                "currency": "USD",
                "payment_method": "bank_transfer"
            }),
            Action(name="send_email_notification", kwargs={
                "user_id": "2",
                "recipient_email": "smith.miller.and.scott@smith-miller-and-scott.com",
                "subject": "Payment Confirmation",
                "message": "Your commitment payment has been successfully processed"
            })
        ],
        outputs=[]
    )
]
