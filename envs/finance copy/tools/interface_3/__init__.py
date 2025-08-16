from .add_new_holding import add_new_holding
from .add_new_instrument import add_new_instrument
from .add_new_instrument_price import add_new_instrument_price
from .add_payment import add_payment
from .delete_holding import delete_holding
from .email_user import email_user
from .fetch_invoices import fetch_invoices
from .find_user import find_user
from .generate_report import generate_report
from .get_filtered_investors import get_filtered_investors
from .get_investor_portfolio import get_investor_portfolio
from .get_notifications import get_notifications
from .get_portfolio_holdings import get_portfolio_holdings
from .retrieve_instrument_prices import retrieve_instrument_prices
from .retrieve_instruments import retrieve_instruments
from .retrieve_reports import retrieve_reports
from .summary_of_instrument_types_by_prices import summary_of_instrument_types_by_prices
from .update_instrument import update_instrument
from .update_instrument_price import update_instrument_price
from .update_report_status import update_report_status


ALL_TOOLS_INTERFACE_3 = [
    add_new_holding,
    add_new_instrument,
    add_new_instrument_price,
    add_payment,
    delete_holding,
    email_user,
    fetch_invoices,
    find_user,
    generate_report,
    get_filtered_investors,
    get_investor_portfolio,
    get_notifications,
    get_portfolio_holdings,
    retrieve_instrument_prices,
    retrieve_instruments,
    retrieve_reports,
    summary_of_instrument_types_by_prices,
    update_instrument,
    update_instrument_price,
    update_report_status
]
