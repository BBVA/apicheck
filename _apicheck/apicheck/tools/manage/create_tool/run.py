"""
This file contains python3.6+ syntax!
Feel free to import and use whatever new package you deem necessary.
"""

import os
import shutil
import logging

from slugify import slugify
from pathlib import Path

from .config import RunningConfig

logger = logging.getLogger("apicheck")


# -------------------------------------------------------------------------
# Main saving methods
# -------------------------------------------------------------------------
def run(running_config: RunningConfig):

    slug_name = slugify(running_config.name).replace("-", "_")

    plugin_template = os.path.join(
        os.path.dirname(__file__),
        "plugin_template"
    )
    output_path = os.path.join(
        os.path.abspath(running_config.dest),
        slug_name
    )

    logger.info("Building plugin template")
    shutil.copytree(plugin_template, output_path)

    logger.info("Converting in package")
    Path(os.path.join(output_path, "__ini__.py")).touch()

    logger.info("Configuring plugin name")
    with open(os.path.join(output_path, "cli.py"), "r") as f:
        content = f.read()

    with open(os.path.join(output_path, "cli.py"), "w") as f:
        f.write(content.replace("##PLUGIN_CMD##", slug_name))

