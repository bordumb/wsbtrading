import alpaca_trade_api as tradeapi

from wsbtrading.instrumentation import Alpaca as iAlpaca


def alpaca_rest_api_conn(trading_type: str):
    """Creates the initial connection to Alpaca API.

    Args:
        trading_type: denotes live versus paper trading

    Returns:
        an API connection to Alpaca

    Note:
        this may create many files on your computer

    **Example**

    .. code-block:: python

        from wsbtrading.data_io import data_io
        alpaca_api = data_io.alpaca_rest_api_conn(trading_type='paper_trading')
    """
    api_key = iAlpaca.api_key
    secret_key = iAlpaca.secret_key
    base_url = iAlpaca.api_call[trading_type]['base_url']

    return tradeapi.REST(api_key, secret_key, base_url=base_url)


# import config
# import websocket
# import json
# import requests

# def on_open(ws):
#     print("opened")
#     auth_data = {
#         "action": "authenticate",
#         "data": {"key_id": config.API_KEY, "secret_key": config.SECRET_KEY}
#     }
#
#     ws.send(json.dumps(auth_data))
#
#     listen_message = {"action": "listen", "data": {"streams": ["AM.TSLA"]}}
#
#     ws.send(json.dumps(listen_message))
#
#
# def on_message(ws, message):
#     print("received a message")
#     print(message)
#
#
# def on_close(ws):
#     print("closed connection")
#
#
# socket = "wss://data.alpaca.markets/stream"
#
#
# ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message, on_close=on_close)
# ws.run_forever()
