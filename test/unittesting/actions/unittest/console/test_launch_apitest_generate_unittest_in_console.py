import sys

import pytest
import logging

from os.path import exists, join

from apitest.actions.unittest.unittest.model import ApitestGenerateUnitTestModel
from apitest.actions.unittest.unittest.console import launch_apitest_generate_unittest_in_console


def test_launch_apitest_generate_unittest_in_console_runs_ok(apitest_file, tmpdir):
    in_file = apitest_file
    out_dir = str(tmpdir) + "/outdir/"
    
    launch_apitest_generate_unittest_in_console(dict(output_dir=out_dir), **dict(file_path=in_file))
    
    # Check that output dir has "conftest.py" file
    assert exists(join(out_dir, "conftest.py")) is True


def test_launch_apitest_generate_unittest_in_console_shared_none(apitest_file):
    in_file = apitest_file

    with pytest.raises(AssertionError):
        launch_apitest_generate_unittest_in_console(None, **dict(file_path=in_file))
    

def test_launch_apitest_generate_unittest_in_console_runs_missing_file_path(tmpdir):
    # sys.stderr = open(str(tmpdir) + "/aaa.out", "w")
    # sys.stdout = open(str(tmpdir) + "/aaaa.out", "w")
    out_dir = str(tmpdir) + "/outdir/"

    with pytest.raises(AssertionError):
        launch_apitest_generate_unittest_in_console(dict(output_dir=out_dir))

        with open(str(tmpdir) + "/aaaa.out", "r") as rr:
            print(rr.read())
