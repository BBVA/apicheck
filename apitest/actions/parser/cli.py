#!/usr/bin/env python3

import click
import logging

from .postman.cli import postman


log = logging.getLogger('apitest')


# --------------------------------------------------------------------------
# CLI APITest
# --------------------------------------------------------------------------
@click.group()
@click.pass_context
def parse(ctx, **kwargs):  # pragma no cover
    ctx.obj.update(kwargs)


parse.add_command(postman)
