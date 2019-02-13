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

import re
import os
import sys
import codecs

from os.path import dirname, join

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

if sys.version_info < (3, 6,):
    raise RuntimeError("Apitest requires Python 3.6.0+")

with open(join(dirname(__file__), 'requirements.txt')) as f:
    required = f.read().splitlines()

with open(join(dirname(__file__), 'README.rst')) as f:
    long_description = f.read()

with open(join(dirname(__file__), 'VERSION')) as f:
    version = f.read()

setup(
    name='apitest',
    version=version,
    install_requires=required,
    url='https://github.com/cr0hn/apitest',
    license='MIT',
    author='cr0hn (@ggdaniel)',
    author_email='cr0hn@cr0hn.com',
    packages=find_packages(),
    include_package_data=True,
    entry_points={'console_scripts': [
        'apitest-importer = apitest.cli.importer:cli',
    ]},
    description='Testing your API for security',
    long_description=long_description,
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.5',
        'Topic :: Security',
    ]
)
