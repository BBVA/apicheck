from urllib.parse import urlparse, urljoin
from os.path import join, dirname, abspath, basename

from jinja2 import Template

from apitest import APITestEndPoint, make_directoriable, form_content2dict, APITestContentType

from ....helpers import build_templates


#
# Render body parameters
#
def _render_body_params(endpoint: APITestEndPoint, template: Template, payload_content: dict):
    """
    Generates tests for requests with information in body content like:
    
        GET / HTTP/1.1
        Host: mysite.com
        
        user=guest&password=1234
    
    This function will test params:
    - user
    - password
    
    """
    content_type = endpoint.request.body.content_type
    body = {}
    if endpoint.request.body.content_type:
        if content_type == APITestContentType.form:
            body = form_content2dict(endpoint.request.body.value)

    if not body:

        template.render(url=endpoint.request.url,
                        method=endpoint.request.method,
                        content_type=content_type,
                        body_content=body,
                        payloads=payload_content)


#
# Render URL parameters
#
def _render_url_params(endpoint: APITestEndPoint, template: Template, payload_content: dict):
    """
    Generates tests for parameters with information in URL, like:
    
        wwww.mysite.com/index.php?id=1&page=abc
    
    This function will generate tests for params:
    - id
    - page
    """
    content_type = APITestContentType(endpoint.request.body.content_type).value
    url = endpoint.request.url
    
    scheme, netloc, url, params, query, fragment = urlparse(url)
    
    base_url = urljoin("%s://%s" % (scheme, netloc), url)
    url_params = form_content2dict(query) if len(query) != 0 else {}
    
    template.render(url=base_url,
                    method=endpoint.request.method,
                    content_type=content_type,
                    body_content=endpoint.request.body.value,
                    url_params=url_params,
                    payloads=payload_content)


RENDERS = {
    'xss_body': _render_body_params,
    'xss_url': _render_url_params
}


def xss_builder(output_test_dir: str, endpoint: APITestEndPoint):
    output_file = join(output_test_dir, "test_xss_methods_{}.py".format(make_directoriable(endpoint.name)))
    templates_dir = abspath(dirname(__file__))
    payload_file = abspath(join(dirname(__file__), "xss.txt"))
    
    # Load payloads
    with build_templates(templates_dir=templates_dir,
                         output_file=output_file) as templates:
        
        # Load local XSS attacks
        with open(payload_file, "r") as f:
            payload_content = f.readlines()

        for template in templates:
            template_name, _ = basename(template.filename).split(".", maxsplit=1)
            
            # Render
            RENDERS[template_name](endpoint, template, payload_content)


__all__ = ("xss_builder",)
