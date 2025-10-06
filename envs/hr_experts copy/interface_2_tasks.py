from tau_bench.types import Action, Task

INTERFACE_2_TEST = [
    Task(
        annotator="0",
        user_id="1",
        instruction=(
            "You are Sarah Johnson, an HR Manager. Establish a complete employee profile and benefits "
            "enrollment for John Smith by creating his user account, configuring his benefits package, "
            "setting up payroll processing, and validating all necessary HR approvals."
        ),
        actions=[
            Action(name="validate_approval", kwargs={
                "action": "hr_management_setup",
                "requester_email": "sarah.johnson@company.com"
            }),
            Action(name="handle_user", kwargs={
                "action": "create",
                "user_data": {
                    "name": "John Smith",
                    "email": "john.smith@company.com",
                    "role": "Software Engineer",
                    "department": "Technology"
                }
            }),
            Action(name="handle_employee_benefits", kwargs={
                "employee_id": "1",
                "benefits_data": {
                    "health_plan": "PPO",
                    "dental_coverage": True,
                    "life_insurance": "2x_salary"
                }
            }),
            Action(name="handle_payroll_record", kwargs={
                "employee_id": "1",
                "pay_period": "2025-10-01",
                "regular_hours": 160,
                "overtime_hours": 8
            }),
            Action(name="search_employee", kwargs={
                "employee_id": "1"
            })
        ],
        outputs=[]
    ),
    Task(
        annotator="1",
        user_id="2",
        instruction=(
            "You are Michael Davis, an HR Director. Build a robust Technology department infrastructure "
            "by establishing the Senior Developer job position, deploying Security Awareness training "
            "across the department, and conducting performance evaluations to maintain operational excellence."
        ),
        actions=[
            Action(name="search_department", kwargs={
                "department_name": "Technology"
            }),
            Action(name="handle_job_position", kwargs={
                "action": "create",
                "position_data": {
                    "title": "Senior Developer",
                    "department": "Technology",
                    "salary_range": "80000-120000"
                }
            }),
            Action(name="handle_training_programs", kwargs={
                "program_name": "Security Awareness",
                "target_department": "Technology",
                "deadline": "2025-12-31"
            }),
            Action(name="handle_performance_review", kwargs={
                "employee_id": "1",
                "review_period": "2025-Q3",
                "rating": "meets_expectations"
            })
        ],
        outputs=[]
    )
]
