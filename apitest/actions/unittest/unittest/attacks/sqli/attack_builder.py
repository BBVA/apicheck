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
