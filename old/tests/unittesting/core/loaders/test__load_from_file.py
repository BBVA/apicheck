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
import json
import pytest

from apitest.core.loaders import _load_from_file


@pytest.fixture
def build_temp_file(apitest_json):
    def _temp_file(path):
        with open(path, "w") as f:
            f.write(json.dumps(apitest_json))
    return _temp_file


def test__load_from_file_runs_ok():
    with pytest.raises(AssertionError):
        _load_from_file(None)


def test__load_from_file_runs_from_file_uri(tmpdir, build_temp_file, apitest_json):
    file_path = os.path.join(str(tmpdir), os.path.basename("file://asdf.json"))

    # create the file first
    build_temp_file(file_path)

    assert _load_from_file(file_path) == apitest_json
