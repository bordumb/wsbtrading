"""Functions to aid in quick maths to calculate for ad-hoc analysis and feature engineering."""

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
    check_columns(dataframe=df, required_columns=[numerator_col, denominator_col])

    df['result'] = df[numerator_col] / df[denominator_col]
    return df
