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
import pytest

from os.path import join, exists

from apitest import ApitestNotFoundError
from apitest.actions.unittest.helpers import _make_package


def test__make_package_runs_ok(tmpdir):
    # Create __init__.py
    _make_package(str(tmpdir))

    # Check file __init__.py exits
    assert exists(join(str(tmpdir), "__init__.py")) is True


def test___make_package_runs_none_input():

    with pytest.raises(AssertionError):
        _make_package(None)


def test___make_package_runs_non_exits_path(tmpdir):

    with pytest.raises(ApitestNotFoundError):
        _make_package(join(str(tmpdir), "xxxxxx"))
