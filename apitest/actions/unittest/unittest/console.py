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
