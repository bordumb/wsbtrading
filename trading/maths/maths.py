"""Functions to aid in quick maths to calculate for ad-hoc analysis and feature engineering."""

from typing import Union, List, Dict, Mapping, Optional, TYPE_CHECKING

from phobos.utils import core


def divide_kernel(numerator: float, denominator: int) -> int:
    """Divides one number by another number.

    Args:
        numerator: the number for the top of your fraction
        denominator: the number for the bottom of your fraction

    Returns:
        a float

    **Example**

    .. code-block:: python

        from trading.maths
        df_mapped = df.withColumn(
            'is_tab_header_cta_impression',
            maths.divide_kernel(
                col('eventType'), col('pageType'), col('impressions')
            )
        )
    """
    cta_impression = iFitness.tab_header_cta['impressions']
    desired_page_types = cta_impression['pageType']
    desired_event_type = cta_impression['eventType']
    desired_impression_type = cta_impression['impressions']['impressionType']

    if impressions is not None and event_type == desired_event_type and page_type in desired_page_types:
        for impression in impressions:
            if 'impressionType' in impression and impression['impressionType'] == desired_impression_type:
                return 1

    return 0