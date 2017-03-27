#!/usr/bin/env python3

import click
import logging

from apitest import global_options

from .model import *
from .console import *
from ...helpers import check_console_input_config


log = logging.getLogger('apitest')


@click.group()
@click.option('-e', '--variable',
              'postman_variables',
              help="setup postman variables", multiple=True)
@click.pass_context
def postman(ctx, **kwargs):  # pragma no cover
    ctx.obj.update(kwargs)


@postman.command(help="Extract information from APITest collection")
@click.argument('file_path', required=True)
@click.pass_obj
def analyze(ctx, **kwargs):
    config = ApitestPostmanAnalyzeModel(**ctx, **kwargs)

    # Check if valid
    if check_console_input_config(config):
        launch_apitest_postman_analyze_in_console(config)


@postman.command(help="Parse Postman collection and export information in "
                      "apitest format")
@click.pass_context
@click.option('-o', '--output',
              'output_file',
              help="output file. This file is in JSON format")
@click.argument('file_path', required=True)
def extract(ctx, **kwargs):
    config = ApitestPostmanParseModel(**ctx, **kwargs)

    if check_console_input_config(config):
        launch_apitest_postman_parse_in_console(ctx.obj)

