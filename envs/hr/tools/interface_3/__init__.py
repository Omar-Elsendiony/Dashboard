from .retrieve_employee_timesheets import RetrieveEmployeeTimesheets
from .retrieve_payroll_records import RetrievePayrollRecords
from .retrieve_payroll_deductions import RetrievePayrollDeductions
from .retrieve_payroll_summary_report import RetrievePayrollSummaryReport
from .retrieve_employees import RetrieveEmployees
from .retrieve_users import RetrieveUsers
from .retrieve_departments import RetrieveDepartments
from .retrieve_expense_reimbursements import RetrieveExpenseReimbursements
from .retrieve_documents import RetrieveDocuments
from .retrieve_audit_logs import RetrieveAuditLogs
from .retrieve_employee_summary_report import RetrieveEmployeeSummaryReport
from .submit_timesheet import SubmitTimesheet
from .approve_correct_timesheet import ApproveCorrectTimesheet
from .process_payroll_run import ProcessPayrollRun
from .insert_payroll_deduction import InsertPayrollDeduction
from .correct_payroll import CorrectPayroll
from .create_expense_reimbursement import CreateExpenseReimbursement
from .process_expense_reimbursement import ProcessExpenseReimbursement
from .update_expense_reimbursement import UpdateExpenseReimbursement
from .attach_document import AttachDocument
from .amend_document import AmendDocument
from .record_audit_entry import RecordAuditEntry

ALL_TOOLS_INTERFACE_3 = [
    RetrieveEmployeeTimesheets,
    RetrievePayrollRecords,
    RetrievePayrollDeductions,
    RetrievePayrollSummaryReport,
    RetrieveEmployees,
    RetrieveUsers,
    RetrieveDepartments,
    RetrieveExpenseReimbursements,
    RetrieveDocuments,
    RetrieveAuditLogs,
    RetrieveEmployeeSummaryReport,
    SubmitTimesheet,
    ApproveCorrectTimesheet,
    ProcessPayrollRun,
    InsertPayrollDeduction,
    CorrectPayroll,
    CreateExpenseReimbursement,
    ProcessExpenseReimbursement,
    UpdateExpenseReimbursement,
    AttachDocument,
    AmendDocument,
    RecordAuditEntry,
]
