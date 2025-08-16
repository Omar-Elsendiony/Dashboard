# Finance Domain Database Wiki

## Overview

The Finance Database supports investment management functionalities, user profiles, fund operations, portfolio management, investor relations, subscription tracking, commitment management, and financial reporting. The database interacts exclusively through provided APIs, ensuring secure and structured financial data management.

## Database Schema

### Users

Maintains user profiles for financial system access.

- **Fields:** user_id, first_name, last_name, email, role, status, timezone, created_at, updated_at
- **Roles:** admin, employee
- **Status:** active, inactive, suspended

### Funds

Stores information about investment funds.

- **Fields:** fund_id, name, fund_type, base_currency, size, status, manager_id, created_at, updated_at
- **Fund Types:** equity, fixed_income, multi_asset, hedge
- **Currencies:** USD, EUR, GBP, NGN
- **Status:** open, closed

### Investors

Details individual and institutional investors.

- **Fields:** investor_id, name, investor_type, accreditation_status, contact_email, employee_id, created_at
- **Types:** retail, high_net_worth, institutional
- **Accreditation:** accredited, non_accredited

### Portfolios

Tracks investment portfolios.

- **Fields:** portfolio_id, investor_id, name, status, created_at, updated_at
- **Status:** active, inactive, archived

### Portfolio Holdings

Records holdings within portfolios.

- **Fields:** holding_id, portfolio_id, instrument_id, quantity, cost_basis, created_at

### Instruments

Financial instruments available for investment.

- **Fields:** instrument_id, ticker, name, instrument_type
- **Types:** stock, bond, derivative, cash, other
- **Status:** active, suspended, delisted

### Instrument Prices

Current and historical pricing data.

- **Fields:** price_id, instrument_id, price_date, open_price, high_price, low_price, close_price

### Subscriptions

Investor subscriptions to funds.

- **Fields:** subscription_id, investor_id, fund_id, amount, status, currency, request_assigned_to, request_date, approval_date, updated_at
- **Status:** pending, approved, cancelled
- **Currency:** USD, EUR,GBP,NGN 

### Commitments

Investment commitments from investors.

- **Fields:** commitment_id, investor_id, fund_id, commitment_amount, currency, commitment_date, status, updated_at
- **Status:** pending, fulfilled
- **Currency:** USD, EUR,GBP,NGN 

### Trades

Trading activity records.

- **Fields:** trade_id, fund_id, instrument_id, quantity, price, side, trade_date, status, created_at
- **side:** buy, sell
- **Status:** pending, executed, failed

### Invoices

Billing and invoice management.

- **Fields:** invoice_id, investor_id, amount, currency, due_date, status, invoice_date, created_at, updated_at
- **Status:** draft, sent, paid, overdue, cancelled

### Payments

Payment tracking and history.

- **Fields:** payment_id, invoice_id, investor_id, amount, currency, payment_date, payment_method, status, created_at, updated_at
- **Status:** pending, completed, failed, refunded

### NAV Records

Net Asset Value tracking for funds.

- **Fields:** nav_id, fund_id, nav_date, nav_value, updated_at

### Reports

Financial reporting and analytics.

- **Fields:** report_id, report_type, fund_id, investor_id, report_date, status, file_path, created_at, updated_at
- **Types:** performance, risk, compliance, tax
- **Status:** draft, completed, published

### Notifications

System notifications and alerts.

- **Fields:** notification_id, email, type, class, reference_id, status, sent_at, created_at
- **Types:** alert, reminder, report, subscription_update
- **Classes:** funds, investors,portfolios,trades,invoices,reports,documents,subscriptions, commitments,tickets,users,portfolio_holdings
- **Status:** pending, sent, failed

### Tickets

Support and issue tracking.

- **Fields:** ticket_id, invoice_id, issue_date, type, status, assigned_to, resolution_date, created_at, updated_at
- **Types:** missing_payment, overpayment, underpayment, mismatched_amount, invoice_duplicate, manual_follow_up
- **Status:** open, in_review, resolved, closed

### Documents

Document management and storage.

- **Fields:** document_id, name, type, uploaded_by, uploaded_date, report_id, size_bytes, status
- **Types:** pdf, xlsx, docx, csv, other
- **Status:** available, archived, deleted

## API Interactions

APIs provided are the exclusive means for the agent to interact with the database, managing users, funds, portfolios, investments, subscriptions, commitments, trades, invoices, payments, and reports.

### Key API Categories

- **User Management:** Create and update user profiles and permissions.
- **Fund Management:** Add/update fund details, NAV records, and fund operations.
- **Portfolio Management:** Manage investor portfolios and holdings.
- **Investment Management:** Process subscriptions, commitments, and trades.
- **Financial Operations:** Handle invoices, payments, and financial reporting.
- **Notification Management:** Send alerts and manage communications.
- **Document Management:** Handle file uploads and document tracking.
- **Reporting & Analytics:** Generate performance and compliance reports.

## Finance Agent Policy

The finance agent operates under strict regulatory and compliance guidelines, ensuring proper authorization, accurate financial calculations, and adherence to investment policies while maintaining data security and audit trails.

## Security and Compliance

All financial operations require proper user authentication, role-based access controls, and maintain comprehensive audit logs for regulatory compliance. Sensitive financial data is protected according to industry standards.

## Data Validation

The system enforces strict data validation for financial amounts, dates, investment eligibility, and regulatory requirements to ensure data integrity and compliance.

## Error Handling

Comprehensive error handling provides clear feedback for failed operations while maintaining security by not exposing sensitive system information.

## Reporting and Analytics

The system supports various reporting formats and analytics to help users monitor investment performance, compliance status, and financial metrics.
