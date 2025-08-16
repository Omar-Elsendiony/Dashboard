#!/bin/bash

# Fund Management API Interface Organization Script
# This script copies APIs to their respective interface folders based on the grouping strategy

set -e  # Exit on any error

echo "Starting API interface organization..."

# Create interface directories
echo "Creating interface directories..."
for i in {1..5}; do
    mkdir -p "interface_$i"
    echo "Created interface_$i/"
done

# Function to safely copy file if it exists
copy_if_exists() {
    local source_file="$1"
    local dest_dir="$2"
    local api_name="$3"
    
    if [ -f "$source_file" ]; then
        cp "$source_file" "$dest_dir/"
        echo "✓ Copied $api_name to $dest_dir/"
    else
        echo "⚠ WARNING: $source_file not found for $api_name"
    fi
}

echo ""
echo "=== INTERFACE 1: Core Fund Operations ==="

# Interface 1 - Read APIs
copy_if_exists "./temp_interfaces/interface_temp_1/get_fund_details.py" "interface_1" "get_fund_details.py"
copy_if_exists "./temp_interfaces/interface_temp_1/get_available_funds.py" "interface_1" "get_available_funds.py"
copy_if_exists "./temp_interfaces/interface_temp_1/get_fund_nav_history.py" "interface_1" "get_fund_nav_history.py"
copy_if_exists "./temp_interfaces/interface_temp_2/database_tools/get_funds.py" "interface_1" "get_funds.py"
copy_if_exists "./temp_interfaces/interface_temp_2/database_tools/list_funds_with_filter.py" "interface_1" "list_funds_with_filter.py"
copy_if_exists "./temp_interfaces/interface_temp_2/fund_management_tools/get_fund_valuation.py" "interface_1" "get_fund_valuation.py"
copy_if_exists "./temp_interfaces/interface_temp_2/fund_tools/get_nav_records.py" "interface_1" "get_nav_records.py"
copy_if_exists "./fund_management_tools/get_fund_instruments.py" "interface_1" "get_fund_instruments.py"
copy_if_exists "./temp_interfaces/interface_temp_2/fund_management_tools/get_reports.py" "interface_1" "get_reports.py"
copy_if_exists "./temp_interfaces/interface_temp_2/fund_management_tools/get_daily_profit_loss_by_fund.py" "interface_1" "get_daily_profit_loss_by_fund.py"
copy_if_exists "./temp_interfaces/interface_temp_2/fund_management_tools/get_fund_trade_details.py" "interface_1" "get_fund_trade_details.py"
copy_if_exists "./temp_interfaces/interface_temp_2/fund_management_tools/get_instruments.py" "interface_1" "get_instruments.py"

# Interface 1 - Create/Update/Delete APIs
copy_if_exists "./fund_management_tools/create_fund.py" "interface_1" "create_fund.py"
copy_if_exists "./fund_management_tools/update_fund.py" "interface_1" "update_fund.py"
copy_if_exists "./fund_management_tools/delete_fund.py" "interface_1" "delete_fund.py"
copy_if_exists "./fund_management_tools/calculate_nav.py" "interface_1" "calculate_nav.py"
copy_if_exists "./temp_interfaces/interface_temp_2/fund_tools/create_nav_record.py" "interface_1" "create_nav_record.py"
copy_if_exists "./temp_interfaces/interface_temp_2/fund_tools/update_nav_record_value.py" "interface_1" "update_nav_record_value.py"
copy_if_exists "./temp_interfaces/interface_temp_2/database_tools/create_new_fund.py" "interface_1" "create_new_fund.py"
copy_if_exists "./temp_interfaces/interface_temp_2/database_tools/update_fund_details.py" "interface_1" "update_fund_details.py"
copy_if_exists "./fund_management_tools/generate_report.py" "interface_1" "generate_report.py"
copy_if_exists "./temp_interfaces/interface_temp_2/fund_management_tools/create_report.py" "interface_1" "create_report.py"
copy_if_exists "./fund_management_tools/calculate_future_value.py" "interface_1" "calculate_future_value.py"
copy_if_exists "./fund_management_tools/calculate_liabilities.py" "interface_1" "calculate_liabilities.py"
copy_if_exists "./fund_management_tools/deactivate_reactivate_instrument.py" "interface_1" "deactivate_reactivate_instrument.py"

