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

