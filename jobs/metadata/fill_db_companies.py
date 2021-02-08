import csv

from wsbtrading.data_io import data_io

# alpaca_api = data_io.alpaca_rest_api_conn(trading_type='paper_trading')
#
# minute_bars = alpaca_api.polygon.historic_agg_v2(symbol='Z',
#                                                  multiplier=1,
#                                                  timespan='minute',
#                                                  _from='2020-10-02',
#                                                  to='2020-10-22')
#
# for bar in minute_bars:
#     print(bar.timestamp, bar.open, bar.high, bar.low, bar.close)

conn, cur = data_io.postgres_conn()


def main():
    # ---------------
    # Create Table  |
    # ---------------
    cur.execute("""
        CREATE TABLE company_listing_status(
        id integer,
        symbol text PRIMARY KEY,
        name text,
        exchange text,
        assetType text, 
        ipoDate date, 
        delistingDate date,
        status text,
        date_created date
    )
    """)
    conn.commit()

    csv_path = f'../../data/prod/stock_tickers/daily/date=*/file.csv'

    # ---------------
    # Insert Data   |
    # ---------------
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header row.
        for row in reader:
            cur.execute(
                "INSERT INTO company_listing_status VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                row
            )
    conn.commit()


if __name__ == '__main__':
    main()
