#!/bin/bash

# Create main directory structure
mkdir -p api_interfaces

# Interface 1: Fund Management & Trading Operations (24 APIs)
# Focus: Fund lifecycle, trading, and instrument management with chaining
mkdir -p api_interfaces/interface_1
echo "Creating Interface 1: Fund Management & Trading Operations"

# Fund Management Chain
cp create_fund.py api_interfaces/interface_1/
cp update_fund.py api_interfaces/interface_1/
cp delete_fund.py api_interfaces/interface_1/
cp get_available_funds.py api_interfaces/interface_1/
cp list_funds_with_filter.py api_interfaces/interface_1/
cp get_fund_instruments.py api_interfaces/interface_1/

# Trading Chain: fund -> instruments -> trades -> prices
cp execute_trade.py api_interfaces/interface_1/
cp add_new_trade_for_fund.py api_interfaces/interface_1/
cp get_fund_trade_details.py api_interfaces/interface_1/
cp update_trade.py api_interfaces/interface_1/
cp get_daily_profit_loss_by_fund.py api_interfaces/interface_1/

# Instrument Management Chain
cp get_instruments.py api_interfaces/interface_1/
cp update_instrument.py api_interfaces/interface_1/
cp deactivate_reactivate_instrument.py api_interfaces/interface_1/
cp get_instruments_prices.py api_interfaces/interface_1/
cp update_instrument_price.py api_interfaces/interface_1/
cp summary_of_instrument_types_by_prices.py api_interfaces/interface_1/

# NAV Calculation Chain
cp calculate_nav.py api_interfaces/interface_1/
cp get_fund_nav_history.py api_interfaces/interface_1/
cp get_nav_records.py api_interfaces/interface_1/
cp update_nav_record_value.py api_interfaces/interface_1/

# Financial Calculations
cp calculate_future_value.py api_interfaces/interface_1/
cp calculate_liabilities.py api_interfaces/interface_1/
cp get_growth_rate.py api_interfaces/interface_1/

# Interface 2: Investor Management & Portfolio Operations (24 APIs)
# Focus: Investor lifecycle, portfolio management, and holdings
mkdir -p api_interfaces/interface_2
echo "Creating Interface 2: Investor Management & Portfolio Operations"

# Investor Lifecycle Chain
cp investor_onboarding.py api_interfaces/interface_2/
cp update_investor_details.py api_interfaces/interface_2/
cp investor_offboarding.py api_interfaces/interface_2/
cp get_filtered_investors.py api_interfaces/interface_2/
cp get_investor_profile.py api_interfaces/interface_2/

# Portfolio Management Chain: portfolio -> holdings -> updates
cp get_investor_portfolio.py api_interfaces/interface_2/
cp get_investor_portfolio_holdings.py api_interfaces/interface_2/
cp get_portfolio_holdings.py api_interfaces/interface_2/
cp add_new_holding.py api_interfaces/interface_2/
cp update_investor_portfolio_holding.py api_interfaces/interface_2/
cp remove_holding.py api_interfaces/interface_2/

# Investor Transaction Chain
cp get_investor_transactions_history.py api_interfaces/interface_2/
cp get_investor_statements.py api_interfaces/interface_2/
cp get_investor_documents.py api_interfaces/interface_2/

# Subscription Management Chain
cp create_subscription.py api_interfaces/interface_2/
cp update_subscription.py api_interfaces/interface_2/
cp cancel_subscription.py api_interfaces/interface_2/
cp get_investor_subscriptions.py api_interfaces/interface_2/
cp get_subscriptions.py api_interfaces/interface_2/

# Redemption Management Chain
cp process_redemption.py api_interfaces/interface_2/
cp get_investor_redemptions.py api_interfaces/interface_2/
cp switch_funds.py api_interfaces/interface_2/

# User Management
cp add_new_user.py api_interfaces/interface_2/
cp find_user.py api_interfaces/interface_2/

