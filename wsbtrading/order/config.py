# --------
# Alpaca |
# --------
class Alpaca:
    api_key = 'PK2TECTJURINF9NGBQT8'
    secret_key = 'q4JCbfISvU3Gq6sLY2dnAr95fs1Ljnut8z3peNw1'
    urls = {
        'base_url': 'https://paper-api.alpaca.markets',
        'account_url': f'{BASE_URL}/v2/account',
        'actionContext': f'{BASE_URL}/v2/order',
    }
    headers = {
        'APCA-API-KEY-ID': api_key,
        'APCA-API-SECRET-KEY': secret_key,
    }

