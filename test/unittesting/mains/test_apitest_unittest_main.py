# import sys
# import pytest
#
# from apitest.apitest_unittest import main
#
#
# def test_apitest_unittest_main_runs_ok():
#     # This test checks that the main command line run well
#
#     sys.argv = [sys.argv[0], "-h"]
#
#     with pytest.raises(SystemExit) as e:
#         main()
#
#     assert str(e.value) == '0'
