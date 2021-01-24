import yfinance as yf
from typing import Optional, List
from abc import abstractmethod
import csv
import pandas
import os


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


def write_snapshot(start_dt: str, end_dt: str, file_name: Optional[str] = 'stock_tickers.csv',
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

        from wsbtrading.data_io import snapshot_daily
        snapshot_daily.write_snapshot(start_dt='2021-01-01', end_dt='2021-01-01')
        snapshot_daily.write_snapshot(start_dt='2017-01-01', end_dt='2017-04-30', stock_tickers=['AAPL', 'GME'])
    """
    os.chdir('wsbtrading/data/')
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


def read_snapshot(stock_tickers: Optional[List[str]] = None) -> 'Dataframe':
    """Reads all, some, or one specific stock's financial snapshot dataset.

    Args:
        stock_tickers: the name(s) of the stocks you want to pull

    Returns:
        one csv per each stock ticker in the input file

    Note:
        this may create many files on your computer

    **Example**

    .. code-block:: python

    from wsbtrading.data_io import snapshot_daily
    snapshot_daily.read_snapshot()
    dict_of_df = snapshot_daily.read_snapshot(stock_tickers=['AAPL'])
    """
    dataframes = {}
    base_path = 'wsbtrading/data/prices/snapshot/daily/'
    files = [file_name for file_name in os.listdir(base_path)]
    if stock_tickers is not None:
        # Pull only the files that the user specifies
        select_files = [file_name for file_name in os.listdir(base_path)
                 if any(file_name == stock + '.csv' for stock in stock_tickers)]
        for file_name in select_files:
            symbol = file_name.split(".")[0]
            df = pandas.read_csv(f'{base_path}{file_name}')
            dataframes[symbol] = df
            return dataframes
    else:
        for file_name in files:
            symbol = file_name.split(".")[0]
            df = pandas.read_csv(f'{base_path}{file_name}')
            dataframes[symbol] = df
            return dataframes

#
#
# import os
# import pandas
#
# stock_tickers = ['AAPL']
# dataframes = {}
# base_path = 'wsbtrading/data/prices/snapshot/daily/'
#
# if stock_tickers is not None:
#     # Pull only the files that the user specifies
#     select_files = [file_name for file_name in os.listdir(base_path)
#                     if any(file_name == stock + '.csv' for stock in stock_tickers)]
#     for file_name in select_files:
#         symbol = file_name.split(".")[0]
#         df = pandas.read_csv(f'{base_path}{file_name}')
#         dataframes[symbol] = df
#         dataframes
#
#
# files = [file_name for file_name in os.listdir(base_path)]
# for file_name in files:
#     print(file_name)
#     symbol = file_name.split(".")[0]
#     df = pandas.read_csv(f'{base_path}{file_name}')
#     dataframes[symbol] = df
#     dataframes

