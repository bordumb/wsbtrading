import requests
import json

from typing import Dict

from wsbtrading.instrumentation import Alpaca as iAlpaca


def get_account(trading_type: str) -> Dict[str, str]:
    """Returns a JSON blog of open order.

    Args:
        trading_type: denotes live versus paper trading

    Returns:
        a dictionary of account information, such as cash on hand, account value, etc.

    Sample:

    .. code-block:

        {'id': '7f8378b3-84b2-4d4d-8b91-d182aee8945a', 'account_number': 'PA31K6O18XZ4', 'status': 'ACTIVE',
         'currency': 'USD', 'buying_power': '385964', 'regt_buying_power': '185964',
         'daytrading_buying_power': '385964', 'cash': '100000', 'portfolio_value': '100000',
         'pattern_day_trader': False, 'trading_blocked': False, 'transfers_blocked': False, 'account_blocked': False,
         'created_at': '2021-01-22T01:28:41.55866Z', 'trade_suspended_by_user': False, 'multiplier': '4',
         'shorting_enabled': True, 'equity': '100000', 'last_equity': '100000', 'long_market_value': '0',
         'short_market_value': '0', 'initial_margin': '7018', 'maintenance_margin': '0', 'last_maintenance_margin': '0',
         'sma': '0', 'daytrade_count': 0}

    More info [here](https://alpaca.markets/docs/api-documentation/api-v2/account/)

    **Example**

    .. code-block:: python

        from wsbtrading.order import account
        account.get_account(trading_type='paper_trading')
    """
    account_url = iAlpaca.api_call[trading_type]['sub_urls']['account_url']
    headers = iAlpaca.headers

    r = requests.get(account_url, headers=headers)

    return json.loads(r.content)
