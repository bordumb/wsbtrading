"""Functions to aid in quick maths to calculate for ad-hoc analysis and feature engineering."""

from trading import check_columns


def divide_kernel(numerator: float, denominator: float) -> float:
    """Divides one number by another number.

    Args:
        numerator: the number for the top of your fraction
        denominator: the number for the bottom of your fraction

    Returns:
        a float

    **Example**

    .. code-block:: python

        from trading.maths
        maths.divide_kernel(numerator=3, denominator=9)
    """
    if denominator == 0:
        return 0
    return numerator / denominator


def divide(df: 'DataFrame', numerator_col: float, denominator_col: float) -> 'DataFrame':
    """Maps a 0-1 column that indicates which events are an impression for the tab header CTA.

    Args:
        df: the dataframe to append a column onto
        numerator_col: the number for the top of your fraction
        denominator_col: the number for the bottom of your fraction

    Returns:
        the original dataframe with the division result appended

    **Example**

    .. code-block:: python

        from trading import maths
        df_mapped = maths.divide(df=df)
    """
    check_columns(dataframe=df, required_columns=[numerator_col, denominator_col])

    df['result'] = divide_kernel(numerator=numerator_col, denominator=denominator_col)
    return df
