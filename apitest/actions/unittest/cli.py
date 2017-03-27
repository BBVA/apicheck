#!/usr/bin/env python3

import click
import logging

from apitest import global_options

from .analyze.console import *
from .unittest.console import *


log = logging.getLogger('apitest')


@click.group()
@click.pass_context
def unittest(ctx, **kwargs):  # pragma no cover
    ctx.obj.update(kwargs)


@unittest.command(help="Load an ApiTest file and display a summary")
@click.pass_context
@click.argument('file_path', required=True)
def analyze(ctx, **kwargs):
    launch_apitest_generate_load_in_console(ctx.obj, **kwargs)


@unittest.command(help="Build unittest-like for testing the API")
@click.pass_context
@click.option('-o', '--output-dir', 'output_dir', required=True)
@click.argument('file_path', required=True)
def generate(ctx, **kwargs):
    launch_apitest_generate_unittest_in_console(ctx.obj, **kwargs)
