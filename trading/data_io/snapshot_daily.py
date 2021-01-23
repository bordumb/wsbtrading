import yfinance as yf
from typing import Optional, List
from abc import abstractmethod
import csv
import pandas
import pandas.io.data as web
import os

os.chdir('trading/data/')


class CSV:
    @abstractmethod
    def writerow(self, row: List[str]) -> None:
        pass

    @abstractmethod
    def writerows(self, rows: List[List[str]]) -> None:
        pass

    @abstractmethod
    def dialect(self) -> csv.Dialect:
        pass


def create_daily_snapshot(start_dt: str, end_dt: str, file_name: Optional[str] = 'stock_tickers.csv',
                          stock_tickers: Optional[List[str]] = None) -> CSV:
    """Takes in a csv of stock tickers and outputs financial data.

    Args:
        start_dt: the first day to pull data
        end_dt: the last day to pull data
        file_name: the path to the stock ticker data

    Returns:
        one csv per each stock ticker in the input file

    Note:
        this may create many files on your computer

    **Example**

    .. code-block:: python

        from trading.data_io import snapshot_daily
        snapshot_daily.create_daily_snapshot(start_dt='2021-01-01', end_dt='2021-01-01')
        snapshot_daily.create_daily_snapshot(start_dt='2017-01-01', end_dt='2017-04-30', stock_tickers=['AAPL', 'GME'])
    """
    # TODO: swap out yfinance for something else
    if stock_tickers is None:
        df = pandas.read_csv(file_name)
        for ticker in df['stock_ticker']:
            data = yf.download(tickers=ticker, start=start_dt, end=end_dt)
            data.to_csv(f'prices/snapshot/daily/{ticker}.csv')
    else:
        for ticker in stock_tickers:
            data = yf.download(tickers=ticker, start=start_dt, end=end_dt)
            data.to_csv(f'prices/snapshot/daily/{ticker}.csv')


from pandas_datareader import data

# Only get the adjusted close.
aapl = data.DataReader("AAPL",
                       start='2020-1-1',
                       end='2020-1-1',
                       data_source='nasdaq')['Adj Close']


data.DataReader(ticker, 'google', start_date, end_date)