echo ""
echo "=== INTERFACE 2: Investor Management & Portfolio Operations ==="

# Interface 2 - Read APIs
copy_if_exists "./temp_interfaces/interface_temp_1/get_investor_profile.py" "interface_2" "get_investor_profile.py"
copy_if_exists "./temp_interfaces/interface_temp_1/get_investor_portfolio.py" "interface_2" "get_investor_portfolio.py"
copy_if_exists "./temp_interfaces/interface_temp_1/get_investor_portfolio_holdings.py" "interface_2" "get_investor_portfolio_holdings.py"
copy_if_exists "./temp_interfaces/interface_temp_1/get_investor_documents.py" "interface_2" "get_investor_documents.py"
copy_if_exists "./temp_interfaces/interface_temp_1/get_investor_statements.py" "interface_2" "get_investor_statements.py"
copy_if_exists "./temp_interfaces/interface_temp_1/get_investor_transactions_history.py" "interface_2" "get_investor_transactions_history.py"
copy_if_exists "./temp_interfaces/interface_temp_2/database_tools/get_investors.py" "interface_2" "get_investors.py"
copy_if_exists "./temp_interfaces/interface_temp_2/database_tools/get_filtered_investors.py" "interface_2" "get_filtered_investors.py"
copy_if_exists "./temp_interfaces/interface_temp_2/database_tools/get_investor_portfolio.py" "interface_2" "get_investor_portfolio_db.py"
copy_if_exists "./temp_interfaces/interface_temp_2/database_tools/get_portfolio_holdings.py" "interface_2" "get_portfolio_holdings.py"
copy_if_exists "./temp_interfaces/interface_temp_2/fund_management_tools/get_user_information.py" "interface_2" "get_user_information.py"
copy_if_exists "./temp_interfaces/interface_temp_2/fund_management_tools/find_user.py" "interface_2" "find_user.py"

# Interface 2 - Create/Update/Delete APIs
copy_if_exists "./fund_management_tools/investor_onboarding.py" "interface_2" "investor_onboarding.py"
copy_if_exists "./fund_management_tools/investor_offboarding.py" "interface_2" "investor_offboarding.py"
copy_if_exists "./temp_interfaces/interface_temp_2/database_tools/onboard_new_investor.py" "interface_2" "onboard_new_investor.py"
copy_if_exists "./temp_interfaces/interface_temp_2/database_tools/update_investor_details.py" "interface_2" "update_investor_details.py"
copy_if_exists "./temp_interfaces/interface_temp_2/database_tools/add_new_holding.py" "interface_2" "add_new_holding.py"
copy_if_exists "./temp_interfaces/interface_temp_2/database_tools/update_investor_portfolio_holding.py" "interface_2" "update_investor_portfolio_holding.py"
copy_if_exists "./temp_interfaces/interface_temp_2/fund_management_tools/add_new_user.py" "interface_2" "add_new_user.py"
copy_if_exists "./fund_management_tools/create_upload_document.py" "interface_2" "create_upload_document.py"
copy_if_exists "./fund_management_tools/switch_funds.py" "interface_2" "switch_funds.py"
copy_if_exists "./temp_interfaces/interface_temp_1/get_available_funds.py" "interface_2" "get_available_funds.py"
copy_if_exists "./temp_interfaces/interface_temp_1/get_fund_details.py" "interface_2" "get_fund_details.py"
copy_if_exists "./temp_interfaces/interface_temp_2/fund_management_tools/get_reports.py" "interface_2" "get_reports.py"
copy_if_exists "./fund_management_tools/generate_report.py" "interface_2" "generate_report.py"

