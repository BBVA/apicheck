import os
import re
import json
import hashlib
import argparse
import stat
import subprocess
import urllib.request

from pathlib import Path
from collections import defaultdict

# -------------------------------------------------------------------------
# Alias management
# -------------------------------------------------------------------------
from typing import List, Tuple, Set

RC_FILES = {
    "bash": ".bashrc",
    "zsh": ".zshrc"
}

REMOTE_BASE = "https://bbva.github.io/apicheck/assets"
CATALOG_REMOTE_FILE = f"{REMOTE_BASE}/catalog.json"
CATALOG_CHECK_SUM = f"{REMOTE_BASE}/catalog.json.checksum"


def _get_version() -> str:
    here = os.path.dirname(__file__)
    init_file = os.path.join(here, "__init__.py")
    with open(init_file, "r") as f:
        content = f.read()

    return re.match(r'(__version__)([\s]+=[\s]+)(\")([\.\d]+)(\")',
                    content).group(4)


class CatalogCheckSumError(Exception):
    pass


def check_apicheck_is_in_path() -> bool:
    shell_name = Path(os.environ.get("SHELL", "/bin/bash")).name

    try:
        rc_file = RC_FILES[shell_name]
    except KeyError:
        rc_file = RC_FILES["bash"]

    with open(Path().home().joinpath(rc_file), "r") as rc:
        content = rc.read()

        if "/.apicheck_manager/bin" not in content:
            return rc_file
        else:
            return None


def add_new_alias(rc_file: str, alias: str):
    if not alias.startswith("alias"):
        alias = f"alias {alias}"

    bashrc_path = Path(rc_file)
    bashrc_text = bashrc_path.read_text()
    if alias not in bashrc_text:

        if not bashrc_text.endswith("\n"):
            bashrc_text += "\n"

        bashrc_path.write_text(f'{bashrc_text}{alias}\n')


def rm_new_alias(rc_file: str, alias: str):
    if not alias.startswith("unalias"):
        alias = f"unalias {alias}"

    bashrc_path = Path(rc_file)
    bashrc_text = bashrc_path.read_text()
    if alias not in bashrc_text:

        if not bashrc_text.endswith("\n"):
            bashrc_text += "\n"

        bashrc_path.write_text(f'{bashrc_text}{alias}\n')


def create_alias():
    # Detect shell and get RC file
    rc_file = get_current_rc_file()
    add_new_alias(rc_file, 'ls="ls -a"')


def get_catalog() -> List[dict] or CatalogCheckSumError:
    # Fetch remote catalog
    with urllib.request.urlopen(CATALOG_REMOTE_FILE) as catalog, \
            urllib.request.urlopen(CATALOG_CHECK_SUM) as check_sum:
        raw_content = catalog.read()
        remote_catalog_check_sum = check_sum.read()
        if type(remote_catalog_check_sum) is bytes:
            remote_catalog_check_sum = remote_catalog_check_sum.decode("UTF-8")

        h = hashlib.sha512()
        h.update(raw_content)
        check_sum = h.hexdigest()

        if check_sum != remote_catalog_check_sum:
            raise CatalogCheckSumError("Wrong remote catalog checksum")

        return json.loads(raw_content)


def search_in_catalog(catalog: List[dict], tool_name: str) -> dict:
    # Find tool
    tool = None
    for cat in catalog:
        if cat["name"] == tool_name:
            return cat
    else:
        return {}


def print_table(content: List[Tuple[str, str]],
                head: tuple = None,
                width: int = 60):
    def border():
        # print("+", "-" * width, "+")
        print(f"+{'-' * width}+")

    max_key_len = max(len(x[0]) for x in content)

    if head:
        if len(head[0]) > max_key_len:
            max_key_len = len(head[0])

        border()
        if len(head) == 2:
            print(f"| {head[0]}", end="")
            print(f"{' ' * (max_key_len - len(head[0]))}", end="")
            print(" | ", end="")
            print(f"{head[1]}", end="")
            print(
                f"{' ' * (width - (max_key_len + len(head[1]) + 5))}",
                end="")
            print(" |")
        else:
            print(f"| {head[0]}{' ' * (width - len(head[0]) - 1)}|")

    border()

    for cat in content:
        print("| ", end="")
        print(f"{cat[0]}", end="")
        print(f"{' ' * (max_key_len - len(cat[0]))}", end="")
        print(" | ", end="")

        rest_space = width - (len(cat[1]) + max_key_len + 5)
        if len(cat[1]) < rest_space:
            print(f"{cat[1]}", end="")
            print(f"{' ' * (width - len(cat[1]) - max_key_len - 5)}", end="")
            print(" |")
        else:
            # Split content y multiple lines
            prev = 0
            column_size = width - max_key_len - 5
            split_text = cat[1].split(" ")
            split_text_len = len(split_text)
            first = True

            while 1:
                text = ""
                for i, x in enumerate(split_text[prev:], start=1):

                    t_text = f"{text} {x}"

                    if len(t_text) > column_size:
                        prev += i
                        break

                    text += f"{x} "

                else:
                    prev = split_text_len

                if first:
                    print(f"{text}{' ' * (column_size - len(text))}", end="")
                    print(" |")
                    first = False
                else:
                    print(f"| "
                          f"{' ' * max_key_len}"
                          f" | "
                          f"{text}{' ' * (column_size - len(text))}", end="")
                    print(" |")

                if prev >= split_text_len:
                    break

        border()


def list_packages(args: argparse.Namespace):
    catalog = get_catalog()

    print_table(head=("Name", "Version"),
                content=[(x["name"], x["version"]) for x in catalog],
                width=50)


