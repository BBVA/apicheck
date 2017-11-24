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
from apitest.core.helpers import form_content2dict


def test_form_content2dict_runs_ok():
    assert form_content2dict("user=john&password=1234") == {"user": "john", "password": "1234"}


def test_form_content2dict_runs_null_input():
    assert form_content2dict(None) == dict(form_data="")


def test_form_content2dict_runs_invalid_input():
    assert form_content2dict("aaaaa") == dict(form_data="aaaaa")