echo ""
echo "=== INTERFACE 3: Subscription & Commitment Management ==="

# Interface 3 - Read APIs
copy_if_exists "./temp_interfaces/interface_temp_1/get_investor_subscriptions.py" "interface_3" "get_investor_subscriptions.py"
copy_if_exists "./temp_interfaces/interface_temp_1/get_investor_commitments.py" "interface_3" "get_investor_commitments.py"
copy_if_exists "./temp_interfaces/interface_temp_1/get_investor_redemptions.py" "interface_3" "get_investor_redemptions.py"
copy_if_exists "./temp_interfaces/interface_temp_2/fund_tools/get_subscriptions.py" "interface_3" "get_subscriptions.py"
copy_if_exists "./temp_interfaces/interface_temp_2/fund_tools/get_commitments.py" "interface_3" "get_commitments.py"
copy_if_exists "./temp_interfaces/interface_temp_2/fund_tools/get_payment_history.py" "interface_3" "get_payment_history.py"
copy_if_exists "./temp_interfaces/interface_temp_2/fund_tools/check_commitment_fulfillment_status.py" "interface_3" "check_commitment_fulfillment_status.py"
copy_if_exists "./temp_interfaces/interface_temp_1/get_investor_profile.py" "interface_3" "get_investor_profile.py"
copy_if_exists "./temp_interfaces/interface_temp_1/get_fund_details.py" "interface_3" "get_fund_details.py"
copy_if_exists "./temp_interfaces/interface_temp_2/fund_management_tools/get_notifications.py" "interface_3" "get_notifications.py"
copy_if_exists "./temp_interfaces/interface_temp_1/get_investor_portfolio.py" "interface_3" "get_investor_portfolio.py"
copy_if_exists "./temp_interfaces/interface_temp_2/database_tools/get_funds.py" "interface_3" "get_funds.py"

# Interface 3 - Create/Update/Delete APIs
copy_if_exists "./fund_management_tools/create_subscription.py" "interface_3" "create_subscription.py"
copy_if_exists "./fund_management_tools/update_subscription.py" "interface_3" "update_subscription.py"
copy_if_exists "./fund_management_tools/cancel_subscription.py" "interface_3" "cancel_subscription.py"
copy_if_exists "./fund_management_tools/create_commitment.py" "interface_3" "create_commitment.py"
copy_if_exists "./fund_management_tools/fulfill_commitment.py" "interface_3" "fulfill_commitment.py"
copy_if_exists "./fund_management_tools/process_redemption.py" "interface_3" "process_redemption.py"
copy_if_exists "./temp_interfaces/interface_temp_2/database_tools/subscribe_investor_to_fund.py" "interface_3" "subscribe_investor_to_fund_db.py"
copy_if_exists "./temp_interfaces/interface_temp_2/fund_tools/create_commitment.py" "interface_3" "create_commitment_ft.py"
copy_if_exists "./temp_interfaces/interface_temp_2/fund_tools/update_subscription.py" "interface_3" "update_subscription_ft.py"
copy_if_exists "./temp_interfaces/interface_temp_2/fund_tools/subscribe_investor_to_fund.py" "interface_3" "subscribe_investor_to_fund_ft.py"
copy_if_exists "./temp_interfaces/interface_temp_2/fund_tools/record_payment.py" "interface_3" "record_payment.py"
copy_if_exists "./temp_interfaces/interface_temp_2/fund_tools/register_payment.py" "interface_3" "register_payment.py"
copy_if_exists "./temp_interfaces/interface_temp_2/fund_management_tools/notify_user.py" "interface_3" "notify_user.py"

echo ""
echo "=== INTERFACE 4: Trading & Instrument Management ==="

