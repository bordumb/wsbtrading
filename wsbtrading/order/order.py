import requests
import json
from typing import Dict, Any

# TODO: Turn these keys into environment variables for security (fine for now as it's paper wsbtrading)
API_KEY = 'PK2TECTJURINF9NGBQT8'
SECRET_KEY = 'q4JCbfISvU3Gq6sLY2dnAr95fs1Ljnut8z3peNw1'

BASE_URL = 'https://paper-api.alpaca.markets'
ACCOUNT_URL = f'{BASE_URL}/v2/account'
ORDERS_URL = f'{BASE_URL}/v2/order'
HEADERS = {
    'APCA-API-KEY-ID': API_KEY,
    'APCA-API-SECRET-KEY': SECRET_KEY,
}


def execute_order(stock_ticker: str, qty: int, side: str, type: str, time_in_force: str) -> Dict[str, Any]:
    """Configures and executes an order.

    Args:
        stock_ticker: the company's stock ticker
        qty: the number of shares to purchase
        side: allows you to choose 'buy', 'sell' side (i.e. buying shares or selling them)
        type: possible values for ``type`` are 'market', 'limit', 'stop', 'stop_limit', 'trailing_stop'
        time_in_force: possible values are 'day', 'gtc', 'opg', 'cls', 'ioc', 'fok'. For more info check
        [here](https://alpaca.markets/docs/trading-on-alpaca/orders/#time-in-force)

    Returns:
        a float representing one number that was divided by another number

    **Example**

    .. code-block:: python

        from wsbtrading.order import execute_order
        execute_order(symbol='AAPL', qty=100, side='buy', type='market', time_in_force='gtc')
    """
    # TODO: add support for more complex order types (https://alpaca.markets/docs/trading-on-alpaca/orders/#bracket-orders)
    data = {
        "symbol": stock_ticker,
        "qty": qty,
        "side": side,
        "type": type,
        "time_in_force": time_in_force
    }

    r = requests.post(ORDERS_URL, json=data, headers=HEADERS)

    return json.loads(r.content)


def get_orders():
    """Returns a JSON blog of open order.

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

        from wsbtrading.order import get_orders
        get_orders()
    """
    r = requests.get(ORDERS_URL, headers=HEADERS)

    return json.loads(r.content)
