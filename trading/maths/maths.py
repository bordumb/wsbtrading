"""Functions to aid in quick maths to calculate for ad-hoc analysis and feature engineering."""
from typing import Optional, List

from trading import check_columns


def divide_kernel(numerator: float, denominator: float) -> float:
    """Divides one number by another number.

    Args:
        numerator: the number for the top of your fraction
        denominator: the number for the bottom of your fraction

    Returns:
        a float representing one number that was divided by another number

    **Example**

    .. code-block:: python

        from trading.maths
        maths.divide_kernel(numerator=3, denominator=9)
    """
    if denominator == 0:
        return 0
    return numerator / denominator


def divide(df: 'DataFrame', numerator_col: str, denominator_col: str) -> 'DataFrame':
    """Divides one number by another.

    Args:
        df: the dataframe to append a column onto
        numerator_col: the name of your numerator column
        denominator_col: the name of your denominator column

    Returns:
        the original dataframe with the division result appended

    **Example**

    .. code-block:: python

        from trading import maths
        df_mapped = maths.divide(df=df)
    """
    df = df.copy()
    check_columns(dataframe=df, required_columns=[numerator_col, denominator_col])

    df[f'{numerator_col}_perc_{denominator_col}'] = df[numerator_col] / df[denominator_col]
    return df


def sma(df: 'Dataframe', metric_col: str, rolling_window: Optional[int] = 20) -> 'DataFrame':
    """Calculates the simple moving average (SMA) over a given time window.

    Args:
        df: the dataframe to append a column onto
        metric_col: the column to calculate over (usually the 'Close' price)
        rolling_window: the time window to calculate over

    Returns:
        the original dataframe with the moving average appended

    **Example**

    .. code-block:: python

        from trading import maths
        df_mapped = maths.sma(df=df, metric_col='Close', rolling_window=20)
    """
    df = df.copy()
    rolling_window_string = str(rolling_window)

    df[f'{rolling_window_string}sma'] = df[metric_col].rolling(window=rolling_window).mean()
    return df


def rolling_stddev(df: 'Dataframe', metric_col: str, rolling_window: Optional[int] = 20) -> 'DataFrame':
    """Calculates the moving standard deviation over a given time window.

    Args:
        df: the dataframe to append a column onto
        metric_col: the column to calculate over (usually the 'Close' price)
        rolling_window: the time window to calculate over

    Returns:
        the original dataframe with the moving standard deviation appended

    **Example**

    .. code-block:: python

        from trading import maths
        df_mapped = maths.rolling_stddev(df=df, metric_col='Close', rolling_window=20)
    """
    df = df.copy()
    rolling_window_string = str(rolling_window)

    df[f'{rolling_window_string}stddev'] = df[metric_col].rolling(window=rolling_window).std()
    return df


def lower_band(df: 'Dataframe', metric_col: str, rolling_window: Optional[int] = 20) -> 'DataFrame':
    """Calculates the lower bound of a stock's price movements.

    Args:
        df: the dataframe to append a column onto
        metric_col: the column to calculate over (usually the 'Close' price)
        rolling_window: the time window to calculate over

    Returns:
        the original dataframe with the lower bound appended

    **Example**

    .. code-block:: python

        from trading import maths
        df_mapped = maths.lower_band(df=df, metric_col='Close')
    """
    rolling_window_string = str(rolling_window)

    df = sma(df=df, metric_col=metric_col, rolling_window=rolling_window)
    df = rolling_stddev(df=df, metric_col=metric_col, rolling_window=rolling_window)

    df['lower_band'] = df[f'{rolling_window_string}sma'] - (2 * df[f'{rolling_window_string}stddev'])
    return df


def upper_band(df: 'Dataframe', metric_col: str, rolling_window: Optional[int] = 20) -> 'DataFrame':
    """Calculates the lower bound of a stock's price movements.

    Args:
        df: the dataframe to append a column onto
        metric_col: the column to calculate over (usually the 'Close' price)
        rolling_window: the time window to calculate over

    Returns:
        the original dataframe with the lower bound appended

    **Example**

    .. code-block:: python

        from trading import maths
        df_mapped = maths.upper_band(df=df, metric_col='Close')
    """
    rolling_window_string = str(rolling_window)

    df = sma(df=df, metric_col=metric_col, rolling_window=rolling_window)
    df = rolling_stddev(df=df, metric_col=metric_col, rolling_window=rolling_window)

    df['upper_band'] = df[f'{rolling_window_string}sma'] + (2 * df[f'{rolling_window_string}stddev'])
    return df


def true_range(df: 'Dataframe', low_col: str, high_col: str) -> 'DataFrame':
    """Calculates the true range (TR) for a stocks price movement.

    Args:
        df: the dataframe to append a column onto
        low_col: the column with the low price
        high_col: the column with the high price

    Returns:
        the original dataframe with the true range appended

    **Example**

    .. code-block:: python

        from trading import maths
        df_mapped = maths.true_range(df=df, low_col='Low', high_col='High')
    """
    df = df.copy()
    df['true_range'] = abs(df[high_col] - df[low_col])
    return df