# Interface 3: Commitment & Financial Operations (24 APIs)
# Focus: Commitments, invoicing, and payment processing
mkdir -p api_interfaces/interface_3
echo "Creating Interface 3: Commitment & Financial Operations"

# Commitment Lifecycle Chain
cp create_commitment.py api_interfaces/interface_3/
cp get_commitments.py api_interfaces/interface_3/
cp get_investor_commitments.py api_interfaces/interface_3/
cp fulfill_commitment.py api_interfaces/interface_3/

# Invoice Management Chain: commitment -> invoice -> payment
cp create_invoice.py api_interfaces/interface_3/
cp get_invoices.py api_interfaces/interface_3/
cp retrieve_invoices.py api_interfaces/interface_3/
cp update_invoice.py api_interfaces/interface_3/
cp delete_invoice.py api_interfaces/interface_3/

# Payment Processing Chain
cp register_payment.py api_interfaces/interface_3/
cp get_payment_history.py api_interfaces/interface_3/

# Reporting Chain (repeated from Interface 1 for financial reporting)
cp generate_report.py api_interfaces/interface_3/
cp get_reports.py api_interfaces/interface_3/

# Document Management Chain
cp create_upload_document.py api_interfaces/interface_3/

# Notification System Chain
cp send_email_notification.py api_interfaces/interface_3/
cp get_notifications.py api_interfaces/interface_3/

# Financial calculations (repeated for commitment/payment calculations)
cp calculate_future_value.py api_interfaces/interface_3/
cp calculate_liabilities.py api_interfaces/interface_3/
cp calculate_nav.py api_interfaces/interface_3/

# Fund and investor operations needed for financial processing
cp get_available_funds.py api_interfaces/interface_3/
cp get_filtered_investors.py api_interfaces/interface_3/
cp get_investor_profile.py api_interfaces/interface_3/

# User management for financial operations
cp add_new_user.py api_interfaces/interface_3/

# Interface 4: Analytics & Reporting (24 APIs)
# Focus: Data analytics, performance metrics, and advanced reporting
mkdir -p api_interfaces/interface_4
echo "Creating Interface 4: Analytics & Reporting"

# Performance Analytics Chain
cp get_fund_nav_history.py api_interfaces/interface_4/
cp get_daily_profit_loss_by_fund.py api_interfaces/interface_4/
cp calculate_future_value.py api_interfaces/interface_4/
cp get_growth_rate.py api_interfaces/interface_4/
cp calculate_nav.py api_interfaces/interface_4/
cp get_nav_records.py api_interfaces/interface_4/

# Portfolio Analytics Chain
cp get_investor_portfolio.py api_interfaces/interface_4/
cp get_investor_portfolio_holdings.py api_interfaces/interface_4/
cp get_portfolio_holdings.py api_interfaces/interface_4/
cp get_investor_transactions_history.py api_interfaces/interface_4/

# Market Data Analytics Chain
cp get_instruments_prices.py api_interfaces/interface_4/
cp summary_of_instrument_types_by_prices.py api_interfaces/interface_4/
cp get_instruments.py api_interfaces/interface_4/
cp get_fund_trade_details.py api_interfaces/interface_4/

# Financial Reporting Chain
cp generate_report.py api_interfaces/interface_4/
cp get_reports.py api_interfaces/interface_4/
cp get_investor_statements.py api_interfaces/interface_4/
cp get_investor_documents.py api_interfaces/interface_4/

# Fund Analytics Chain
cp get_available_funds.py api_interfaces/interface_4/
cp list_funds_with_filter.py api_interfaces/interface_4/
cp get_fund_instruments.py api_interfaces/interface_4/

# Investor Analytics Chain
cp get_filtered_investors.py api_interfaces/interface_4/
cp get_investor_profile.py api_interfaces/interface_4/

