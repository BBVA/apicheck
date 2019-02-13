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

from .console import *

log = logging.getLogger('apitest')


# --------------------------------------------------------------------------
# CLI APITest
# --------------------------------------------------------------------------
@click.group()
@click.pass_context
def compare(ctx, **kwargs):  # pragma no cover
    ctx.obj.update(kwargs)


@compare.command(help="Compare two APIs")
@click.pass_context
@click.argument('api_old_connection_string', required=True)
@click.argument('api_current_connection_string', required=True)
def compare(ctx, **kwargs):
    launch_apitest_comparer_console(ctx.obj, **kwargs)


__all__ = ("compare", )
