import os
import logging

from pathlib import Path
from os import mkdir, makedirs
from os.path import join, abspath, dirname

from jinja2 import Template
from typing import Tuple, Iterator

from apitest import APITest, make_directoriable, find_files_by_extension, ApitestNotFoundError, APITestEndPoint

log = logging.getLogger("apitest")


def _make_package(path: str) -> None:
    assert isinstance(path, str)
    
    try:
        Path(join(path, "__init__.py")).touch()
    except FileNotFoundError as e:
        raise ApitestNotFoundError from e


def go_through_end_points(data: APITest, *, base_dir: str = None) -> Iterator[Tuple[str, APITestEndPoint]]:
    """
    Walk through test, create a directory for each one, and yield the base test folder and
    the EndPoint object
    
    >>> parser = APITest()
    >>> paths = go_through_end_points(parser)
    >>> for end_point_path, end_point in paths:
            print(end_point_path, type(end_point))
        
        /home/my_user/postman_project_name/collection_name/end_point_1, <APITestEndPoint>
        /home/my_user/postman_project_name/collection_name/end_point_2, <APITestEndPoint>
        /home/my_user/postman_project_name/collection_name/end_point_3, <APITestEndPoint>
    
    :param data: A APITest instance
    :type data: Postman
    
    :param base_dir: base dir for test
    :type base_dir: str

    :return: yield a tuple as format: (end_point_path, APITestEndPoint)
    :rtype: str, APITestEndPoint
    """
    assert isinstance(data, APITest)
    
    if not base_dir:
        base_dir = os.getcwd()
    
    # Build basename for test
    base_path = abspath(join(base_dir, make_directoriable(data.title)))
    
    # Create base dir
    try:
        makedirs(base_path)
        
        # Create __init__.py file
        _make_package(base_path)
    except OSError as e:
        log.debug(e)
    
    for collection in data.collections:
        collection_path = abspath(join(base_path, make_directoriable(collection.name)))
        try:
            # For each collection create their own directory
            mkdir(collection_path)
            
            # Create __init__.py file
            _make_package(collection_path)
        except OSError as e:
            log.debug(e)
        
        for end_point in collection.end_points:
            end_point_path = abspath(join(collection_path, make_directoriable(end_point.name)))
            
            try:
                # For each end-point create their own directory
                mkdir(end_point_path)
                
                # Create __init__.py file
                _make_package(end_point_path)
            except OSError as e:
                log.debug(e)
            
            yield end_point_path, end_point


class CustomTemplate(object):
    """This class wraps the Jinja2 Template, it aims to autocontent the render method, avoiding
    not return rendered info, instead, the content is stored in the class and can be consulted after
    it was rendered"""
    
    def __init__(self, filename, *, template=None):
        self.template = template
        self.rendered = None
        self.filename = filename
    
    def render(self, **kwargs):
        self.rendered = self.template.render(**kwargs)


class build_templates(object):
    """
    This context manager load and manage the Jinja Templates, wrapping the Template reading, storing and
    adding to the results the shared jinja2 information.
    
    Shared Jinja2 information is a a file, called `shared_fixtures` and is located under: `actions/unittest/attacks/`.
    
    The function also generates the .py ordering the imports located at the top of the jinja2 template files.
    
    This context manager yield a list of templates.
    
    Each iteration of build_templates yields `CustomTemplate` object instance.
    
    >>> with build_templates(templates_dir=templates_dir, output_file=output_file) as templates:
            for template in templates:
                template.render(url=endpoint.request.url)
            
                print(type(template))
    
    <class 'CustomTemplate'>
    <class 'CustomTemplate'>
    
    :param templates_dir: base path for templates
    :type templates_dir: str
    
    :param output_file: results file name
    :type output_file: str
    
    :raise ApitestNotFoundError: if base dir not found
    """
    
    def __init__(self, templates_dir: str = None, output_file: str = None):
        assert output_file is not None
        assert templates_dir is not None
        
        self.imports = dict(start_import=set(), start_from=set())
        self.results = []
        self.output_file = output_file
        self.templates = set(find_files_by_extension(templates_dir))
        
    def __enter__(self):
        # get each template
        for template in self.templates:
            template_file = join(dirname(__file__), template)
            
            # Read the template and build the Jinja2 Template object
            with open(template_file, "r") as template_content:
                custom_template = CustomTemplate(filename=template, template=Template(template_content.read()))

            self.results.append(custom_template)
            
            yield custom_template
                                
    def __exit__(self, exc_type, exc_val, exc_tb):
        shared_fixtures = join(dirname(__file__), "unittest", "attacks", "shared_fixtures.jinja2.py")
    
        # Check if there are content to save
        if not any(True for template in self.results if template.rendered):
            return
        
        with open(shared_fixtures, "r") as f_shared:
            shared = Template(f_shared.read()).render()
            
        # Before write each template, add shared info to each template
        with open(self.output_file, "w") as o:

            # Extract imports from file content
            #
            #   from xxx import yyy
            #
            #   or
            #
            #   import xxxx
            self.__extract_imports(shared)
            
            for template in self.results:
                self.__extract_imports(template.rendered)
            
            for inp in self.imports["start_import"]:
                o.write(inp)
                o.write("\n")
            
            if self.imports["start_from"]:
                o.write("\n")
                for _from in self.imports["start_from"]:
                    o.write(_from)
                    o.write("\n")
            
            # Write now the shared template
            for shared_lines in shared.splitlines():
                if not any(shared_lines.startswith(match) for match in ("from", "import")):
                    o.write(shared_lines)
                    o.write("\n")

            # Write Templates without imports
            for template in self.results:
                
                for line_num, template_line in enumerate(template.rendered.splitlines()):
                    
                    # Find any line that are note an import or from .. import
                    if not any(template_line.startswith(match) for match in ("from", "import")):
                        
                        # Introduce spaces at the beginning of file, if the processed
                        # line is the first. This is because these jinja file without
                        # external imports, haven't the necessary spaces at the beginning
                        if template_line != "" and line_num == 0:
                            o.write("\n" * 2)
                            
                        o.write(template_line)
                        o.write("\n")
            
    def __extract_imports(self, text_content: str):
        if not text_content:
            return
        
        for template_line in text_content.splitlines():
            if template_line.startswith("from"):
                self.imports["start_from"].add(template_line)
            if template_line.startswith("import"):
                self.imports["start_import"].add(template_line)

__all__ = ("go_through_end_points", "CustomTemplate", "build_templates")

