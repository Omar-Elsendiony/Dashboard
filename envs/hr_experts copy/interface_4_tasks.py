from tau_bench.types import Action, Task

INTERFACE_4_TEST = [
    Task(
        annotator="0",
        user_id="1",
        instruction=(
            "You are Sarah Johnson, an HR Manager. Ensure John Smith's successful workforce integration "
            "by administering his user account setup, managing his benefits enrollment, overseeing "
            "payroll administration, and confirming all regulatory approvals are obtained."
        ),
        actions=[
            Action(name="confirm_approval", kwargs={
                "action": "hr_management_setup",
                "requester_email": "sarah.johnson@company.com"
            }),
            Action(name="administer_user", kwargs={
                "action": "create",
                "user_data": {
                    "name": "John Smith",
                    "email": "john.smith@company.com",
                    "role": "Software Engineer",
                    "department": "Technology"
                }
            }),
            Action(name="administer_employee_benefits", kwargs={
                "employee_id": "1",
                "benefits_data": {
                    "health_plan": "PPO",
                    "dental_coverage": True,
                    "life_insurance": "2x_salary"
                }
            }),
            Action(name="administer_payroll_record", kwargs={
                "employee_id": "1",
                "pay_period": "2025-10-01",
                "regular_hours": 160,
                "overtime_hours": 8
            }),
            Action(name="lookup_employee", kwargs={
                "employee_id": "1"
            })
        ],
        outputs=[]
    ),
    Task(
        annotator="1",
        user_id="2",
        instruction=(
            "You are Michael Davis, an HR Director. Optimize the Technology department's workforce "
            "capabilities by administering the Senior Developer position creation, deploying comprehensive "
            "Security Awareness training programs, and overseeing performance review administration."
        ),
        actions=[
            Action(name="lookup_department", kwargs={
                "department_name": "Technology"
            }),
            Action(name="administer_job_position", kwargs={
                "action": "create",
                "position_data": {
                    "title": "Senior Developer",
                    "department": "Technology",
                    "salary_range": "80000-120000"
                }
            }),
            Action(name="administer_training_programs", kwargs={
                "program_name": "Security Awareness",
                "target_department": "Technology",
                "deadline": "2025-12-31"
            }),
            Action(name="administer_performance_review", kwargs={
                "employee_id": "1",
                "review_period": "2025-Q3",
                "rating": "meets_expectations"
            })
        ],
        outputs=[]
    )
]
