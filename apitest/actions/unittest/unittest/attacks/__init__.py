from .xss import *
from .sqli import *
from .http_methods import http_method_builder

ATTACKS_TEST = dict(
    xss=xss_builder,
    sql_injection=sqli_builder,
    http_methods=http_method_builder
)
