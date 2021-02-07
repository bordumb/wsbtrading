import pandas as pd
from datetime import datetime

from typing import List, Optional, Union

from wsbtrading.data_io import data_io
from wsbtrading.instrumentation import AlphaAdvantage as iAlphaAdvantage

today_date = datetime.today().strftime('%Y-%m-%d')


def pull_company_listing_status() -> 'pd.DataFrame':
    """Pulls a list of de-listed companies from Alpha Advantage (www.alphavantage.co/documentation/)

    The company listing schema is:

    .. code-block::

        root
        |-- symbol: string (nullable = true)
        |-- name: string (nullable = true)
        |-- assetType: string (nullable = true)
        |-- ipoDate: date (nullable = true)
        |-- delistingDate: date (nullable = true)
        |-- status: string (nullable = true); values are ``Delisted`` or ``Active``
        |-- date_created: date (nullable = true)
    """
    api_key = iAlphaAdvantage.api_key
    appended_data = []

    for state in ['delisted', 'listed']:
        api_url = f'https://www.alphavantage.co/query?function=LISTING_STATUS&state={state}&apikey={api_key}'
        df = pd.read_csv(f'{api_url}')
        appended_data.append(df)

    df = pd.concat(appended_data)
    df['date_created'] = today_date

    return df


# TODO: create enhanced metadata, such as days it took to be delisted, age of companies in days, etc.
# def calculate_days_until_delisting(dataframe: 'pd.DataFrame') -> 'pd.DataFrame':
#     df['days_to_delisting'] = date_diff(df['ipoDate'] - df['delistingDate'])


def main():
    # -------
    # Read  |
    # -------
    pandas_df = pull_company_listing_status()

    # --------
    # Write  |
    # --------
    pandas_df.to_csv(f'data/snapshot/stock_ticker_list/daily/date={today_date}.csv')
    # path_to_write = data_io.generate_path_to_write(environment='prod',
    #                                                granularity='daily',
    #                                                dataset_name='stock_ticker_list')
    #
    # aggregate_raw.repartition(10).write.mode('overwrite').parquet(path_to_write)


if __name__ == '__main__':
    main()
