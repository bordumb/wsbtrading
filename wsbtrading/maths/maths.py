"""Functions to aid in quick maths to calculate for ad-hoc analysis and feature engineering."""
from typing import Optional
import pandas as pd
import numpy as np

from wsbtrading import check_columns


def divide_kernel(numerator: float, denominator: float) -> float:
    """Divides one number by another number.

    Args:
        numerator: the number for the top of your fraction
        denominator: the number for the bottom of your fraction

    Returns:
        a float representing one number that was divided by another number

    **Example**

    .. code-block:: python

        from wsbtrading.maths
        maths.divide_kernel(numerator=3, denominator=9)
    """
    if denominator == 0:
        return 0
    return numerator / denominator


def divide(df: 'DataFrame', numerator_col: str, denominator_col: str) -> pd.DataFrame:
    """Divides one number by another.

    Args:
        df: the dataframe to append a column onto
        numerator_col: the name of your numerator column
        denominator_col: the name of your denominator column

    Returns:
        the original dataframe with the division result appended

    **Example**

    .. code-block:: python

        from wsbtrading import maths
        df_mapped = maths.divide(df=df)
    """
    df = df.copy()
    check_columns(dataframe=df, required_columns=[numerator_col, denominator_col])

    df[f'{numerator_col}_perc_{denominator_col}'] = df[numerator_col] / df[denominator_col]
    return df


def sma(df: 'Dataframe', metric_col: str, rolling_window: Optional[int] = 20) -> pd.DataFrame:
    """Calculates the simple moving average (SMA) over a given time window.

    Args:
        df: the dataframe to append a column onto
        metric_col: the column to calculate over (usually the 'Close' price)
        rolling_window: the time window to calculate over

    Returns:
        the original dataframe with the moving average appended

    **Example**

    .. code-block:: python

        from wsbtrading import maths
        df_mapped = maths.sma(df=df, metric_col='Close', rolling_window=20)
    """
    df = df.copy()
    rolling_window_string = str(rolling_window)

    df[f'{rolling_window_string}sma'] = df[metric_col].rolling(window=rolling_window).mean()
    return df


def ema(df: 'Dataframe', metric_col: str, rolling_window: Optional[int] = 20) -> pd.DataFrame:
    """Calculates the exponential moving average (EMA) over a given time window.
    For more on ema versus sma, please [see this article](https://www.investopedia.com/ask/answers/122314/what-exponential-moving-average-ema-formula-and-how-ema-calculated.asp)

    Args:
        df: the dataframe to append a column onto
        metric_col: the column to calculate over (usually the 'Close' price)
        rolling_window: the time window to calculate over

    Returns:
        the original dataframe with the exponential moving average appended

    **Example**

    .. code-block:: python

        from wsbtrading import maths
        df_mapped = maths.ema(df=df, metric_col='Close', rolling_window=20)
    """
    df = df.copy()
    rolling_window_string = str(rolling_window)

    df[f'{rolling_window_string}ema'] = df[metric_col].rolling(window=rolling_window).mean()
    return df


def rolling_stddev(df: 'Dataframe', metric_col: str, rolling_window: Optional[int] = 20) -> pd.DataFrame:
    """Calculates the moving standard deviation over a given time window.

    Args:
        df: the dataframe to append a column onto
        metric_col: the column to calculate over (usually the 'Close' price)
        rolling_window: the time window to calculate over

    Returns:
        the original dataframe with the moving standard deviation appended

    **Example**

    .. code-block:: python

        from wsbtrading import maths
        df_mapped = maths.rolling_stddev(df=df, metric_col='Close', rolling_window=20)
    """
    df = df.copy()
    rolling_window_string = str(rolling_window)

    df[f'{rolling_window_string}stddev'] = df[metric_col].rolling(window=rolling_window).std()
    return df


def lower_band(df: 'Dataframe', metric_col: str, rolling_window: Optional[int] = 20) -> pd.DataFrame:
    """Calculates the lower bound of a stock's price movements.

    Args:
        df: the dataframe to append a column onto
        metric_col: the column to calculate over (usually the 'Close' price)
        rolling_window: the time window to calculate over

    Returns:
        the original dataframe with the lower bound appended

    **Example**

    .. code-block:: python

        from wsbtrading import maths
        df_mapped = maths.lower_band(df=df, metric_col='Close')
    """
    rolling_window_string = str(rolling_window)

    df = sma(df=df, metric_col=metric_col, rolling_window=rolling_window)
    df = rolling_stddev(df=df, metric_col=metric_col, rolling_window=rolling_window)

    df['lower_band'] = df[f'{rolling_window_string}sma'] - (2 * df[f'{rolling_window_string}stddev'])
    return df


