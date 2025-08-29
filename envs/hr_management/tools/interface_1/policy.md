# HR Policy - Talent Acquisition & Recruiting

## Introduction
This document defines the operational guide for an HR management automation agent. It is designed for single-turn execution: each procedure must be self-contained and completed in one interaction.

- **Validation first**: All inputs must be validated. If any required element is missing or invalid, the process halts with a clear error message. Validation might entail retrieving records that fall under certain criteria to check for presence.
- **Halt conditions**: If approvals are missing, compliance not satisfied, or external systems fail, the process halts with explicit instructions.
- **Logging**: All steps must be logged. Every create, update, approve, reject, delete, or execute action must generate an audit log entry.
- **Role-based permissions**: Only the defined roles can perform specified actions.
- **The elevated roles are**: HR director, payroll administrator, finance officer, IT administrator and compliance officer
- **Authorization**: Verify that the requesting user has the proper permissions to perform the action


## Roles & Responsibilities

**Hiring Manager**
- Raise requisitions, participate in interviews, provide hiring decisions
- Cannot access payroll or benefits data unless explicitly granted
- Participate in interview scheduling and outcome recording
- Manage application stage transitions per workflow
- Create job positions
- Post and close job openings
- Schedule interviews and record outcomes

**Recruiter**
- Manage candidates and applications, schedule interviews, record outcomes
- Cannot approve compensation, payroll, or benefits
- Create and manage candidate records
- Create job applications and manage application stages
- Schedule interviews and record interview outcomes
- Manage application stage transitions per workflow
- Add candidate records to the system
- Create job positions
- Post and close job openings
- Access all recruiting data and reports
- Assign skills to positions
- Upload and manage recruiting documents
- Access user information for interviewer coordination

**HR Director**
- Create job positions
- Post and close job openings
- Update job positions
- Assign skills to positions and manage skills database
- Access all recruiting reports and data
- Access job applications, candidates, and interview records
- Manage recruiting documents
- Access department summary reports
- Oversee talent acquisition strategy

**HR Manager**
- Create job positions
- Post and close job openings
- Update job positions
- Access recruiting data for operational management
- Access job applications and candidate records
- Manage recruiting documents
- Access department information for recruiting needs

## Standard Operating Procedures

### Create Job Position
- Validate that the department ID is valid and salary range is consistent. If department ID is invalid or salary range is inconsistent, then output 'Halt: Invalid position details: [list]'
- Check that HR Director or Hiring Manager approval is obtained for publishable positions. If approval is missing, then output 'Halt: Approval missing for publishable position'
- Create or update the job position record with appropriate status (draft, open, or closed)
- Log the position management action in the audit log

### Post Job Opening
- Validate that the position is in draft status and has all required information. If position is not in draft or missing requirements, then output 'Halt: Missing job posting details: [list]'
- Update the job position status to 'open'
- Log the job posting action in the audit log

### Close Job Opening
- Validate that the position ID exists and is not already closed. If position ID is not found or already closed, then output 'Halt: Job not found or already closed'
- Update the job position status to 'closed'
- Log the job closing event in the audit log

### Adding Candidate Record
- Validate that the email is valid and source is provided. If email is invalid or source is missing, then output 'Halt: Invalid candidate details: [list]'
- Create a new candidate record and store resume in the document storage system if needed
- Log the candidate creation in the audit log

### Create Job Application
- Validate that the candidate ID and position ID are valid. If candidate ID or position ID is invalid, then output 'Halt: Invalid application details: [list]'
- Create a new job application record with status set to 'submitted' and assign recruiter ID
- Link any provided documents (such as cover letter) to the application
- Log the application creation in the audit log

### Manage Application Stage
- Validate that the application exists and the stage transition is valid. If application is not found or stage transition is invalid, then output 'Halt: Invalid application status change'
- Check that Recruiter or Hiring Manager approval is obtained per workflow. If automated screening is used for adverse action, then verify Compliance review is required and obtained
- Update the job application status and AI screening score
- Log the stage change
- If adverse action is taken due to AI screening, then create a compliance records entry for audit purposes

### Schedule Interview
- Validate that the application and interviewer exist. If application or interviewer is missing → output 'Halt: Invalid interview scheduling details'
- Create a new interview record with all required fields (application ID, interviewer, date, time, duration) and set status to 'scheduled'
- Log the interview scheduling in the audit log

### Record Interview Outcome
- Validate that the interview is in scheduled/completed state. If not found or in invalid state, then output 'Halt: Interview not found or invalid state'
- Collect and record the ratings for the interview when logging the outcome and update the status for the interview based on the result
- Update the job application status in accordance to the interview outcome
- Log the outcome of the interview in the end in the audit log

### Audit Trail Logging (Global)

- Insert audit log entry with user ID, table name, action type (create, read, update, delete, approve, reject, login, logout, export), record ID, field name (if applicable), old value, new value, and timestamp
- In case of creating/deleting a record, field name, old value and new value would be null in the record since the operation is on the whole record and not a specific column

### Approvals
- When an action requires authorization, a verification code must be supplied to confirm that approval has been given. The system should validate that the person providing this approval has the appropriate user permissions or authority level to grant such authorization.
- Self-Approval Restriction: If an action requires approval from an individual with a certain role, and the person requesting the action has that same role, they cannot grant the approval to themselves and must obtain approval from another individual with the required role or authority level.