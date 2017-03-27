# import logging
#
# from apitest import PostmanConfig
#
# from .api import *
# from .model import *
#
# log = logging.getLogger('apitest')
#
#
# def launch_apitest_postman_parse_in_console(shared_config: ApitestPostmanParseModel, **kwargs):
#     """Launch in console mode"""
#
#     # Load config
#     config = ApitestPostmanParseModel(**shared_config, **kwargs)
#
#     # Check if config is valid
#     if not config.is_valid:
#         for prop, msg in config.validation_errors:
#             log.critical("[!] '%s' property %s" % (prop, msg))
#         return
#
#     log.setLevel(config.verbosity)
#
#     try:
#         log.console("[*] Analyzing parser file: '%s'" % config.file_path)
#
#         # Build postman config
#         postman_config = PostmanConfig(variables=config.postman_variables)
#
#         loaded_file = parse_postman_file(config.file_path, postman_config)
#
#         if loaded_file.is_valid:
#             log.console("[*] File format is OKs")
#             log.console("[*] Exporting to: '{}'".format(config.output_file))
#
#             with open(config.output_file, "w") as f:
#                 f.write(loaded_file.to_json())
#
#         else:
#             log.console("[!] File format is WRONG")
#
#             for tag, error in loaded_file.validation_errors:
#                 log.console("    - {}: {}".format(tag, error))
#
#     except KeyboardInterrupt:
#         log.console("[*] CTRL+C caught. Exiting...")
#     except Exception as e:
#         log.critical("[!] Unhandled exception: %s" % str(e))
#
#         log.exception("[!] Unhandled exception: %s" % e, stack_info=True)
#     finally:
#         log.debug("[*] Shutdown...")
#
#
# __all__ = ("launch_apitest_postman_parse_in_console", )
