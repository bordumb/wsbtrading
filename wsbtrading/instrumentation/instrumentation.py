# --------
# Alpaca |
# --------
class Alpaca:
    # TODO: Turn these keys into environment variables for security (fine for now as it's paper wsbtrading)
    api_key = 'PK2TECTJURINF9NGBQT8'
    secret_key = 'q4JCbfISvU3Gq6sLY2dnAr95fs1Ljnut8z3peNw1'

    headers = {
        'APCA-API-KEY-ID': api_key,
        'APCA-API-SECRET-KEY': secret_key,
    }

    live_trading_url = 'https://api.alpaca.markets'
    paper_trading_url = 'https://paper-api.alpaca.markets'

    api_call = {
        'live_trading': {
            'base_url': 'https://api.alpaca.markets',
            'sub_urls': {
                'account_url': f'{live_trading_url}/v2/account',
                'order': f'{live_trading_url}/v2/order',
            }
        },
        'paper_trading': {
            'base_url': 'https://paper-api.alpaca.markets',
            'sub_urls': {
                'account_url': f'{paper_trading_url}/v2/account',
                'order': f'{paper_trading_url}/v2/order',
            }
        }
    }

