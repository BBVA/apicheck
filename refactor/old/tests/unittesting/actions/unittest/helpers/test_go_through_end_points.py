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
import os
import pytest

from os.path import exists, abspath, join

from apitest import APITestEndPoint
from apitest.actions.unittest.helpers import go_through_end_points, make_directoriable


def test_go_through_end_points_runs_invalid_data(tmpdir, apitest_obj):

    with pytest.raises(AssertionError):
        list(go_through_end_points(None))


def test_go_through_end_points_runs_none_basedir(tmpdir, apitest_obj):

    g = go_through_end_points(apitest_obj)

    base_dir = os.getcwd()
    base_path = abspath(join(base_dir, make_directoriable(apitest_obj.title)))

    endpoint_path, _ = list(g)[0]

    assert endpoint_path.startswith(base_path)


def test_go_through_end_points_runs_ok(tmpdir, apitest_obj):
    paths = list(go_through_end_points(apitest_obj, base_dir=str(tmpdir)))

    for endpoint, obj in paths:
        assert isinstance(endpoint, str)
        assert isinstance(obj, APITestEndPoint)


def test_go_through_end_points_check_files_exits(tmpdir, apitest_obj):
    paths = list(go_through_end_points(apitest_obj, base_dir=str(tmpdir)))

    for endpoint, obj in paths:
        assert exists(endpoint) is True


def test_go_through_end_points_already_exits_base_path(tmpdir, apitest_obj):
    go_through_end_points(apitest_obj, base_dir=str(tmpdir))
    go_through_end_points(apitest_obj, base_dir=str(tmpdir))
