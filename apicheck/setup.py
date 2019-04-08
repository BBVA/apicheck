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

import sys

from setuptools import setup, find_packages

if sys.version_info < (3, 7,):
    raise RuntimeError("APICheck requires Python 3.7.0+")

VERSION = "1.0.0"

setup(
    name='apicheck',
    version=VERSION,
    install_requires=[
        "aiohttp",
        "mitmproxy",
        'sqlalchemy',
        "sqlalchemy-aio",
        "terminaltables"
    ],
    extras_require={
        'mysql': ['pg8000'],
        'postgres': ['PyMySQL'],
    },
    url='https://github.com/bbva/apicheck',
    license='MIT',
    author='BBVA-Labs Team',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            # Importers. Long name and alias
            'apicheck-importer = apicheck.cli.importers:cli',
            'aci = apicheck.cli.importers:cli',

            # Actions. Long name and alias
            'apicheck-actions = apicheck.cli.actions:cli',
            'aca = apicheck.cli.actions:cli',

            # manage. Long name and alias
            'apicheck-manage = apicheck.cli.manage:cli',
            'acm = apicheck.cli.manage:cli',
        ],
    },
    description='Testing your API for security',
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Topic :: Security',
    ]
)