# Interface 4 - Read APIs
copy_if_exists "./temp_interfaces/interface_temp_2/fund_management_tools/get_fund_trade_details.py" "interface_4" "get_fund_trade_details.py"
copy_if_exists "./temp_interfaces/interface_temp_2/fund_management_tools/get_instruments.py" "interface_4" "get_instruments.py"
copy_if_exists "./temp_interfaces/interface_temp_2/fund_management_tools/get_instruments_prices.py" "interface_4" "get_instruments_prices.py"
copy_if_exists "./fund_management_tools/get_fund_instruments.py" "interface_4" "get_fund_instruments.py"
copy_if_exists "./temp_interfaces/interface_temp_2/fund_management_tools/get_daily_profit_loss_by_fund.py" "interface_4" "get_daily_profit_loss_by_fund.py"
copy_if_exists "./temp_interfaces/interface_temp_2/fund_management_tools/get_fund_valuation.py" "interface_4" "get_fund_valuation.py"
copy_if_exists "./temp_interfaces/interface_temp_2/database_tools/get_portfolio_holdings.py" "interface_4" "get_portfolio_holdings.py"
copy_if_exists "./temp_interfaces/interface_temp_1/get_fund_nav_history.py" "interface_4" "get_fund_nav_history.py"
copy_if_exists "./temp_interfaces/interface_temp_2/fund_tools/get_nav_records.py" "interface_4" "get_nav_records.py"
copy_if_exists "./temp_interfaces/interface_temp_1/get_fund_details.py" "interface_4" "get_fund_details.py"
copy_if_exists "./temp_interfaces/interface_temp_2/database_tools/get_funds.py" "interface_4" "get_funds.py"
copy_if_exists "./temp_interfaces/interface_temp_1/get_investor_portfolio_holdings.py" "interface_4" "get_investor_portfolio_holdings.py"

# Interface 4 - Create/Update/Delete APIs
copy_if_exists "./fund_management_tools/execute_trade.py" "interface_4" "execute_trade.py"
copy_if_exists "./fund_management_tools/update_instrument.py" "interface_4" "update_instrument.py"
copy_if_exists "./fund_management_tools/deactivate_reactivate_instrument.py" "interface_4" "deactivate_reactivate_instrument.py"
copy_if_exists "./temp_interfaces/interface_temp_2/fund_management_tools/update_instrument_price.py" "interface_4" "update_instrument_price.py"
copy_if_exists "./temp_interfaces/interface_temp_2/fund_management_tools/update_trade.py" "interface_4" "update_trade.py"
copy_if_exists "./temp_interfaces/interface_temp_2/fund_management_tools/add_new_trade_for_fund.py" "interface_4" "add_new_trade_for_fund.py"
copy_if_exists "./fund_management_tools/calculate_nav.py" "interface_4" "calculate_nav.py"
copy_if_exists "./fund_management_tools/calculate_liabilities.py" "interface_4" "calculate_liabilities.py"
copy_if_exists "./fund_management_tools/calculate_future_value.py" "interface_4" "calculate_future_value.py"
copy_if_exists "./temp_interfaces/interface_temp_2/database_tools/add_new_holding.py" "interface_4" "add_new_holding.py"
copy_if_exists "./temp_interfaces/interface_temp_2/database_tools/update_investor_portfolio_holding.py" "interface_4" "update_investor_portfolio_holding.py"
copy_if_exists "./temp_interfaces/interface_temp_2/fund_tools/create_nav_record.py" "interface_4" "create_nav_record.py"
copy_if_exists "./temp_interfaces/interface_temp_2/fund_tools/update_nav_record_value.py" "interface_4" "update_nav_record_value.py"

echo ""
echo "=== INTERFACE 5: Reporting & Notifications ==="

