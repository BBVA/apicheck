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

# --------------------------------------------------------------------------
# Mocking call to the Mongo Database
# --------------------------------------------------------------------------
import motor.motor_asyncio
import apitest.core.loaders

from apitest import ApitestConnectionError
from apitest.core.loaders import _load_from_mongo

async def _do_mongodb_query_new_runs_oks(col, query: dict):
    return [{"hello": "word"}]


async def _do_mongodb_query_new_return_empty_dict(col, query: dict):
    return []


class _A:
    def __init__(self, params=None):
        pass

    def __getitem__(self, item):
        return _A()

motor.motor_asyncio.AsyncIOMotorClient = _A


# --------------------------------------------------------------------------
# Start tests
# --------------------------------------------------------------------------
def test__load_from_mongo_runs_ok():
    apitest.core.loaders._do_mongodb_query = _do_mongodb_query_new_runs_oks

    assert _load_from_mongo("mongodb://127.0.0.1") == {"hello": "word"}


def test__load_from_mongo_runs_with_database():
    apitest.core.loaders._do_mongodb_query = _do_mongodb_query_new_runs_oks

    assert _load_from_mongo("mongodb://127.0.0.1/db") == {"hello": "word"}


def test__load_from_mongo_runs_empty_returns():
    apitest.core.loaders._do_mongodb_query = _do_mongodb_query_new_return_empty_dict

    assert _load_from_mongo("mongodb://127.0.0.1") == {}


def test__load_from_mongo_runs_raises_timeout():

    class _B(_A):
        def __init__(self, params=None):
            super(_B, self).__init__()
            raise ApitestConnectionError("timeout")

    motor.motor_asyncio.AsyncIOMotorClient = _B

    with pytest.raises(ApitestConnectionError):
        _load_from_mongo("mongodb://127.0.0.2")
