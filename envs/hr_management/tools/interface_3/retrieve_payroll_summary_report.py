import json
from typing import Any, Dict, Optional
from datetime import datetime
from tau_bench.envs.tool import Tool

class RetrievePayrollSummaryReport(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], pay_period_start: str = None, 
               pay_period_end: str = None, department_id: str = None) -> str:
        payroll_records = data.get("payroll_records", {})
        payroll_deductions = data.get("payroll_deductions", {})
        employees = data.get("employees", {})
        job_positions = data.get("job_positions", {})
        
        filtered_records = []
        
        for payroll in payroll_records.values():
            # Filter by pay period range
            if pay_period_start or pay_period_end:
                record_start = payroll.get("pay_period_start")
                record_end = payroll.get("pay_period_end")
                
                # Skip if we don't have valid dates
                if not record_start or not record_end:
                    continue
                
                # Convert strings to dates for comparison
                try:
                    record_start_date = datetime.strptime(record_start, "%Y-%m-%d").date()
                    record_end_date = datetime.strptime(record_end, "%Y-%m-%d").date()
                    
                    # Filter by start date (payroll period must start on or after this date)
                    if pay_period_start:
                        filter_start_date = datetime.strptime(pay_period_start, "%Y-%m-%d").date()
                        if record_start_date < filter_start_date:
                            continue
                    
                    # Filter by end date (payroll period must end on or before this date)
                    if pay_period_end:
                        filter_end_date = datetime.strptime(pay_period_end, "%Y-%m-%d").date()
                        if record_end_date > filter_end_date:
                            continue
                            
                except ValueError:
                    # Skip records with invalid date format
                    continue
            
            # Filter by department
            if department_id:
                employee = employees.get(payroll.get("employee_id"), {})
                position = job_positions.get(employee.get("position_id"), {})
                if position.get("department_id") != department_id:
                    continue
            
            filtered_records.append(payroll)
        
        # Calculate totals
        total_employees = len(filtered_records)
        total_hours = sum(float(record.get("hours_worked", 0)) for record in filtered_records)
        total_gross_pay = sum(
            float(record.get("hours_worked", 0)) * float(record.get("hourly_rate", 0)) 
            for record in filtered_records
        )
        
        # Calculate total deductions
        total_deductions = 0
        for record in filtered_records:
            payroll_id = record.get("payroll_id")
            for deduction in payroll_deductions.values():
                if deduction.get("payroll_id") == payroll_id:
                    total_deductions += float(deduction.get("amount", 0))
        
        total_net_pay = total_gross_pay - total_deductions
        
        summary = {
            "pay_period_start": pay_period_start,
            "pay_period_end": pay_period_end,
            "department_id": department_id,
            "total_employees": total_employees,
            "total_hours": round(total_hours, 2),
            "total_gross_pay": round(total_gross_pay, 2),
            "total_deductions": round(total_deductions, 2),
            "total_net_pay": round(total_net_pay, 2)
        }
        
        return json.dumps(summary)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "retrieve_payroll_summary_report",
                "description": "Get payroll summary statistics for a date range",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "pay_period_start": {
                            "type": "string", 
                            "description": "Include payroll periods starting on or after this date (YYYY-MM-DD)"
                        },
                        "pay_period_end": {
                            "type": "string", 
                            "description": "Include payroll periods ending on or before this date (YYYY-MM-DD)"
                        },
                        "department_id": {
                            "type": "string", 
                            "description": "Filter by specific department ID"
                        }
                    },
                    "required": []
                }
            }
        }