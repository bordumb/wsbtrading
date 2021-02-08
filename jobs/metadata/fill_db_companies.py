import csv
import psycopg2

from wsbtrading.data_io import data_io


conn, cur = data_io.postgres_conn()

csv_path = f'../../data/prod/stock_tickers/daily/date=2021-02-07/file.csv'


def get_table_field_names(table_name: str):
    """Queries the field names of a given table.

    Args:
        table_name: the name of the table to query

    Returns:
        a list of column names

    **Example**

    .. code-block:: python

        mapped_df = get_table_field_names(table_name='company_listing_status')
    """
    try:
        cur.execute(f'Select * FROM {table_name} LIMIT 0')
        col_names = [desc[0] for desc in cur.description]
    except psycopg2.Error as e:
        print(f'error: {e}')

    return col_names


def insert_csv_to_sql(table_name: str, csv_path: str, delimiter: str = ','):
    """Given a SQL table.

    Args:
        table_name: the name of the table to query
        csv_path: the path to the data file to import
        delimiter: the type of delimiter for the file

    **Example**

    .. code-block:: python

        insert_csv_to_sql(table_name='company_listing_status', csv_path='../file.csv')
    """
    col_names = get_table_field_names(table_name=table_name)

    try:
        csv_contents = open(csv_path, 'r')
        next(csv_contents)
    except psycopg2.Error as e:
        print(f'error: {e}')

    try:
        cur.copy_from(file=csv_contents,
                      table=table_name,
                      columns=col_names,
                      sep=delimiter)
        conn.commit()
        cur.close()
        conn.close()
        print("Success!")
    except psycopg2.Error as e:
        print(f'error: {e}')


def main():
    # ---------------
    # Create Table  |
    # ---------------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS company_listing_status(
        id text,
        symbol text,
        name text,
        exchange text,
        assetType text,
        ipoDate text,
        delistingDate text,
        status text,
        date_created text
    )
    """)
    conn.commit()

    # ---------------
    # Insert Data   |
    # ---------------
    insert_csv_to_sql(table_name='company_listing_status', csv_path=csv_path)


if __name__ == '__main__':
    main()
