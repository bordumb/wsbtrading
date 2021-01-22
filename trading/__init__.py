__version__ = '1.0.0a55'

__doc__ = """``Trading`` is a module with functions for data I/O, aggregation, modeling, and placing trades online"""

import logging
import uuid

def load_logging_config():
    logging.basicConfig(format='%(asctime)s - %(name)s - [%(levelname)s] - %(message)s')


def generate_staging_version() -> str:
    return __version__ + '_' + uuid.uuid4().hex[:8]
