# Copyright 2017 BBVA
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
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
