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

from apitest.core.shared_cmd_options import global_options


def test_global_options_runs_ok():

    c = global_options()

    assert callable(c.__call__(lambda x: x)) is True


def test_global_options_check_input_params():

    with pytest.raises(AssertionError):
        global_options(None)
