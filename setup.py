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

if sys.version_info < (3, 5, ):
    raise RuntimeError("Apitest requires Python 3.5.0+")

#
# Get version software version
#
version_file = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "apitest")), '__init__.py')
with codecs.open(version_file, 'r', 'latin1') as fp:
    try:
        version = re.findall(r"^__version__ = ['\"]([^']+)['\"]\r?$",
                             fp.read(), re.M)[0]
    except IndexError:
        raise RuntimeError('Unable to determine version.')


with open(join(dirname(__file__), 'requirements.txt')) as f:
    required = f.read().splitlines()

with open(join(dirname(__file__), 'requirements-performance.txt')) as f:
    required_performance = f.read().splitlines()

with open(join(dirname(__file__), 'requirements-runtest.txt')) as f:
    required_test = f.read().splitlines()

with open(join(dirname(__file__), 'README.rst')) as f:
    long_description = f.read()


class PyTest(TestCommand):
    user_options = []

    def run(self):
        import subprocess
        import sys
        errno = subprocess.call([sys.executable,
                                 '-m',
                                 'pytest',
                                 '--cov-report',
                                 'html',
                                 '--cov-report',
                                 'term',
                                 '--cov',
                                 'apitest'])
        raise SystemExit(errno)

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
    extras_require={
        'performance':  required_performance
    },
    entry_points={'console_scripts': [
        'apitest = apitest.actions.cli:cli',
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
    ],
    tests_require=required_test,
    cmdclass=dict(test=PyTest)
)