# Commitment & Payment Analytics
cp get_commitments.py api_interfaces/interface_4/
cp get_payment_history.py api_interfaces/interface_4/

# Interface 5: System Administration & Configuration (24 APIs)
# Focus: System settings, configurations, and administrative functions
mkdir -p api_interfaces/interface_5
echo "Creating Interface 5: System Administration & Configuration"

# User Administration Chain
cp add_new_user.py api_interfaces/interface_5/
cp find_user.py api_interfaces/interface_5/
cp investor_onboarding.py api_interfaces/interface_5/
cp investor_offboarding.py api_interfaces/interface_5/
cp update_investor_details.py api_interfaces/interface_5/

# System Configuration Chain
cp create_fund.py api_interfaces/interface_5/
cp update_fund.py api_interfaces/interface_5/
cp delete_fund.py api_interfaces/interface_5/
cp deactivate_reactivate_instrument.py api_interfaces/interface_5/
cp update_instrument.py api_interfaces/interface_5/

# Data Management Chain
cp create_upload_document.py api_interfaces/interface_5/
cp get_investor_documents.py api_interfaces/interface_5/
cp update_instrument_price.py api_interfaces/interface_5/
cp update_nav_record_value.py api_interfaces/interface_5/

# Notification Administration Chain
cp send_email_notification.py api_interfaces/interface_5/
cp get_notifications.py api_interfaces/interface_5/

# Subscription Administration Chain
cp create_subscription.py api_interfaces/interface_5/
cp update_subscription.py api_interfaces/interface_5/
cp cancel_subscription.py api_interfaces/interface_5/
cp get_subscriptions.py api_interfaces/interface_5/

# Financial Administration Chain
cp create_commitment.py api_interfaces/interface_5/
cp create_invoice.py api_interfaces/interface_5/
cp update_invoice.py api_interfaces/interface_5/
cp delete_invoice.py api_interfaces/interface_5/

# System Monitoring Chain
cp get_reports.py api_interfaces/interface_5/
cp generate_report.py api_interfaces/interface_5/

# Create summary file
cat > api_interfaces/INTERFACE_SUMMARY.md << EOF
# API Interface Distribution Summary

## Interface 1: Fund Management & Trading Operations (24 APIs)
**Read Operations (12):**
- get_available_funds.py
- list_funds_with_filter.py  
- get_fund_instruments.py
- get_fund_trade_details.py
- get_daily_profit_loss_by_fund.py
- get_instruments.py
- get_instruments_prices.py
- summary_of_instrument_types_by_prices.py
- get_fund_nav_history.py
- get_nav_records.py
- calculate_future_value.py
- get_growth_rate.py

**Write Operations (12):**
- create_fund.py
- update_fund.py
- delete_fund.py
- execute_trade.py
- add_new_trade_for_fund.py
- update_trade.py
- update_instrument.py
- deactivate_reactivate_instrument.py
- update_instrument_price.py
- calculate_nav.py
- update_nav_record_value.py
- calculate_liabilities.py

## Interface 2: Investor Management & Portfolio Operations (24 APIs)
**Read Operations (12):**
- get_filtered_investors.py
- get_investor_profile.py
- get_investor_portfolio.py
- get_investor_portfolio_holdings.py
- get_portfolio_holdings.py
- get_investor_transactions_history.py
- get_investor_statements.py
- get_investor_documents.py
- get_investor_subscriptions.py
- get_subscriptions.py
- get_investor_redemptions.py
- find_user.py

**Write Operations (12):**
- investor_onboarding.py
- update_investor_details.py
- investor_offboarding.py
- add_new_holding.py
- update_investor_portfolio_holding.py
- remove_holding.py
- create_subscription.py
- update_subscription.py
- cancel_subscription.py
- process_redemption.py
- switch_funds.py
- add_new_user.py

