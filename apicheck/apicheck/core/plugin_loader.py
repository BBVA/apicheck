import os
import importlib

from typing import Tuple, Callable, Dict

from apicheck.exceptions import APICheckException

MODULES_FN = (
    ("cli", "cli"),
    ("config", "RunningConfig"),
    ("run", "run"),
)


def load_plugins(plugin_type: str) \
        -> APICheckException or Dict[str, Tuple[Callable, Callable, Callable]]:
    """
    This function loads APICheck plugins.

    Return a dict with format

    {
        "PLUGIN_NAME": (cli: function, RunningConfig: function, run: class),
    }

    :param plugin_type: could be "sources" or "actions"

    """

    if plugin_type not in ("actions", "sources"):
        raise APICheckException("Invalid plugin name")

    p_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", plugin_type)
    )

    plugins_load_path = []

    #
    # Locate each plugin dir path
    #
    for root, dirs, files in os.walk(p_path, topdown=False):
        if all(f"{x}.py" in files for x in ("cli", "run", "config")):
            plugins_load_path.append(root.split("/")[-1])

    ret = {}

    for plugin_name in plugins_load_path:
        mod_name = f"apicheck.{plugin_type}.{plugin_name}"

        # The module is loaded but not used due to allow to load dependencies
        # inside the submodules
        importlib.import_module(mod_name)

        plugin_modules = []
        for module, fn in MODULES_FN:
            h = importlib.import_module(f"{mod_name}.{module}")

            plugin_modules.append(getattr(h, fn))

        ret[plugin_name] = plugin_modules

    return ret
