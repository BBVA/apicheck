# import logging
#
# try:
#     from ujson import load
# except ImportError:
#     from json import load
#
# from .model import *
# from ...helpers import *
#
# from apitest import postman_parser
#
# log = logging.getLogger('apitest')
#
#
# def launch_apitest_postman_analyze_in_console(shared_config: ApitestPostmanAnalyzeModel, **kwargs):
#     """Launch in console mode"""
#
#     # Load config
#     config = ApitestPostmanAnalyzeModel(**shared_config, **kwargs)
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
#         # Get and load data
#         with open(config.file_path, "r") as f:
#             json_info = load(f)
#
#             loaded_file = postman_parser(json_info)
#
#         if loaded_file.is_valid:
#             log.console("[*] File format is OKs")
#             log.console("[*] Summary:")
#             log.console("    - Total collections: %s" % len(loaded_file.collections))
#             log.console("    - Total end-points: %s" % sum(len(x.end_points) for x in loaded_file.collections))
#
#             if config.verbosity >= 2:
#                 for col in loaded_file.collections:
#                     log.console("      > {name:{align}} - {endpoint:>5} endpoints".format(name=col.name,
#                                                                                           align=20,
#                                                                                           endpoint=len(col.end_points)))
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
# __all__ = ("launch_apitest_postman_analyze_in_console",)
