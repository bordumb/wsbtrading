"""Functions to wrangle dates."""

from datetime import datetime, timedelta
from typing import List


def convert_unix_timestamp_to_date_kernel(timestamp: int, output_time: bool = False) -> str:
    """Converts an integer timestamp into date string.

    Args:
        timestamp: the timestamp (in ms) to convert to date string
        output_time: a flag whether to include time in the conversion

    Returns:
        date string extracted out of the timestamp

    **Example**

    .. code-block:: python

        from wsbtrading.utils import dates
        timestamp = 1609459200
        dates.convert_unix_timestamp_to_date_kernel(timestamp=timestamp, output_time=False)
        # '2020-07-01'
        df_mapped = df.withColumn(
            'eventDate',
            dates.convert_unix_timestamp_to_date_kernel.udf(
                col('timestamp'), lit(True)
            )
        )
    """
    return datetime.utcfromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S' if output_time else '%Y-%m-%d')


def parse_date_from_string(date: str) -> datetime:
    """Converts a date from a string to a datetime.

    Args:
        date: the date to parse from string representation to datetime

    Returns:
        datetime object of the date

    **Example**

    .. code-block:: python

        from wsbtrading.utils import dates
        dates.parse_date_from_string('2020-04-20')
    """
    return datetime.strptime(f'{date} 00:00:00', '%Y-%m-%d %H:%M:%S')


def build_date_range(start_date: str, end_date: str) -> List[str]:
    """Creates an array of dates, useful for creating time ranges for analysis.

    Args:
        start_date: the date to start with
        end_date: the date to end with

    Returns:
        list of datetime object filling the range of dates

    **Example**

    .. code-block:: python

        from wsbtrading.utils import dates
        dates.build_date_range(start_date='2020-04-01', end_date='2020-04-03')
        # ['2020-04-01', '2020-04-02', '2020-04-03']
    """
    start_date = parse_date_from_string(start_date)
    end_date = parse_date_from_string(end_date)

    return [(start_date + timedelta(days=+x)).strftime('%Y-%m-%d') for x in range(0, (end_date - start_date).days + 1)]


def date_range_to_unix_range(date_range: List[str]) -> str:
    """Formats an array of dates to a string that can be used in file paths names.

    Args:
        date_range: a list of dates, formatted as YYYY-MM-DD

    Returns:
        a string that looks like a dict filled with dates

    **Example**

    .. code-block:: python

        from wsbtrading.utils import dates
        dates.date_range_to_unix_range(['2020-04-01', '2020-04-02', '2020-04-03'])
        # '{2020-04-01,2020-04-02,2020-04-03}'
    """
    return '{%s}' % ','.join(date_range)


def date_slider(date: str, days_to_add: int) -> str:
    """Takes a date string and shifts it.

    Note:
        useful for times when you want to look back N-number of days, such as looking at time windows

    Args:
        date: the date to be shifted, formatted as YYYY-MM-DD
        days_to_add: the number of days to shift by

    Returns:
        the shifted date

    **Example**

    .. code-block:: python

        from wsbtrading.utils import dates
        dates.date_slider(date='2020-01-01', days_to_add=7)
        # '2020-01-08'
    """
    return (datetime.strptime(date, '%Y-%m-%d') + timedelta(days=days_to_add)).strftime('%Y-%m-%d')
