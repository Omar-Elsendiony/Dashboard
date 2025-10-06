from tau_bench.types import Action, Task

INTERFACE_3_TEST = [
    Task(
        annotator="0",
        user_id="1",
        instruction=(
            "You are Sarah Johnson, an HR Manager. Complete John Smith's employee integration "
            "by processing his user account creation, enrolling him in comprehensive benefits, "
            "establishing his payroll configuration, and verifying all approval requirements are met."
        ),
        actions=[
            Action(name="verify_approval", kwargs={
                "action": "hr_management_setup",
                "requester_email": "sarah.johnson@company.com"
            }),
            Action(name="process_user", kwargs={
                "action": "create",
                "user_data": {
                    "name": "John Smith",
                    "email": "john.smith@company.com",
                    "role": "Software Engineer",
                    "department": "Technology"
                }
            }),
            Action(name="process_employee_benefits", kwargs={
                "employee_id": "1",
                "benefits_data": {
                    "health_plan": "PPO",
                    "dental_coverage": True,
                    "life_insurance": "2x_salary"
                }
            }),
            Action(name="process_payroll_record", kwargs={
                "employee_id": "1",
                "pay_period": "2025-10-01",
                "regular_hours": 160,
                "overtime_hours": 8
            }),
            Action(name="find_employee", kwargs={
                "employee_id": "1"
            })
        ],
        outputs=[]
    ),
    Task(
        annotator="1",
        user_id="2",
        instruction=(
            "You are Michael Davis, an HR Director. Strengthen the Technology department's operational "
            "capacity by processing the creation of a Senior Developer role, implementing Security Awareness "
            "training initiatives, and conducting comprehensive performance assessments."
        ),
        actions=[
            Action(name="find_department", kwargs={
                "department_name": "Technology"
            }),
            Action(name="process_job_position", kwargs={
                "action": "create",
                "position_data": {
                    "title": "Senior Developer",
                    "department": "Technology",
                    "salary_range": "80000-120000"
                }
            }),
            Action(name="process_training_programs", kwargs={
                "program_name": "Security Awareness",
                "target_department": "Technology",
                "deadline": "2025-12-31"
            }),
            Action(name="process_performance_review", kwargs={
                "employee_id": "1",
                "review_period": "2025-Q3",
                "rating": "meets_expectations"
            })
        ],
        outputs=[]
    )
]
