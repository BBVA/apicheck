import pytest

from os.path import join

from apitest import ApitestNotFoundError
from apitest.actions.unittest.helpers import build_templates, CustomTemplate


@pytest.fixture
def test_path(tmpdir):
    for x in ('xx1.jinja2.py', 'xx1.jinja2.py', 'xx1.txt'):
        open(join(str(tmpdir), x), "w").write("xxx")
    
    return str(tmpdir)


@pytest.fixture
def built_jinja_templates(tmpdir):
    
    with open(str(tmpdir) + "/case_01.jinja2.py", "w") as c01:
        c01.write("""import re
        
def test_sqli_case_001(make_requests):
    current, good, bad = make_requests("{{ url }}")

    assert bad.status_code == current.status_code
    assert bad.body == current.body
""")
    
    with open(str(tmpdir) + "/case_02.jinja2.py", "w") as c02:
        c02.write("""from apitest.helpers.fuzzer import build_fuzzed_method
        
def test_sqli_case_001(make_requests):
    current, good, bad = make_requests("{{ url }}")

    assert bad.status_code == current.status_code
    assert bad.body == current.body
""")
    
    with open(str(tmpdir) + "/empty.jinja2.py", "w") as c03:
        c03.write("")

    return str(tmpdir)


@pytest.fixture
def fixtures_with_spaces(tmpdir):

    with open(str(tmpdir) + "/case_03.jinja2.py", "w") as f:
        f.write("""def test_sqli_case_001(make_requests):
        current, good, bad = make_requests("{{ url }}")

        assert bad.status_code == current.status_code
        assert bad.body == current.body
    """)
    
    return str(tmpdir)


# --------------------------------------------------------------------------
# Constructor
# --------------------------------------------------------------------------
def test_build_templates_constructor_ok():
    r = build_templates("/tmp", "blah")
    assert r is not None


def test_build_templates_constructor_none_templates_dir():
    
    with pytest.raises(AssertionError):
        build_templates(None, "blah")


def test_build_templates_constructor_none_output_file_dir():
    
    with pytest.raises(AssertionError):
        build_templates("/tmp", None)


def test_build_templates_constructor_templates_dir_not_found():
    
    with pytest.raises(ApitestNotFoundError):
        build_templates("/asdfasfasdfsa", "as")


# --------------------------------------------------------------------------
# __enter__ method
# --------------------------------------------------------------------------
def test___enter___instance_ok(test_path):
    
    with build_templates(test_path, "") as templates:
        for template in templates:
            assert isinstance(template, CustomTemplate)


# --------------------------------------------------------------------------
# __exit__ method
# --------------------------------------------------------------------------
def test__exit__empty_templates(tmpdir):
    
    output_file = str(tmpdir) + "/output"
    bt = build_templates(str(tmpdir), output_file)
    
    with bt as _:
        pass
    
    assert len(bt.results) == 0


def test___exit__built_templates_oks(built_jinja_templates):
    output_file = built_jinja_templates + "/output"
    
    bt = build_templates(built_jinja_templates, output_file)
    
    with bt as templates:
        for template in templates:
            template.render()


def test___exit__built_templates_template_with_non_imports(fixtures_with_spaces):
    output_file = fixtures_with_spaces + "/output"
    
    bt = build_templates(fixtures_with_spaces, output_file)
    
    with bt as templates:
        for template in templates:
            template.render()
