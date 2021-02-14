"""
This job initially populates the fundamentals_daily table in Postgress from a CSV
TODO: get this automated from Quandl's API
"""
from wsbtrading import data_io


csv_path = f'../../data/prod/fundamentals/daily/fundamentals_daily_20210210.csv'


def main():
    # ---------------
    # Insert Data   |
    # ---------------
    data_io.insert_csv_to_sql(table_name='fundamentals_daily', csv_path=csv_path)


if __name__ == '__main__':
    main()
