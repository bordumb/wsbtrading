import requests
import json

# TODO: Turn these keys into environment variables for security (fine for now as it's paper trading)
API_KEY = 'PK2TECTJURINF9NGBQT8'
SECRET_KEY = 'q4JCbfISvU3Gq6sLY2dnAr95fs1Ljnut8z3peNw1'

BASE_URL = 'https://paper-api.alpaca.markets'
ACCOUNT_URL = f'{BASE_URL}/v2/account'
ORDERS_URL = f'{BASE_URL}/v2/orders'
HEADERS = {
    'APCA-API-KEY-ID': API_KEY,
    'APCA-API-SECRET-KEY': SECRET_KEY,
}

def get_account():
    r = requests.get(ACCOUNT_URL, headers=HEADERS)

    return json.load(r.content)

def create_order(symbol, qty, side, type, time_in_force):
    data = {
        "symbol": symbol,
        "qty": qty,
        "side": side,
        "type": type,
        "time_in_force": time_in_force
    }

    r = requests.post(ORDERS_URL, json=data, headers=HEADERS)

    return json.loads(r.content)

def get_orders():
    r = requests.get(ORDERS_URL, headers=HEADERS)

    return json.loads(r.content)

create_order(symbol="AAPL", qty=100, side="buy", type="market", time_in_force="gtc")

orders = get_orders()
print(orders)