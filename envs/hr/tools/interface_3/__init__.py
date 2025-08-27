from .add_payroll_deduction import AddPayrollDeduction
from .approve_correct_timesheet import ApproveCorrectTimesheet
from .correct_payroll import CorrectPayroll
from .create_audit_log import CreateAuditLog
from .create_expense_reimbursement import CreateExpenseReimbursement
from .get_audit_logs import GetAuditLogs
from .get_departments import GetDepartments
from .get_documents import GetDocuments
from .get_employee_summary_report import GetEmployeeSummaryReport
from .get_employee_timesheets import GetEmployeeTimesheets
from .get_employees import GetEmployees
from .get_expense_reimbursements import GetExpenseReimbursements
from .get_payroll_deductions import GetPayrollDeductions
from .get_payroll_records import GetPayrollRecords
from .get_payroll_summary_report import GetPayrollSummaryReport
from .get_users import GetUsers
from .process_expense_reimbursement import ProcessExpenseReimbursement
from .process_payroll_run import ProcessPayrollRun
from .submit_timesheet import SubmitTimesheet
from .update_document import UpdateDocument
from .update_expense_reimbursement import UpdateExpenseReimbursement
from .upload_document import UploadDocument

ALL_TOOLS_INTERFACE_3 = [
    AddPayrollDeduction,
    ApproveCorrectTimesheet,
    CorrectPayroll,
    CreateAuditLog,
    CreateExpenseReimbursement,
    GetAuditLogs,
    GetDepartments,
    GetDocuments,
    GetEmployeeSummaryReport,
    GetEmployeeTimesheets,
    GetEmployees,
    GetExpenseReimbursements,
    GetPayrollDeductions,
    GetPayrollRecords,
    GetPayrollSummaryReport,
    GetUsers,
    ProcessExpenseReimbursement,
    ProcessPayrollRun,
    SubmitTimesheet,
    UpdateDocument,
    UpdateExpenseReimbursement,
    UploadDocument
]
