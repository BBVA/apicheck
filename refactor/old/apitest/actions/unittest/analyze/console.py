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

try:
    from ujson import load
except ImportError:
    from json import load

from apitest import APITest, display_apitest_object_summary, load_data

from .model import *

log = logging.getLogger('apitest')


def launch_apitest_generate_load_in_console(shared_config, **kwargs):
    """Launch in console mode"""

    # Load confaig
    config = ApitestGenerateLoadModel(**shared_config, **kwargs)

    log.setLevel(config.verbosity)

    # Check if config is valid
    if not config.is_valid:
        log.console("[!] Invalid input configuration ")

        if config.verbosity > 2:
            for prop, msg in config.validation_errors:
                log.console("[!] '%s' property %s" % (prop, msg))
        return

    try:

        loaded_file = load_data(config.file_path)

        if not loaded_file.is_valid:
            log.critical("[!] File format is WRONG")

            for tag, error in loaded_file.validation_errors:
                log.critical("    - {}: {}".format(tag, error))
            return

        # Display a summary of API
        display_apitest_object_summary(loaded_file, display_function=log.console)

    except KeyboardInterrupt:
        log.console("[*] CTRL+C caught. Exiting...")
    except Exception as e:
        log.critical("[!] Unhandled exception: %s" % str(e))

        log.exception("[!] Unhandled exception: %s" % e, stack_info=True)
    finally:
        log.debug("[*] Shutdown...")


__all__ = ("launch_apitest_generate_load_in_console", )
