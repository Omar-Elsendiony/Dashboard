from tau_bench.types import Action, Task

INTERFACE_1_TEST = [
    Task(
        annotator="0",
        user_id="1",
        instruction=(
            "You are Sarah Johnson, an HR Manager. Complete the employee onboarding process for John Smith "
            "by setting up his user account, configuring his benefits package, processing his initial payroll setup, "
            "and ensuring all HR management approvals are in place."
        ),
        actions=[
            Action(name="check_approval", kwargs={
                "action": "hr_management_setup",
                "requester_email": "sarah.johnson@company.com"
            }),
            Action(name="manage_user", kwargs={
                "action": "create",
                "user_data": {
                    "name": "John Smith",
                    "email": "john.smith@company.com",
                    "role": "Software Engineer",
                    "department": "Technology"
                }
            }),
            Action(name="manage_employee_benefits", kwargs={
                "employee_id": "1",
                "benefits_data": {
                    "health_plan": "PPO",
                    "dental_coverage": True,
                    "life_insurance": "2x_salary"
                }
            }),
            Action(name="manage_payroll_record", kwargs={
                "employee_id": "1",
                "pay_period": "2025-10-01",
                "regular_hours": 160,
                "overtime_hours": 8
            }),
            Action(name="discover_employee", kwargs={
                "employee_id": "1"
            })
        ],
        outputs=[]
    ),
    Task(
        annotator="1",
        user_id="2",
        instruction=(
            "You are Michael Davis, an HR Director. Establish a comprehensive departmental structure "
            "by creating a new Senior Developer position in the Technology department, implementing "
            "mandatory security training programs, and conducting performance reviews to ensure organizational compliance."
        ),
        actions=[
            Action(name="discover_department", kwargs={
                "department_name": "Technology"
            }),
            Action(name="manage_job_position", kwargs={
                "action": "create",
                "position_data": {
                    "title": "Senior Developer",
                    "department": "Technology",
                    "salary_range": "80000-120000"
                }
            }),
            Action(name="manage_training_programs", kwargs={
                "program_name": "Security Awareness",
                "target_department": "Technology",
                "deadline": "2025-12-31"
            }),
            Action(name="manage_performance_review", kwargs={
                "employee_id": "1",
                "review_period": "2025-Q3",
                "rating": "meets_expectations"
            })
        ],
        outputs=[]
    )
]