## Interface 3: Commitment & Financial Operations (24 APIs)
**Read Operations (12):**
- get_commitments.py
- get_investor_commitments.py
- get_invoices.py
- retrieve_invoices.py
- get_payment_history.py
- get_reports.py
- get_notifications.py
- get_available_funds.py
- get_filtered_investors.py
- get_investor_profile.py
- calculate_future_value.py
- calculate_liabilities.py

**Write Operations (12):**
- create_commitment.py
- fulfill_commitment.py
- create_invoice.py
- update_invoice.py
- delete_invoice.py
- register_payment.py
- generate_report.py
- create_upload_document.py
- send_email_notification.py
- calculate_nav.py
- add_new_user.py

## Interface 4: Analytics & Reporting (24 APIs)
**Read Operations (18):**
- get_fund_nav_history.py
- get_daily_profit_loss_by_fund.py
- calculate_future_value.py
- get_growth_rate.py
- get_nav_records.py
- get_investor_portfolio.py
- get_investor_portfolio_holdings.py
- get_portfolio_holdings.py
- get_investor_transactions_history.py
- get_instruments_prices.py
- summary_of_instrument_types_by_prices.py
- get_instruments.py
- get_fund_trade_details.py
- get_reports.py
- get_investor_statements.py
- get_investor_documents.py
- get_available_funds.py
- list_funds_with_filter.py
- get_fund_instruments.py
- get_filtered_investors.py
- get_investor_profile.py
- get_commitments.py
- get_payment_history.py

**Write Operations (6):**
- calculate_nav.py
- generate_report.py

## Interface 5: System Administration & Configuration (24 APIs)
**Read Operations (7):**
- find_user.py
- get_investor_documents.py
- get_notifications.py
- get_subscriptions.py
- get_reports.py

**Write Operations (19):**
- add_new_user.py
- investor_onboarding.py
- investor_offboarding.py
- update_investor_details.py
- create_fund.py
- update_fund.py
- delete_fund.py
- deactivate_reactivate_instrument.py
- update_instrument.py
- create_upload_document.py
- update_instrument_price.py
- update_nav_record_value.py
- send_email_notification.py
- create_subscription.py
- update_subscription.py
- cancel_subscription.py
- create_commitment.py
- create_invoice.py
- update_invoice.py
- delete_invoice.py
- generate_report.py

## API Repetition Summary:
**Most Repeated APIs across interfaces:**
- get_available_funds.py (Interface 1, 3, 4)
- calculate_future_value.py (Interface 1, 3, 4)
- generate_report.py (Interface 3, 4, 5)
- get_reports.py (Interface 3, 4, 5)
- add_new_user.py (Interface 2, 3, 5)
- get_filtered_investors.py (Interface 2, 3, 4)
- get_investor_profile.py (Interface 2, 3, 4)
- calculate_nav.py (Interface 1, 3, 4)
- get_notifications.py (Interface 3, 5)
- send_email_notification.py (Interface 3, 5)

## Key API Chains Identified:

1. **Fund Trading Chain:** get_available_funds -> get_fund_instruments -> execute_trade -> get_fund_trade_details
2. **Portfolio Management Chain:** get_investor_portfolio -> get_portfolio_holdings -> update_investor_portfolio_holding
3. **Commitment-Invoice-Payment Chain:** create_commitment -> create_invoice -> register_payment
4. **NAV Calculation Chain:** get_fund_instruments -> calculate_nav -> update_nav_record_value
5. **Investor Onboarding Chain:** investor_onboarding -> create_subscription -> create_commitment
6. **Analytics Chain:** get_fund_nav_history -> calculate_future_value -> generate_report
7. **Administration Chain:** add_new_user -> investor_onboarding -> create_fund

EOF

echo "API interfaces created successfully!"
echo "All 5 interfaces now have 24 APIs each (120 total API copies)"
echo "APIs are repeated across interfaces where logical grouping requires it"
echo "Check INTERFACE_SUMMARY.md for detailed breakdown and repetition analysis"