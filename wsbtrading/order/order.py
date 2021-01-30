import requests
import json
from typing import Dict, Any

from wsbtrading.instrumentation import Alpaca as iAlpaca


def execute_order(stock_ticker: str, qty: int, side: str, type: str, time_in_force: str, trading_type: str) \
        -> Dict[str, Any]:
    """Configures and executes an order.

    Args:
        stock_ticker: the company's stock ticker
        qty: the number of shares to purchase
        side: allows you to choose 'buy', 'sell' side (i.e. buying shares or selling them)
        type: possible values for ``type`` are 'market', 'limit', 'stop', 'stop_limit', 'trailing_stop'
        time_in_force: possible values are 'day', 'gtc', 'opg', 'cls', 'ioc', 'fok'. For more info check
        trading_type: denotes live versus paper trading
        [here](https://alpaca.markets/docs/trading-on-alpaca/orders/#time-in-force)

    Returns:
        a float representing one number that was divided by another number

    **Example**

    .. code-block:: python

        from wsbtrading.order import order
        order.execute_order(
            stock_ticker='TSLA',
            qty=10,
            side='buy',
            type='market',
            time_in_force='gtc',
            trading_type='paper_trading'
        )
    """
    order_url = iAlpaca.api_call[trading_type]['sub_urls']['order_url']
    headers = iAlpaca.headers
    # TODO: add support for more complex order types (https://alpaca.markets/docs/trading-on-alpaca/orders/#bracket-orders)
    data = {
        "symbol": stock_ticker,
        "qty": qty,
        "side": side,
        "type": type,
        "time_in_force": time_in_force
    }

    r = requests.post(url=order_url, json=data, headers=headers)

    return json.loads(r.content)


def get_orders(trading_type: str) -> Dict[str, Any]:
    """Returns a JSON blog of open order(s).

    Args:
        trading_type: denotes live versus paper trading

    Returns:
    .. code-block:

        [{'id': 'acd7cfe6-086b-4ff7-a10d-3eb7ec84b3c7', 'client_order_id': '8e77087b-b548-4a19-a81b-7ad030beeb3d',
        'created_at': '2021-01-23T17:21:02.916741Z', 'updated_at': '2021-01-23T17:21:02.916741Z',
        'submitted_at': '2021-01-23T17:21:02.90977Z', 'filled_at': None, 'expired_at': None, 'canceled_at': None,
        'failed_at': None, 'replaced_at': None, 'replaced_by': None, 'replaces': None,
        'asset_id': 'b0b6dd9d-8b9b-48a9-ba46-b9d54906e415', 'symbol': 'AAPL', 'asset_class': 'us_equity',
        'qty': '100', 'filled_qty': '0', 'filled_avg_price': None, 'order_class': '', 'order_type': 'market',
        'type': 'market', 'side': 'buy', 'time_in_force': 'gtc', 'limit_price': None, 'stop_price': None,
        'status': 'accepted', 'extended_hours': False, 'legs': None, 'trail_percent': None, 'trail_price': None,
        'hwm': None}]

    More info [here](https://alpaca.markets/docs/api-documentation/api-v2/orders/)

    **Example**

    .. code-block:: python

        from wsbtrading.order import order
        order.get_orders(trading_type='paper_trading')
    """
    order_url = iAlpaca.api_call[trading_type]['sub_urls']['order_url']
    headers = iAlpaca.headers

    r = requests.get(order_url, headers=headers)

    return json.loads(r.content)
