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

from click.testing import CliRunner

from apitest.actions.cli import cli

import apitest.actions.compare.console


def _launch_apitest_comparer_console(blah, **kwargs):
    click.echo("ok")


def test_cli_compare_runs_show_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["compare"])

    assert 'compare [OPTIONS] API_OLD_CONNECTION_STRING\n                   API_CURRENT_CONNECTION_STRING'\
           in result.output
    assert 'Usage:' in result.output


def test_cli_compare_runs_ok():
    # Patch the launch of: launch_apitest_generate_load_in_console
    apitest.actions.compare.cli.launch_apitest_comparer_console = _launch_apitest_comparer_console

    runner = CliRunner()
    result = runner.invoke(cli, ["compare", "old_connection_string", "new_connection_string"])

    assert 'ok' in result.output
