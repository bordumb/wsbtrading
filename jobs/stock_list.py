import yfinance as yf
import pandas as pd
from datetime import datetime

from typing import List, Optional, Union

from wsbtrading.data_io import data_io
from wsbtrading.instrumentation import AlphaAdvantage as iAlphaAdvantage

ticker_list = ['AAPL']
start_dt = '1950-01-01'
end_dt = '2021-02-01'

for ticker in ticker_list:
    pandas_df = yf.download(tickers=ticker, start=start_dt, end=end_dt)
    pandas_df['stock_ticker'] = ticker
    pandas_df.to_csv(f'data/prices/snapshot/daily/{ticker}.csv')

    spark_df = spark.createDataFrame(pandas_df)

path_to_write = data_io.generate_path_to_write(environment='prod',
                                               granularity='daily',
                                               dataset_name='daily_prices')


def pull_company_listing_status():
    """Pulls a list of de-listed companies from Alpha Advantage (www.alphavantage.co/documentation/)

    The ``impressions`` schema is:

    .. code-block::

        root
        |-- symbol: string (nullable = true)
        |-- name: string (nullable = true)
        |-- assetType: string (nullable = true)
        |-- ipoDate: date (nullable = true)
        |-- delistingDate: date (nullable = true)
        |-- status: date (nullable = true)
    """
    api_key = iAlphaAdvantage.api_key
    appended_data = []
    for state in ['delisted', 'listed']:
        api_url = f'https://www.alphavantage.co/query?function=LISTING_STATUS&state={state}&apikey={api_key}'
        df = pd.read_csv(f'{api_url}')
        appended_data.append(df)
    df = pd.concat(appended_data)
    df['date_created'] = datetime.today().strftime('%Y-%m-%d')
    return df

df = pull_company_listing_status()
df

def yahoo_price_pull(start_dt: str, end_dt: str, file_name: Optional[str] = 'stock_tickers.csv',
                     stock_tickers: Optional[List[str]] = None) -> 'DataFrame':
    """Filters the dataframe, after the mapper but before the reducer.

    Args:
        df: the dataframe, typically after filtering

    Returns:
        The filtered dataframe.
    """
    df = pandas.read_csv(file_name)
    for ticker in ticker_list:
        pandas_df = yf.download(tickers=ticker, start=start_dt, end=end_dt)
        pandas_df['stock_ticker'] = ticker
        pandas_df.to_csv(f'prices/snapshot/daily/{ticker}.csv')

        spark_df = spark.createDataFrame(pandas_df)

    if stock_tickers is None:
        df = pandas.read_csv(file_name)
        for ticker in df['stock_ticker']:
            pandas_df = yf.download(tickers=ticker, start=start_dt, end=end_dt)
            spark_df = pandas_to_spark(pandas_df)
    else:
        for ticker in stock_tickers:
            data = yf.download(tickers=ticker, start=start_dt, end=end_dt)
            data.to_csv(f'prices/snapshot/daily/{ticker}.csv')


def main():
    # -------------------------------------------------
    # TV: Read, filter, map dimensions, map measures  |
    # -------------------------------------------------
    video_clickstream_raw = data_io.read_from_hdfs(spark_session=SPARK_SESSION,
                                                   dataset_name='clickstream:video:t1-enriched-utc',
                                                   start_date=DATE_TO_READ,
                                                   end_date=DATE_TO_READ)

    video_clickstream_raw = video_clickstream_raw.repartition(1600)

    aggregate_raw = aggregate_raw \
        .fillna('ALL_ITEMS', subset=grouping_fields) \
        .withColumn('rptg_dt', lit(DATE_TO_READ))

    # --------
    # Write  |
    # --------
    path_to_write = data_io.generate_path_to_write(environment='prod',
                                                   granularity='daily',
                                                   dataset_name='test_dataset')

    aggregate_raw.repartition(10).write.mode('overwrite').parquet(path_to_write)


if __name__ == '__main__':
    main()