def avg_true_range(df: 'Dataframe', low_col: str, high_col: str, rolling_window: Optional[int] = 20) -> 'DataFrame':
    """Calculates the true range (TR) for a stocks price movement over a given time window.

    Args:
        df: the dataframe to append a column onto
        low_col: the column with the low price
        high_col: the column with the high price
        rolling_window: the time window to calculate over

    Returns:
        the original dataframe with the true range appended

    **Example**

    .. code-block:: python

        from trading import maths
        df_mapped = maths.avg_true_range(df=df, low_col='Low', high_col='High', rolling_window=20)
    """
    df = df.copy()
    df = true_range(df=df, low_col=low_col, high_col=high_col)

    df['ATR'] = df['true_range'].rolling(window=rolling_window).mean()
    return df


def lower_keltner(df: 'Dataframe', metric_col: str, low_col: str, high_col: str, rolling_window: Optional[int] = 20) \
        -> 'DataFrame':
    """Calculates the lower Keltner of a stock's price movements.

    Args:
        df: the dataframe to append a column onto
        metric_col: the column to calculate over (usually the 'Close' price)
        low_col: the column with the low price
        high_col: the column with the high price
        rolling_window: the time window to calculate over

    Returns:
        the original dataframe with the lower bound appended

    **Example**

    .. code-block:: python

        from trading import maths
        df_mapped = maths.lower_keltner(df=df, metric_col='Close', low_col='Low', high_col='High', rolling_window=20)
    """
    rolling_window_string = str(rolling_window)

    df = sma(df=df, metric_col=metric_col, rolling_window=rolling_window)
    # df = rolling_stddev(df=df, metric_col=metric_col, rolling_window=rolling_window)
    df = avg_true_range(df=df, low_col=low_col, high_col=high_col, rolling_window=rolling_window)

    df['lower_keltner'] = df[f'{rolling_window_string}sma'] - (df['ATR'] * 1.5)
    return df


def upper_keltner(df: 'Dataframe', metric_col: str, low_col: str, high_col: str, rolling_window: Optional[int] = 20) \
        -> 'DataFrame':
    """Calculates the upper Keltner of a stock's price movements.

    Args:
        df: the dataframe to append a column onto
        metric_col: the column to calculate over (usually the 'Close' price)
        low_col: the column with the low price
        high_col: the column with the high price
        rolling_window: the time window to calculate over

    Returns:
        the original dataframe with the lower bound appended

    **Example**

    .. code-block:: python

        from trading import maths
        df_mapped = maths.upper_keltner(df=df, metric_col='Close', low_col='Low', high_col='High', rolling_window=20)
    """
    rolling_window_string = str(rolling_window)

    df = sma(df=df, metric_col=metric_col, rolling_window=rolling_window)
    # df = rolling_stddev(df=df, metric_col=metric_col, rolling_window=rolling_window)
    df = avg_true_range(df=df, low_col=low_col, high_col=high_col, rolling_window=rolling_window)

    df['upper_keltner'] = df[f'{rolling_window_string}sma'] + (df['ATR'] * 1.5)
    return df


def is_in_squeeze(df: 'Dataframe', metric_col: str, low_col: str, high_col: str, look_back_period: Optional[int] = -3,
                  rolling_window: Optional[int] = 20) -> bool:
    """Calculates whether a stock's price moments are indicative of an upcoming squeeze (i.e. going to the moon!🚀🚀🚀).

    Args:
        df: the dataframe to append a column onto
        metric_col: the column to calculate over (usually the 'Close' price)
        low_col: the column with the low price
        high_col: the column with the high price
        look_back_period: the number of days to look back
        rolling_window: the time window to calculate over

    Returns:
        the original dataframe with the lower bound appended

    **Example**

    .. code-block:: python

        from trading import maths
        df_mapped = maths.is_in_squeeze(
            df=df,
            metric_col='Close',
            low_col='Low',
            high_col='High',
            rolling_window=20
        )
    """
    lower_band_df = lower_band(df=df, metric_col=metric_col)
    upper_band_df = upper_band(df=lower_band_df, metric_col=metric_col)
    lower_keltner_df = lower_keltner(df=upper_band_df, metric_col=metric_col, low_col=low_col, high_col=high_col,
                                     rolling_window=rolling_window)
    upper_keltner_df = upper_keltner(df=lower_keltner_df, metric_col=metric_col, low_col=low_col, high_col=high_col,
                                     rolling_window=rolling_window)

    return upper_keltner_df['lower_band'].iloc[look_back_period] \
           > upper_keltner_df['lower_keltner'].iloc[look_back_period] \
           and upper_keltner_df['upper_band'].iloc[look_back_period] \
           < upper_keltner_df['upper_keltner'].iloc[look_back_period]
