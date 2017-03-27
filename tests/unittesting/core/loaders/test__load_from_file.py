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
