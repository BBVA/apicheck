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

from .proxy.console import *

log = logging.getLogger('apitest')


# --------------------------------------------------------------------------
# CLI APITest
# --------------------------------------------------------------------------
@click.group()
@click.pass_context
def sendto(ctx, **kwargs):  # pragma no cover
    ctx.obj.update(kwargs)


@sendto.command(help="Send API end-point queries thought a proxy")
@click.pass_context
@click.option('-P', '--proxy', "proxy_url", required=True, default="http://127.0.0.1:8080")
@click.argument('apitest_file', required=True)
def proxy(ctx, **kwargs):
    launch_apitest_sento_proxy_console(ctx.obj, **kwargs)
