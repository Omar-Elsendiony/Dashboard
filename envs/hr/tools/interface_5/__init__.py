from .lookup_benefits_plans import LookupBenefitsPlans
from .lookup_employee_benefits import LookupEmployeeBenefits
from .lookup_leave_requests import LookupLeaveRequests
from .calculate_leave_balance import CalculateLeaveBalance
from .lookup_employees import LookupEmployees
from .lookup_users import LookupUsers
from .lookup_documents import LookupDocuments
from .lookup_audit_logs import LookupAuditLogs
from .lookup_payroll_records import LookupPayrollRecords
from .lookup_departments import LookupDepartments
from .lookup_expense_reimbursements import LookupExpenseReimbursements
from .create_benefits_plan import CreateBenefitsPlan
from .update_benefits_plan import UpdateBenefitsPlan
from .enroll_employee_benefits import EnrollEmployeeBenefits
from .update_employee_benefits import UpdateEmployeeBenefits
from .create_leave_request import CreateLeaveRequest
from .update_leave_request import UpdateLeaveRequest
from .process_leave_request import ProcessLeaveRequest
from .insert_document import InsertDocument
from .adjust_document import AdjustDocument
from .log_audit_event import LogAuditEvent

ALL_TOOLS_INTERFACE_5 = [
    LookupBenefitsPlans,
    LookupEmployeeBenefits,
    LookupLeaveRequests,
    CalculateLeaveBalance,
    LookupEmployees,
    LookupUsers,
    LookupDocuments,
    LookupAuditLogs,
    LookupPayrollRecords,
    LookupDepartments,
    LookupExpenseReimbursements,
    CreateBenefitsPlan,
    UpdateBenefitsPlan,
    EnrollEmployeeBenefits,
    UpdateEmployeeBenefits,
    CreateLeaveRequest,
    UpdateLeaveRequest,
    ProcessLeaveRequest,
    InsertDocument,
    AdjustDocument,
    LogAuditEvent,
]
