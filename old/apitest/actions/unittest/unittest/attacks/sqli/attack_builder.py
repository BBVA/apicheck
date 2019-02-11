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
from os.path import join, dirname, abspath

from apitest import APITestEndPoint, make_directoriable

from ....helpers import build_templates


def sqli_builder(output_test_dir: str, endpoint: APITestEndPoint):
    output_file = join(output_test_dir, "test_sqli_{}.py".format(make_directoriable(endpoint.name)))
    templates_dir = abspath(dirname(__file__))

    with build_templates(templates_dir=templates_dir,
                         output_file=output_file) as templates:
        for template in templates:
            template.render(url=endpoint.request.url,
                            method=endpoint.request.method)

__all__ = ("sqli_builder",)
