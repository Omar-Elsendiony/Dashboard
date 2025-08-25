from tau_bench.types import Action, Task

INTERFACE_5_TEST = [
    Task(
        annotator="0",
        user_id="user_0005",
        instruction=(
            "Your user ID is user_0005. You want to validate your bank account, ensure your provider is active, "
            "convert EUR to USD for a payment, and record the final payment transaction with currency details."
        ),
        actions=[
            Action(name="get_bank_account_details", kwargs={
                "user_id": "user_0005",
                "bank_account_id": "bka_9995"
            }),
            Action(name="validate_provider_route", kwargs={
                "provider_name": "HSBC"
            }),
            Action(name="convert_currency", kwargs={
                "from_currency": "EUR",
                "to_currency": "USD",
                "amount": 1000.0
            }),
            Action(name="record_payment_fx", kwargs={
                "source_id": "payment_5522",
                "from_currency": "EUR",
                "to_currency": "USD",
                "original_amount": 1000.0,
                "converted_amount": 1085.5
            })
        ],
        outputs=[]
    )
]
