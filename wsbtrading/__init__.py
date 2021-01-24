__version__ = '1.0.0a04'

__doc__ = """wsbtrading is a library that handles data I/O, aggregation, and modeling to facilitate algorithmic trading stategies."""

import logging
import uuid
from typing import List


def load_logging_config():
    logging.basicConfig(format='%(asctime)s - %(name)s - [%(levelname)s] - %(message)s')


def generate_staging_version() -> str:
    return __version__ + '_' + uuid.uuid4().hex[:8]


class MissingColumnError(Exception):
    """Custom error raised when a dataframe is missing a column required for some calculation."""


def check_columns(dataframe: 'DataFrame', required_columns: List[str]):
    """Checks if the dataframe has all the columns.

    Raises:
        MissingColumnError: if any of the required_columns not in the dataframe's schema
    """
    missing_columns = [column for column in required_columns if column not in dataframe.columns.to_series()]
    if missing_columns:
        raise MissingColumnError(f'The dataframe requires the following columns: {required_columns}. '
                                 f'Missing columns are: {missing_columns}.')
