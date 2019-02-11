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
