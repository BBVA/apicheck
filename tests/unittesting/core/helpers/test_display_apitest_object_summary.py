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
from apitest.core.helpers import display_apitest_object_summary


def test_display_apitest_object_summary_runs_ok(apitest_obj):

    assert display_apitest_object_summary(apitest_obj) is None


def test_display_apitest_object_summary_custom_function(apitest_obj):

    assert display_apitest_object_summary(apitest_obj, display_function=lambda x: x) is None
