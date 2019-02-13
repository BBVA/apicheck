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
import shutil
import logging

from os.path import dirname, join, abspath

from apitest import APITest

from .attacks import ATTACKS_TEST
from ..helpers import go_through_end_points
from .model import ApitestGenerateUnitTestModel

log = logging.getLogger("apitest")


def build_unittest(config: ApitestGenerateUnitTestModel, data: APITest):
    """
    Build unittest-like cases

    :param config: configuration instance
    :type config: ApitestGenerateUnitTestModel

    :param data: Postman object instance
    :type data: APITest

    """
    assert isinstance(config, ApitestGenerateUnitTestModel)

    for end_point_path, endpoint in go_through_end_points(data, base_dir=config.output_dir):
        log.console("[*] Generating tests for end-point: {}".format(endpoint.name))

        # Build test for each type of attack
        for attack, attack_builder in ATTACKS_TEST.items():
            log.console("    > Building attacks tests: '{}'".format(attack))

            attack_builder(end_point_path, endpoint)

    # Copy py.test fixtures
    pytest_src = join(abspath(dirname(__file__)), "attacks", "_conftest.py")
    pytest_dst = join(abspath(dirname(config.output_dir)), "conftest.py")

    shutil.copy(pytest_src, pytest_dst)

__all__ = ("build_unittest", )
