import logging

try:
    from ujson import load
except ImportError:
    from json import load

from .api import *
from .model import *

from apitest import APITest, display_apitest_object_summary, load_data

log = logging.getLogger('apitest')


def launch_apitest_sento_proxy_console(shared_config: ApitestSendtoModel, **kwargs):
    """Launch in console mode"""
    
    # Load config
    config = ApitestSendtoModel(**shared_config, **kwargs)
    
    # Check if config is valid
    if not config.is_valid:
        for prop, msg in config.validation_errors:
            log.critical("[!] '%s' property %s" % (prop, msg))
        return
    
    log.setLevel(config.verbosity)
    
    # Build proxy inf
    proxy_info = ProxyConfig(url=config.proxy_url,
                             user=config.proxy_user,
                             password=config.proxy_password)
    
    try:
        log.console("[*] Loading API information...")
        
        # Get and load data
        loaded_file = load_data(config.apitest_file)
        
        if not loaded_file.is_valid:
            log.critical("[!] File format is WRONG")

            for tag, error in loaded_file.validation_errors:
                log.critical("    - {}: {}".format(tag, error))
            return

        # Display a summary of API
        display_apitest_object_summary(loaded_file, display_function=log.console)
        
        # Make the requests
        log.console("[*] Making queries to the endpoints through the proxy: '{}'".format(proxy_info.url))
        
        make_all_requests(proxy=proxy_info, apitest_obj=loaded_file)
    
    except KeyboardInterrupt:
        log.console("[*] CTRL+C caught. Exiting...")
    except Exception as e:
        log.critical("[!] Unhandled exception: %s" % str(e))
        
        log.exception("[!] Unhandled exception: %s" % e, stack_info=True)
    finally:
        log.debug("[*] Shutdown...")


__all__ = ("launch_apitest_sento_proxy_console",)
