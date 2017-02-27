import sys

import pytest
import logging

from os.path import exists, join

from apitest.actions.unittest.unittest.console import launch_apitest_generate_unittest_in_console


def test_launch_apitest_generate_unittest_in_console_runs_ok(apitest_file, tmpdir):
    in_file = apitest_file
    out_dir = str(tmpdir) + "/outdir/"

    # Patching log
    log = logging.getLogger('apitest')
    
    def _exception(msg, *args, exc_info=True, **kwargs):
        pass

    def _console(msg, *args, exc_info=True, **kwargs):
        pass

    log.exception = _exception
    log.console = _console
    
    launch_apitest_generate_unittest_in_console(dict(output_dir=out_dir), **dict(file_path=in_file))
    
    # Check that output dir has "conftest.py" file
    assert exists(join(out_dir, "conftest.py")) is True


def test_launch_apitest_generate_unittest_in_console_shared_none(apitest_file):
    in_file = apitest_file

    with pytest.raises(AssertionError):
        launch_apitest_generate_unittest_in_console(None, **dict(file_path=in_file))
    

def test_launch_apitest_generate_unittest_in_console_runs_missing_file_path(tmpdir):
    out_dir = str(tmpdir) + "/outdir/"
    
    # Patching log
    log = logging.getLogger('apitest')
    _messages = []
    
    def _exception(msg, *args, exc_info=True, **kwargs):
        _messages.append(msg)

    def _console(msg, *args, exc_info=True, **kwargs):
        pass

    log.exception = _exception
    log.console = _console

    launch_apitest_generate_unittest_in_console(dict(output_dir=out_dir))

    assert "[!] Unhandled exception:" in "".join(_messages)
    

def test_launch_apitest_generate_unittest_in_console_invalid_json(tmpdir, apitest_invalid_file):
    out_dir = str(tmpdir) + "/outdir/"
    
    # Patching log
    log = logging.getLogger('apitest')
    _messages = []
    
    def _console(msg, *args, exc_info=True, **kwargs):
        _messages.append(msg)

    log.console = _console

    launch_apitest_generate_unittest_in_console(dict(output_dir=out_dir, file_path=apitest_invalid_file))

    assert "[!] File format are invalid for" in "".join(_messages)
    

def test_launch_apitest_generate_unittest_in_console_invalid_model(apitest_file, tmpdir):
    in_file = apitest_file
    out_dir = str(tmpdir) + "/outdir/"
    
    # Patching log
    log = logging.getLogger('apitest')
    
    _messages = []

    def _critical(msg, *args, exc_info=True, **kwargs):
        _messages.append(msg)

    def _console(msg, *args, exc_info=True, **kwargs):
        pass
    
    log.critical = _critical
    log.console = _console
    
    launch_apitest_generate_unittest_in_console(dict(output_dir=1), **dict(file_path=in_file))
    
    # Check that output dir has "conftest.py" file
    error_trace = "".join(_messages)
    assert "[!]" in error_trace and "property should be" in error_trace
