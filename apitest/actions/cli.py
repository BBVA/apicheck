import click
import logging

from apitest import global_options

from .parser.cli import parse
from .sendto.cli import sendto
from .unittest.cli import unittest
from .compare.cli import compare

log = logging.getLogger('apitest')


@global_options()
@click.pass_context
def cli(ctx, **kwargs):
    ctx.obj = kwargs


cli.add_command(parse)
cli.add_command(sendto)
cli.add_command(compare)
cli.add_command(unittest)


if __name__ == "__main__" and __package__ is None:  # pragma no cover
    cli()
