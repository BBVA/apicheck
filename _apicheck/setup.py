# Copyright 2019 BBVA
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

import os
import sys

from setuptools import setup, find_packages

apicheck_home = os.path.join(os.path.dirname(__file__), "apicheck")


def find_tools() -> list:
    """
    This function finds apicheck cli tools to build the cli entry-points
    """

    tools_base_path = os.path.join(apicheck_home, "tools")

    entry_points = []

    for tool_dir in os.listdir(tools_base_path):

        if tool_dir.startswith("_"):
            continue

        tool_cmd = tool_dir.replace("_", "")

        entry_points.append(
            f"at-{tool_cmd} = apicheck.tools.{tool_dir}.cli:cli"
        )

    return entry_points


def find_commands() -> list:
    """
    This function finds apicheck cli commands to build the cli entry-points
    """

    commands_base_path = os.path.join(apicheck_home, "commands")

    entry_points = []

    for command in os.listdir(commands_base_path):
        if command.startswith("_"):
            continue

        command_file, _ = os.path.splitext(command)

        command_name = command_file.replace("_", "")

        entry_points.append(
            f"ac-{command_name} = apicheck.commands.{command_file}:main"
        )

    return entry_points


if sys.version_info < (3, 7,):
    raise RuntimeError("APIChdeck requires Python 3.7.0+")

with open("requirements.txt", "r") as f:
    REQUIREMENTS = f.read().splitlines()

VERSION = "1.0.0"

ENTRY_POINTS = []
ENTRY_POINTS.extend(find_tools())
ENTRY_POINTS.extend(find_commands())

setup(
    name='apicheck',
    version=VERSION,
    install_requires=REQUIREMENTS,
    extras_require={
        'mysql': ['PyMySQL'],
    },
    url='https://github.com/bbva/apicheck',
    license='MIT',
    author='BBVA-Labs Team',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': ENTRY_POINTS
    },
    description='The DevSecOps toolset for REST APIs',
    classifiers=[
        'Topic :: Security',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Other Audience',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.7'
    ]
)
