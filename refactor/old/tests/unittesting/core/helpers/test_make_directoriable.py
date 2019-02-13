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
from apitest.core.helpers import make_directoriable


def test_make_directoriable_ok_case():
    assert make_directoriable("Hello World guy!") == "hello_world_guy"


def test_make_directoriable_underline():
    assert make_directoriable("Hello-World-guy!") == "hello_world_guy"


def test_make_directoriable_bad_input():
    assert make_directoriable(None) == ""
