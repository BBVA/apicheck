import yaml
import inspect

from yaml import load

try:
    from yaml import CLoader as Loader, CDumper as Dumper, \
        CSafeLoader as SafeLoader
except ImportError as e:
    from yaml import Loader, Dumper, SafeLoader


def slug(text: str) -> str:
    return text.lower().replace(" ", "-")


def debugging() -> bool:
    for frame in inspect.stack():
        if frame[1].endswith("pydevd.py"):
            return True
    return False


def yaml_loader(content: str) -> dict:
    """This function uses the most efficient method to load a YAML file
    and exclude datetime object to avoid fails in json convertions"""

    # Code taken from: https://stackoverflow.com/a/52312810
    NoDatesSafeLoader = yaml.SafeLoader
    NoDatesSafeLoader.yaml_implicit_resolvers = {
        k: [r for r in v if r[0] != 'tag:yaml.org,2002:timestamp'] for
        k, v in NoDatesSafeLoader.yaml_implicit_resolvers.items()
    }

    return load(content, Loader=NoDatesSafeLoader)
