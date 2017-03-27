import logging

try:
    from ujson import load
except ImportError:
    from json import load

from .model import *
from .helpers import *

from apitest import APITest, display_apitest_object_summary, load_data

log = logging.getLogger('apitest')


def launch_apitest_comparer_console(shared_config: ApitestComparerModel, **kwargs):
    """Launch in console mode"""

    # Load config
    config = ApitestComparerModel(**shared_config, **kwargs)

    # Check if config is valid
    if not config.is_valid:
        for prop, msg in config.validation_errors:
            log.critical("[!] '%s' property %s" % (prop, msg))
        return

    log.setLevel(config.verbosity)

    try:
        log.console("[*] Loading API information...")

        loaded_file = load_data(config.api_prev_file)
        old_info = load_data(config.api_current_file)

        if not loaded_file.is_valid:
            log.critical("[!] File format is WRONG")
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


__all__ = ("launch_apitest_comparer_console",)
