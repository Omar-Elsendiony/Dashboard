from tau_bench.types import Action, Task

INTERFACE_4_TEST = [
    Task(
        annotator="4",
        user_id="4",
        instruction=(
            "You are James Wilson, a Finance Manager. You need to manage payroll and benefits operations. "
            "Get payroll entities, process payroll cycles, manage benefit plans, and handle payment operations."
        ),
        actions=[
            Action(name="get_payroll_entities", kwargs={
                "entity_type": "payroll_cycles",
                "filters": {"status": "open"}
            }),
            Action(name="process_payroll_cycle_operations", kwargs={
                "operation_type": "create_cycle",
                "cycle_start_date": "01-01-2025",
                "cycle_end_date": "01-31-2025",
                "frequency": "monthly",
                "cutoff_date": "01-25-2025",
                "user_id": "4"
            }),
            Action(name="process_payroll_input_operations", kwargs={
                "operation_type": "create_input",
                "employee_id": "5",
                "cycle_id": "2",
                "hours_worked": 160,
                "overtime_hours": 8,
                "user_id": "4"
            }),
            Action(name="process_benefit_plan_operations", kwargs={
                "operation_type": "create_plan",
                "benefit_type": "health_insurance",
                "plan_name": "Premium Health Plan 2025",
                "provider_name": "HealthCorp Insurance",
                "effective_from": "01-01-2025",
                "effective_until": "12-31-2025",
                "user_id": "4",
                "default_employee_contribution": 200.0,
                "default_employer_contribution": 800.0
            }),
            Action(name="build_audit_entry", kwargs={
                "reference_id": "2",
                "reference_type": "payroll_cycle",
                "action": "create",
                "user_id": "4",
                "field_name": "cycle_creation"
            })
        ],
        outputs=[]
    )
]
