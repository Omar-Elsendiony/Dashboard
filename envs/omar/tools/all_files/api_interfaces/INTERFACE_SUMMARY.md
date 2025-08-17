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

