from typing import List
import pandas as pd
from datetime import datetime
import yfinance as yf

from wsbtrading.data_io import data_io
from wsbtrading.instrumentation import AlphaAdvantage as iAlphaAdvantage

today_date = datetime.today().strftime('%Y-%m-%d')
CSV = data_io.CSV
method = 'yfinance'


def get_stock_ticker_list(latest_date: str) -> List[str]:
    """Pulls the csv from data/prod/stock_tickers/daily and
    extracts just a list of the stock tickers from the field `symbol`
    """
    df = pd.read_csv(f'../data/prod/stock_tickers/daily/date={latest_date}/file.csv')
    return df['symbol'].tolist()


def pull_company_prices_daily_alpha_advantage(stock_ticker: str) -> 'pd.DataFrame':
    """Pulls a list of de-listed companies from Alpha Advantage (www.alphavantage.co/documentation/)

    Args:
        stock_ticker: a single stock symbol to pull data for

    The stock prices schema is:

    .. code-block::

        root
        |-- timestamp: date (nullable = true)
        |-- stock_ticker: string (nullable = true)
        |-- open: float (nullable = true)
        |-- high: float (nullable = true)
        |-- low: float (nullable = true)
        |-- close: float (nullable = true)
        |-- adjusted_close: float (nullable = true)
        |-- volume: integer (nullable = true)
        |-- dividend_amount: float (nullable = true)
        |-- split_coefficient: float (nullable = true)
    """
    api_key = iAlphaAdvantage.api_key
    appended_data = []

    api_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={stock_ticker}&outputsize=full&apikey={api_key}&datatype=csv '
    df = pd.read_csv(f'{api_url}')
    df['stock_ticker'] = stock_ticker
    appended_data.append(df)

    return pd.concat(appended_data)


def pull_company_prices_daily_yfinance(stock_ticker: str, start_date: str, end_date: str) -> 'pd.DataFrame':
    """Pulls a list of de-listed companies from YFinance

    Args:
        stock_ticker_list: list of stock symbols to pull data for
        start_date: the date to start looking at stocks
        end_date: the date to end looking at stocks

    The stock prices schema is:

    .. code-block::

        root
        |-- timestamp: date (nullable = true)
        |-- stock_ticker: string (nullable = true)
        |-- open: float (nullable = true)
        |-- high: float (nullable = true)
        |-- low: float (nullable = true)
        |-- close: float (nullable = true)
        |-- adjusted_close: float (nullable = true)
    """
    appended_data = []

    df = yf.download(tickers=stock_ticker, start=start_date, end=end_date)
    df['stock_ticker'] = stock_ticker
    appended_data.append(df)

    return pd.concat(appended_data)


# TODO: Add a similar function for alpaca api and handle json -> (pandas df) -> csv

def main():
    # -------
    # Read  |
    # -------
    stock_ticker_list = get_stock_ticker_list(latest_date='2021-02-07')

    # --------
    # Write  |
    # --------
    start_date = '2000-01-01'
    end_date = '2021-02-01'
    for stock_ticker in stock_ticker_list:
        print(stock_ticker)
        df = pull_company_prices_daily_yfinance(stock_ticker=stock_ticker,
                                                start_date=start_date,
                                                end_date=end_date)
        # df = pull_company_prices_daily_alpha_advantage(stock_ticker=stock_ticker)

        df.to_csv(f'../../data/prod/stock_prices/daily/{stock_ticker}_{start_date}_{end_date}.csv')


if __name__ == '__main__':
    main()
