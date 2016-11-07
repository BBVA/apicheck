#!/usr/bin/env python3

import click
import logging

from apitest import global_options

from .proxy.console import *

log = logging.getLogger('apitest')


# --------------------------------------------------------------------------
# CLI APITest
# --------------------------------------------------------------------------
@global_options()
@click.pass_context
def cli(ctx, **kwargs):  # pragma no cover
    ctx.obj = kwargs


@cli.command(help="Send API end-point queries thought a proxy")
@click.pass_context
@click.option('-P', '--proxy', "proxy_url", required=True, default="http://127.0.0.1:8080")
@click.argument('apitest_file', required=True)
def proxy(ctx, **kwargs):
    launch_apitest_sento_proxy_console(ctx.obj, **kwargs)


if __name__ == "__main__" and __package__ is None:  # pragma no cover
    cli()