def install_package(args: argparse.Namespace):

    def docker_hub_image(image_name: str, version: str) -> str:
        return f"bbvalabs/{image_name}:{version}"

    def get_or_create_config_path() -> Path:
        _path = Path().home().joinpath(".apicheck_manager")

        if not _path.exists():
            print(
                f"[*] Creating path for storing apicheck tools at : "
                f"{str(_path)}/bin"
            )
            os.mkdir(str(_path))

        return _path

    def load_current_config(_path) -> dict:
        if not _path.joinpath("meta.json").exists():
            meta = {"installed": {}}
        else:
            with open(str(_path.joinpath("meta.json")), "r") as f:
                meta = json.load(f)

        return meta

    def build_tool_script(path: Path,
                          image_name: str,
                          version: str,
                          short_command: str):

        base_script_path = path.joinpath("bin")

        if not base_script_path.exists():
            os.mkdir(str(base_script_path))

        script_path = str(base_script_path.joinpath(image_name))

        scripts = [script_path]

        if short_command:
            scripts.append(str(base_script_path.joinpath(short_command)))

        content = "\n".join([
            "#!/bin/sh",
            "",
            f"docker run --rm -i {docker_hub_image(image_name, version)} "
            f"\"$@\"",
        ])

        for s in scripts:

            with open(s, "w") as f:
                f.write(content)
            os.chmod(
                s,
                stat.S_IXUSR | stat.S_IRUSR | stat.S_IWUSR |
                stat.S_IRGRP | stat.S_IROTH
            )

    def pull_docker_image(image_name: str, version: str):
        #
        # Pull Docker image
        #
        _image_name = docker_hub_image(image_name, version)

        command = f"docker pull {_image_name}"

        proc = subprocess.Popen(command,
                                stdout=subprocess.PIPE,
                                shell=True)
        print("")
        while 1:
            line = proc.stdout.readline()

            if not line:
                break

            print("   ", line.decode("UTF-8"), end="")
        print("")

    tool_name = args.tool_name
    # docker_image_name = tool_name.replace('_', '-')

    # Common config
    config_path = get_or_create_config_path()
    config_file = load_current_config(config_path)

    # -------------------------------------------------------------------------
    # Search in catalog
    # -------------------------------------------------------------------------
    catalog = get_catalog()

    # Find tool
    tool = search_in_catalog(catalog, tool_name)
    if not tool:
        print(f"[!] Can't find tool named '{tool_name}'")
        exit(1)

    catalog_tool_name = tool["name"]
    catalog_tool_version = tool["version"]
    catalog_short_command = tool.get("short-command", "")

    # -------------------------------------------------------------------------
    # Install / update tool
    # -------------------------------------------------------------------------
    if catalog_tool_name not in config_file["installed"]:

        print(f"[*] Fetching Docker image for tool '{tool_name}'")
        pull_docker_image(catalog_tool_name, catalog_tool_version)
    else:
        if config_file["installed"][catalog_tool_name] != catalog_tool_version:
            print(f"[*] Updating Docker image for tool '{tool_name}'")
            pull_docker_image(catalog_tool_name, catalog_tool_version)
        else:
            print(f"\n[*] Tools is already installed\n")
            exit(0)

    #
    # Making script tools
    #
    print("[*] Making launch scripts")
    build_tool_script(config_path,
                      catalog_tool_name,
                      catalog_tool_version,
                      catalog_short_command)

    #
    # Fill env-file
    #
    print("[*] Updating configuration file ")
    config_file["installed"][tool_name] = tool["version"]

    #
    # Dump the config
    #
    with open(str(config_path.joinpath("meta.json")), "w") as f:
        json.dump(config_file, f)


def info_package(args: argparse.Namespace):
    tool_name = args.tool_name

    catalog = get_catalog()

    # Find tool
    tool = search_in_catalog(catalog, tool_name)
    if not tool:
        print(f"[!] Can't find tool named '{tool_name}'")
        exit(1)

    print()
    print_table(content=[
        tuple(y)
        for y in tool.items()
    ], head=(f"Tool name '{tool_name}'",), width=75)


def main():
    actions = {
        "list": list_packages,
        "info": info_package,
        "install": install_package,
        "version": lambda x: print(f"\nCurrent version: {_get_version()}\n"),
    }

    parser = argparse.ArgumentParser(description='APICheck Manager')
    parser.add_argument("-w", "--disable-warning",
                        action="store_true",
                        default=False,
                        help="disable check of RC Shell File")

    subparsers = parser.add_subparsers(dest="action", help='available actions')

    # create the parser for the "a" command
    tool_list = subparsers.add_parser('list', help='search in A')

    tool_info = subparsers.add_parser('info', help='show expanded tool info')
    tool_info.add_argument("tool_name")

    tool_install = subparsers.add_parser('install',
                                         help='install an APICheck tool')
    tool_install.add_argument("tool_name")

    version = subparsers.add_parser('version',
                                    help='displays version')

    cli_parsed = parser.parse_args()

    if not cli_parsed.action:
        print("\n[!] Invalid action name\n")
        parser.print_help()
        exit(1)

    rc_file = check_apicheck_is_in_path()
    if not cli_parsed.disable_warning and rc_file:
        print("\n".join([
            "-" * 65,
            " WARNING: \n",
            " You must include apic heck path to your shell RC file.\n",
            " Please add: 'export PATH=\"$HOME/.apicheck_manager/bin:$PATH\"'",
            f" to your '{rc_file}' file",
            "-" * 65
        ]))

    # Launch action
    try:
        actions[cli_parsed.action](cli_parsed)
    except CatalogCheckSumError as e:
        print(f"[!] {e}")


if __name__ == '__main__':
    main()
