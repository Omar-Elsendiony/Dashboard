from tau_bench.types import Action, Task

INTERFACE_5_TEST = [
    Task(
        annotator="0",
        user_id="1",
        instruction=(
            "You are Sarah Johnson, an HR Manager. Achieve complete employee onboarding for John Smith "
            "by executing his user account creation, implementing his benefits package, establishing "
            "payroll execution, and ensuring proper authentication of all required approvals."
        ),
        actions=[
            Action(name="authenticate_approval", kwargs={
                "action": "hr_management_setup",
                "requester_email": "sarah.johnson@company.com"
            }),
            Action(name="execute_user", kwargs={
                "action": "create",
                "user_data": {
                    "name": "John Smith",
                    "email": "john.smith@company.com",
                    "role": "Software Engineer",
                    "department": "Technology"
                }
            }),
            Action(name="execute_employee_benefits", kwargs={
                "employee_id": "1",
                "benefits_data": {
                    "health_plan": "PPO",
                    "dental_coverage": True,
                    "life_insurance": "2x_salary"
                }
            }),
            Action(name="execute_payroll_record", kwargs={
                "employee_id": "1",
                "pay_period": "2025-10-01",
                "regular_hours": 160,
                "overtime_hours": 8
            }),
            Action(name="retrieve_employee", kwargs={
                "employee_id": "1"
            })
        ],
        outputs=[]
    ),
    Task(
        annotator="1",
        user_id="2",
        instruction=(
            "You are Michael Davis, an HR Director. Maximize the Technology department's organizational "
            "effectiveness by executing the Senior Developer position establishment, implementing "
            "Security Awareness training execution, and delivering comprehensive performance review outcomes."
        ),
        actions=[
            Action(name="retrieve_department", kwargs={
                "department_name": "Technology"
            }),
            Action(name="execute_job_position", kwargs={
                "action": "create",
                "position_data": {
                    "title": "Senior Developer",
                    "department": "Technology",
                    "salary_range": "80000-120000"
                }
            }),
            Action(name="execute_training_programs", kwargs={
                "program_name": "Security Awareness",
                "target_department": "Technology",
                "deadline": "2025-12-31"
            }),
            Action(name="execute_performance_review", kwargs={
                "employee_id": "1",
                "review_period": "2025-Q3",
                "rating": "meets_expectations"
            })
        ],
        outputs=[]
    )
]
