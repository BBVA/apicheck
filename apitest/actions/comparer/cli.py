#!/usr/bin/env python3

import click
import logging

from apitest import global_options

from .console import *

log = logging.getLogger('apitest')


# --------------------------------------------------------------------------
# CLI APITest
# --------------------------------------------------------------------------
@global_options()
@click.pass_context
def cli(ctx, **kwargs):  # pragma no cover
    ctx.obj = kwargs


@cli.command(help="Compare two APIs")
@click.pass_context
@click.argument('api_old_connection_string', required=True)
@click.argument('api_current_connection_string', required=True)
def compare(ctx, **kwargs):
    launch_apitest_comparer_console(ctx.obj, **kwargs)


if __name__ == "__main__" and __package__ is None:  # pragma no cover
    cli()
