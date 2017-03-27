import logging

try:
    from ujson import load
except ImportError:
    from json import load

from apitest import get_log_level, run_in_console

from .api import *
from .model import *
from .parsers import PostmanConfig, postman_parser

log = logging.getLogger('apitest')


def launch_apitest_postman_analyze_in_console(
        config: ApitestPostmanAnalyzeModel):
    log.setLevel(get_log_level(config.verbosity))

    with run_in_console(config.debug):

        log.console("[*] Analyzing parser file: '%s'" % config.file_path)

        # Get and load data
        with open(config.file_path, "r") as f:
            json_info = load(f)

            parsed_env_vars = {}
            if config.postman_variables:
                for var in config.postman_variables:
                    parsed_env_vars.update(dict([var.split("=")]))

            loaded_file = postman_parser(json_info,
                                         parsed_env_vars)

        if loaded_file.is_valid:
            log.console("[*] File format is OKs")
            log.console("[*] Summary:")
            log.console(
                "    - Total collections: %s" % len(loaded_file.collections))
            log.console("    - Total end-points: %s" % sum(
                len(x.end_points) for x in loaded_file.collections))

            if config.verbosity >= 2:
                for col in loaded_file.collections:
                    log.console("> {name:{align}} - {endpoint:>5} "
                                "endpoints".format(
                                    name=col.name,
                                    align=20,
                                    endpoint=len(col.end_points)))
        else:
            log.console("[!] File format is WRONG")

            for tag, error in loaded_file.validation_errors:
                log.console("    - {}: {}".format(tag, error))


def launch_apitest_postman_parse_in_console(
        config: ApitestPostmanParseModel):
    log.setLevel(get_log_level(config.verbosity))

    with run_in_console(config.debug):

        log.console("[*] Analyzing parser file: '%s'" % config.file_path)

        loaded_file = parse_postman_file(config.file_path,
                                         config.postman_variables)

        if loaded_file.is_valid:
            log.console("[*] File format is OKs")
            log.console("[*] Exporting to: '{}'".format(config.output_file))

            with open(config.output_file, "w") as f:
                f.write(loaded_file.to_json())

        else:
            log.console("[!] File format is WRONG")

            for tag, error in loaded_file.validation_errors:
                log.console("    - {}: {}".format(tag, error))


__all__ = ("launch_apitest_postman_analyze_in_console",
           "launch_apitest_postman_parse_in_console")
