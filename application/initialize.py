import base64
import logging
import os
import sys
import warnings
from io import StringIO

import kwlog
from devtools import debug

logger = kwlog.logger(__name__)

LOGGER_FORMAT = ' - '.join(
    ['%(asctime)s', '%(process)d', '%(name)s', '%(levelname)s', '%(message)s']
)


def initialize() -> None:
    warnings.filterwarnings('ignore')

    kwlog.EMAIL_LOG_LEVEL = 'info'

    log_level = os.environ.get('LOG_LEVEL', 'INFO')
    logging.basicConfig(format=LOGGER_FORMAT, level=log_level, force=True)

    logger.info(debug.format(os.environ))
