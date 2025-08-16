from .add_new_trade_for_fund import add_new_trade_for_fund
from .add_new_user import add_new_user
from .assign_user_to_handle_investor_or_fund import assign_user_to_handle_investor_or_fund
from .create_nav_record import create_nav_record
from .create_new_fund import create_new_fund
from .fetch_instruments_with_its_price import fetch_instruments_with_its_price
from .fetch_investors_with_portfolio_holdings import fetch_investors_with_portfolio_holdings
from .fetch_user_by_mail import fetch_user_by_mail
from .find_reports import find_reports
from .get_daily_profit_loss_by_fund import get_daily_profit_loss_by_fund
from .get_fund_trade_details import get_fund_trade_details
from .get_fund_valuation import get_fund_valuation
from .get_nav_records import get_nav_records
from .notify_user import notify_user
from .retrieve_funds_with_filter import retrieve_funds_with_filter
from .retrieve_subscriptions import retrieve_subscriptions
from .update_fund_details import update_fund_details
from .update_instrument_price import update_instrument_price
from .update_nav_record_value import update_nav_record_value
from .update_trade import update_trade


ALL_TOOLS_INTERFACE_2 = [
    add_new_trade_for_fund,
    add_new_user,
    assign_user_to_handle_investor_or_fund,
    create_nav_record,
    create_new_fund,
    fetch_instruments_with_its_price,
    fetch_investors_with_portfolio_holdings,
    fetch_user_by_mail,
    find_reports,
    get_daily_profit_loss_by_fund,
    get_fund_trade_details,
    get_fund_valuation,
    get_nav_records,
    notify_user,
    retrieve_funds_with_filter,
    retrieve_subscriptions,
    update_fund_details,
    update_instrument_price,
    update_nav_record_value,
    update_trade
]
