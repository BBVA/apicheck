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
except ImportError:  # pragma no cover
    from json import load

from apitest import load_data

from .model import *
from .api import *

log = logging.getLogger('apitest')


def launch_apitest_generate_unittest_in_console(shared_config, **kwargs):
    """Launch in console mode"""
    assert isinstance(shared_config, dict)

    # Load confaig
    config = ApitestGenerateUnitTestModel(**shared_config, **kwargs)

    log.setLevel(config.verbosity)

    # Check if config is valid
    if not config.is_valid:
        for prop, msg in config.validation_errors:
            log.critical("[!] '%s' property %s" % (prop, msg))
        return

    try:
        parser_data = load_data(config.file_path)

        if not parser_data.is_valid:
            log.console("[!] File format are invalid for '{}'".format(config.file_path))

        build_unittest(config, parser_data)

    except KeyboardInterrupt:  # pragma no cover
        log.console("[*] CTRL+C caught. Exiting...")
    except Exception as e:
        log.console("[!] Unhandled exception: %s" % str(e))

        log.exception("[!] Unhandled exception: %s" % e, stack_info=True)
    finally:
        log.debug("[*] Shutdown...")


__all__ = ("launch_apitest_generate_unittest_in_console", )
