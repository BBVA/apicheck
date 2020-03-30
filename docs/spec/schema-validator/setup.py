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

HERE = os.path.abspath(os.path.dirname(__file__))


if sys.version_info < (3, 7,):
    raise RuntimeError("Sendtoproxy requires Python 3.7.0+")

with open(os.path.join(HERE, "requirements.txt"), "r") as f:
    REQUIREMENTS = f.read().splitlines()

VERSION = "1.0.0"

setup(
    name='apicheck-schema-validator',
    version=VERSION,
    install_requires=REQUIREMENTS,
    include_package_data=True,
    url='https://github.com/bbva/apicheck',
    license='MIT',
    author='BBVA-Labs Team',
    packages=find_packages(),
    entry_points={
        'console_scripts': {
            "ac-scheme-validator = apicheck_schema_validator.schema_validator:main",
            "ac-sv = apicheck_schema_validator.schema_validator:main"
        }
    },
    description='Read request from stdin and send it to proxy',
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
