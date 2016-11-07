#!/usr/bin/env python3

import click
import logging

from apitest import global_options

from .parse.console import *
from .analyze.console import *


log = logging.getLogger('apitest')


# --------------------------------------------------------------------------
# CLI APITest
# --------------------------------------------------------------------------
@global_options()
@click.pass_context
def cli_postman(ctx, **kwargs):  # pragma no cover
    ctx.obj = kwargs


@cli_postman.command(help="Extract information from APITest collection")
@click.pass_context
@click.argument('file_path', required=True)
def analyze(ctx, **kwargs):
    launch_apitest_postman_analyze_in_console(ctx.obj, **kwargs)


@cli_postman.command(help="Parse APITest collection and export information in apitest format")
@click.pass_context
@click.option('-o', '--output', 'output_file', help="output file. This file is in JSON format")
@click.argument('file_path', required=True)
def parse(ctx, **kwargs):
    launch_apitest_postman_parse_in_console(ctx.obj, **kwargs)


if __name__ == "__main__" and __package__ is None:  # pragma no cover
    cli_postman()
