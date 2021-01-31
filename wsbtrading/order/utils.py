import logging
from time import sleep

import alpaca_trade_api as tradeapi
import pandas as pd

from wsbtrading.instrumentation import Alpaca as iAlpaca


def api_start():
    api_key = iAlpaca.api_key
    api_secret = iAlpaca.api_secret
    base_url = iAlpaca.live_trading_url
    api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')

    return api


def time_to_market_close() -> float:
    """Calculate the time (seconds) until the market closes

    Note:
        this is mostly to be used to stop ourselves from making orders to soon before the bell closes.

    **Example**

    .. code-block:: python

        from wsbtrading.order import utils
        utils.time_to_market_close()
    """
    api = api_start()
    clock = api.get_clock()

    return (clock.next_close - clock.timestamp).total_seconds()


def wait_for_market_open():
    """Function to make ourselves wait for the market to open.

    **Example**

    .. code-block:: python

        from wsbtrading.order import utils
        utils.time_to_market_close()
    """
    api = api_start()
    clock = api.get_clock()
    if not clock.is_open:
        time_to_open = (clock.next_open - clock.timestamp).total_seconds()
        sleep(round(time_to_open))
