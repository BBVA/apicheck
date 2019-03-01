"""
This file contains python3.6+ syntax!
Feel free to import and use whatever new package you deem necessary.
"""

import logging

from .model import RunningConfig

logger = logging.getLogger("apicheck")


def run(running_config: RunningConfig):
    logger.info(f"Send API '{running_config.api_id}' to proxy")