def upper_band(df: 'Dataframe', metric_col: str, rolling_window: Optional[int] = 20) -> pd.DataFrame:
    """Calculates the lower bound of a stock's price movements.

    Args:
        df: the dataframe to append a column onto
        metric_col: the column to calculate over (usually the 'Close' price)
        rolling_window: the time window to calculate over

    Returns:
        the original dataframe with the lower bound appended

    **Example**

    .. code-block:: python

        from wsbtrading import maths
        df_mapped = maths.upper_band(df=df, metric_col='Close')
    """
    rolling_window_string = str(rolling_window)

    df = sma(df=df, metric_col=metric_col, rolling_window=rolling_window)
    df = rolling_stddev(df=df, metric_col=metric_col, rolling_window=rolling_window)

    df['upper_band'] = df[f'{rolling_window_string}sma'] + (2 * df[f'{rolling_window_string}stddev'])
    return df


def true_range(df: 'Dataframe', low_col: str, high_col: str) -> pd.DataFrame:
    """Calculates the true range (TR) for a stocks price movement.

    Args:
        df: the dataframe to append a column onto
        low_col: the column with the low price
        high_col: the column with the high price

    Returns:
        the original dataframe with the true range appended

    **Example**

    .. code-block:: python

        from wsbtrading import maths
        df_mapped = maths.true_range(df=df, low_col='Low', high_col='High')
    """
    df = df.copy()
    df['true_range'] = abs(df[high_col] - df[low_col])
    return df


def avg_true_range(df: 'Dataframe', low_col: str, high_col: str, rolling_window: Optional[int] = 20) -> pd.DataFrame:
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

        from wsbtrading import maths
        df_mapped = maths.avg_true_range(df=df, low_col='Low', high_col='High', rolling_window=20)
    """
    df = df.copy()
    df = true_range(df=df, low_col=low_col, high_col=high_col)

    df['ATR'] = df['true_range'].rolling(window=rolling_window).mean()
    return df


def lower_keltner(df: 'Dataframe', metric_col: str, low_col: str, high_col: str, rolling_window: Optional[int] = 20) \
        -> pd.DataFrame:
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

        from wsbtrading import maths
        df_mapped = maths.lower_keltner(df=df, metric_col='Close', low_col='Low', high_col='High', rolling_window=20)
    """
    rolling_window_string = str(rolling_window)

    df = sma(df=df, metric_col=metric_col, rolling_window=rolling_window)
    df = avg_true_range(df=df, low_col=low_col, high_col=high_col, rolling_window=rolling_window)

    df['lower_keltner'] = df[f'{rolling_window_string}sma'] - (df['ATR'] * 1.5)
    return df


def upper_keltner(df: 'Dataframe', metric_col: str, low_col: str, high_col: str, rolling_window: Optional[int] = 20) \
        -> pd.DataFrame:
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

        from wsbtrading import maths
        df_mapped = maths.upper_keltner(df=df, metric_col='Close', low_col='Low', high_col='High', rolling_window=20)
    """
    rolling_window_string = str(rolling_window)

    df = sma(df=df, metric_col=metric_col, rolling_window=rolling_window)
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

        from wsbtrading import maths
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


def calculate_turbulence(df: 'Dataframe', date_col: str, adjusted_close: str, stock_ticker_col: Optional[str] = None) -> pd.DataFrame:
    """Calculates the .

    Note:

    Args:
        df: the dataframe to append a column onto
        date_col: the column to calculate over (usually the 'Close' price)
        adjusted_close: the column with the low price

    Returns:
        the original dataframe with the lower bound appended

    **Example**

    .. code-block:: python

        from wsbtrading import maths
        df_mapped = maths.is_in_squeeze(
            df=df,
            metric_col='Close',
            low_col='Low',
            high_col='High',
            rolling_window=20
        )
    """
    df_price_pivot = df.pivot(index=date_col, columns=stock_ticker_col, values=adjusted_close)
    unique_date = df[date_col].unique()
    # start after a year
    start = 252
    turbulence_index = [0] * start
    # turbulence_index = [0]
    count = 0
    for i in range(start, len(unique_date)):
        current_price = df_price_pivot[df_price_pivot.index == unique_date[i]]
        hist_price = df_price_pivot[[n in unique_date[0:i] for n in df_price_pivot.index]]
        cov_temp = hist_price.cov()
        current_temp = (current_price - np.mean(hist_price, axis=0))
        temp = current_temp.values.dot(np.linalg.inv(cov_temp)).dot(current_temp.values.T)
        if temp > 0:
            count += 1
            if count > 2:
                turbulence_temp = temp[0][0]
            else:
                # avoid large outlier because of the calculation just begins
                turbulence_temp = 0
        else:
            turbulence_temp = 0
        turbulence_index.append(turbulence_temp)

    turbulence_index = pd.DataFrame({'date_col': date_col.index,
                                     'turbulence': turbulence_index})
    return turbulence_index
