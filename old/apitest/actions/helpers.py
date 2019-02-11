# Copyright 2017 BBVA
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import logging

from ..core.model import SharedConfig


def check_console_input_config(config: SharedConfig,
                               log: logging.Logger = None) -> bool:

    log = log or logging.getLogger(__package__.split(".", maxsplit=1)[0])

    # Check if config is valid
    if not config.is_valid:
        for prop, msg in config.validation_errors:

            log.critical("[!] '%s' property %s" % (prop, msg))
        return False

    return True


__all__ = ("check_console_input_config", )