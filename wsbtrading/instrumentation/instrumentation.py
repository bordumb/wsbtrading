# --------
# Alpaca |
# --------
class Alpaca:
    # TODO: Turn these keys into environment variables for security (fine for now as it's paper wsbtrading)
    api_key = 'PK847B96RX8C9GJ3AMO7'
    secret_key = '3ZdZzKEXYwJQxQtq7JNK0KDeatZXzvQSvAwZPuqh'

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
                'order_url': f'{live_trading_url}/v2/orders',
            }
        },
        'paper_trading': {
            'base_url': 'https://paper-api.alpaca.markets',
            'sub_urls': {
                'account_url': f'{paper_trading_url}/v2/account',
                'order_url': f'{paper_trading_url}/v2/orders',
            }
        }
    }


# -----------------
# Alpha Advantage |
# https://www.alphavantage.co/documentation/#listing-status
# -----------------
class AlphaAdvantage:
    # TODO: Turn these keys into environment variables for security (fine for now as it's paper wsbtrading)
    api_key = 'XQ6PZ3J5YFU4VRIS'
