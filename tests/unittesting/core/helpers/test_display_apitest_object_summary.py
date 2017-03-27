from apitest.core.helpers import display_apitest_object_summary


def test_display_apitest_object_summary_runs_ok(apitest_obj):
    
    assert display_apitest_object_summary(apitest_obj) is None


def test_display_apitest_object_summary_custom_function(apitest_obj):
    
    assert display_apitest_object_summary(apitest_obj, display_function=lambda x: x) is None
