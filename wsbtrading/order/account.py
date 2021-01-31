import requests
import json
import alpaca_trade_api as tradeapi

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

        Account({'account_blocked': False,
                 'account_number': 'PA3CXEIHWXHP',
                 'buying_power': '3990803.201',
                 'cash': '1000000',
                 'created_at': '2021-01-30T16:30:05.404915Z',
                 'currency': 'USD',
                 'daytrade_count': 0,
                 'daytrading_buying_power': '3990803.201',
                 'equity': '1000000',
                 'id': 'f53f4501-58b1-4527-b565-8b1cf61dfb17',
                 'initial_margin': '4598.3995',
                 'last_equity': '1000000',
                 'last_maintenance_margin': '0',
                 'long_market_value': '0',
                 'maintenance_margin': '0',
                 'multiplier': '4',
                 'pattern_day_trader': False,
                 'portfolio_value': '1000000',
                 'regt_buying_power': '1990803.201',
                 'short_market_value': '0',
                 'shorting_enabled': True,
                 'sma': '0',
                 'status': 'ACTIVE',
                 'trade_suspended_by_user': False,
                 'trading_blocked': False,
                 'transfers_blocked': False})

    More info [here](https://alpaca.markets/docs/api-documentation/api-v2/account/)

    **Example**

    .. code-block:: python

        from wsbtrading.order import account
        account.get_account(trading_type='paper_trading')
    """
    base_url = iAlpaca.api_call[trading_type]['base_url']
    api_key = iAlpaca.api_key
    api_secret = iAlpaca.api_secret

    api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')

    return api.get_account()