# Interface 5 - Read APIs
copy_if_exists "./temp_interfaces/interface_temp_2/fund_management_tools/get_reports.py" "interface_5" "get_reports.py"
copy_if_exists "./temp_interfaces/interface_temp_2/fund_management_tools/get_notifications.py" "interface_5" "get_notifications.py"
copy_if_exists "./temp_interfaces/interface_temp_1/get_investor_statements.py" "interface_5" "get_investor_statements.py"
copy_if_exists "./temp_interfaces/interface_temp_1/get_investor_transactions_history.py" "interface_5" "get_investor_transactions_history.py"
copy_if_exists "./temp_interfaces/interface_temp_2/fund_management_tools/get_daily_profit_loss_by_fund.py" "interface_5" "get_daily_profit_loss_by_fund.py"
copy_if_exists "./temp_interfaces/interface_temp_2/fund_management_tools/get_fund_valuation.py" "interface_5" "get_fund_valuation.py"
copy_if_exists "./temp_interfaces/interface_temp_2/fund_tools/get_payment_history.py" "interface_5" "get_payment_history.py"
copy_if_exists "./temp_interfaces/interface_temp_1/get_investor_portfolio.py" "interface_5" "get_investor_portfolio.py"
copy_if_exists "./temp_interfaces/interface_temp_1/get_investor_subscriptions.py" "interface_5" "get_investor_subscriptions.py"
copy_if_exists "./temp_interfaces/interface_temp_1/get_investor_commitments.py" "interface_5" "get_investor_commitments.py"
copy_if_exists "./temp_interfaces/interface_temp_1/get_investor_redemptions.py" "interface_5" "get_investor_redemptions.py"
copy_if_exists "./temp_interfaces/interface_temp_2/fund_management_tools/get_user_information.py" "interface_5" "get_user_information.py"

# Interface 5 - Create/Update/Delete APIs
copy_if_exists "./fund_management_tools/generate_report.py" "interface_5" "generate_report.py"
copy_if_exists "./temp_interfaces/interface_temp_2/fund_management_tools/create_report.py" "interface_5" "create_report.py"
copy_if_exists "./temp_interfaces/interface_temp_2/fund_management_tools/notify_user.py" "interface_5" "notify_user.py"
copy_if_exists "./temp_interfaces/interface_temp_2/fund_management_tools/send_email_notification.py" "interface_5" "send_email_notification.py"
copy_if_exists "./fund_management_tools/create_upload_document.py" "interface_5" "create_upload_document.py"
copy_if_exists "./fund_management_tools/switch_funds.py" "interface_5" "switch_funds.py"
copy_if_exists "./fund_management_tools/process_redemption.py" "interface_5" "process_redemption.py"
copy_if_exists "./fund_management_tools/fulfill_commitment.py" "interface_5" "fulfill_commitment.py"
copy_if_exists "./temp_interfaces/interface_temp_2/fund_tools/record_payment.py" "interface_5" "record_payment.py"
copy_if_exists "./temp_interfaces/interface_temp_2/fund_tools/register_payment.py" "interface_5" "register_payment.py"
copy_if_exists "./fund_management_tools/update_subscription.py" "interface_5" "update_subscription.py"
copy_if_exists "./temp_interfaces/interface_temp_2/fund_management_tools/add_new_user.py" "interface_5" "add_new_user.py"
copy_if_exists "./temp_interfaces/interface_temp_2/fund_management_tools/find_user.py" "interface_5" "find_user.py"

echo ""
echo "=== SUMMARY ==="
echo "API organization completed!"
echo ""

# Count files in each interface
for i in {1..5}; do
    count=$(find "interface_$i" -name "*.py" 2>/dev/null | wc -l)
    echo "Interface $i: $count files"
done

echo ""
echo "Interface structure created:"
echo "interface_1/ - Core Fund Operations"
echo "interface_2/ - Investor Management & Portfolio Operations"
echo "interface_3/ - Subscription & Commitment Management"
echo "interface_4/ - Trading & Instrument Management"
echo "interface_5/ - Reporting & Notifications"
echo ""
echo "Note: Some files may be renamed with suffixes (e.g., _db, _ft) to avoid conflicts when the same API exists in multiple source directories."