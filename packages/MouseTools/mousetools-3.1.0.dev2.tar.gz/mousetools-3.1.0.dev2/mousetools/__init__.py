import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

__version__ = "3.1.0-dev.2"  # will be set at runtime
logger.info(f"MouseTools version: {__version__}")
