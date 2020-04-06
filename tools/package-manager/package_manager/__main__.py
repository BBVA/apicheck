import os
import json
import argparse
import urllib.request

from pathlib import Path

# -------------------------------------------------------------------------
# Alias management
# -------------------------------------------------------------------------
from typing import List, Tuple, Set

RC_FILES = {
    "bash": ".bashrc",
    "zsh": ".zshrc"
}


def get_current_rc_file():
    shell_name = Path(os.environ.get("SHELL", "/bin/bash")).name

    try:
        rc_file = RC_FILES[shell_name]
    except KeyError:
        rc_file = RC_FILES["bash"]

    return rc_file


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


# -------------------------------------------------------------------------
# Catalog manage
# -------------------------------------------------------------------------
CATALOG_REMOTE_FILE = "https://bbva.github.io/apicheck/catalog.json"


def get_catalog() -> List[dict]:
    # Fetch remote catalog
    with urllib.request.urlopen(CATALOG_REMOTE_FILE) as response:
        catalog_json = json.loads(response.read())

    return catalog_json


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
        border()
        if len(head) == 2:
            print(f"| {head[0]}", end="")
            print(f"{' ' * (max_key_len - 4)}", end="")
            print(" | ", end="")
            print(f"{head[1]}", end="")
            print(
                f"{' ' * (width - len(head[0]) - len(head[1]) - max_key_len - 1)}",
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

        rest_space = width - len(cat[1]) - max_key_len - 5
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
                for i, x in enumerate(split_text[prev:]):

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
                content=[(x["name"], x["version"]) for x in catalog])


def install_package(args: argparse.Namespace):

    def build_alias_cmd(cmd: str, docker_image: str):
        return f'''alias {cmd}="docker run --rm -i {docker_image}"'''

    tool_name = args.tool_name
    env_name = args.env_name or "default"
    docker_image_name = tool_name.replace('_', '-')

    catalog = get_catalog()

    # Find tool
    if not (tool := search_in_catalog(catalog, tool_name)):
        print(f"[!] Can't find tool named '{tool_name}'")
        exit(1)

    catalog_tool_name = tool["name"]
    catalog_short_command = tool["short-command"]

    #
    # Pull Docker image
    #
    print(f"[*] Fetching Docker image for tool '{tool_name}'")
    docker_image_name = f"bbvalabs/{docker_image_name}"
    docker_image_name = "python:3.8-alpine"

    command = f"docker pull {docker_image_name}"

    # os.system(command)

    #
    # Get / create environment config file
    #
    path = Path().home().joinpath(".apicheck_manager")

    if not path.exists():
        print(
            f"[*] Creating path for storing apicheck environments at : "
            f"{str(path)}"
        )
        os.mkdir(str(path))

    env_path_route_deactivate = path.joinpath(f"{env_name}.deactivate")
    deactivate_env_path = str(env_path_route_deactivate)
    if not env_path_route_deactivate.exists():
        print(f"[*] Creating deactivate env config for '{env_name}'")

        header = [
            f"""PS1=$(echo $PS1 | sed 's/[(]APICheck[)][ ]//g')""",
        ]

        with open(str(deactivate_env_path), "w") as f:
            f.write("\n".join(header))

    env_path_route = path.joinpath(env_name)
    activate_env_path = str(env_path_route)
    if not env_path_route.exists():
        print(f"[*] Creating env config for '{env_name}'")

        header = [
            '''PS1="(APICheck) $PS1"''',
            f'''alias deactivate="source {deactivate_env_path}"''',
        ]

        with open(str(activate_env_path), "w") as f:
            f.write("\n".join(header))

    #
    # Fill env-file
    #
    print("[*] filling environment alias file ")

    alias1 = build_alias_cmd(catalog_tool_name, docker_image_name)
    alias2 = build_alias_cmd(catalog_short_command, docker_image_name)

    add_new_alias(activate_env_path, alias1)
    add_new_alias(activate_env_path, alias2)

    rm_new_alias(deactivate_env_path, catalog_tool_name)
    rm_new_alias(deactivate_env_path, catalog_tool_name)


def activate_env(args: argparse.Namespace):
    env_name = args.env_name or "default"

    #
    # Get / create environment config file
    #
    path = Path().home().joinpath(".apicheck_manager")

    if not path.exists():
        print("[!] Env name doesn't exits")
        exit(1)

    env_path_route = path.joinpath(env_name)
    if not env_path_route.exists():
        print("[!] Env name doesn't exits")

    os.system(f"source {env_path_route}")


def info_package(args: argparse.Namespace):
    tool_name = args.tool_name

    catalog = get_catalog()

    # Find tool
    if not (tool := search_in_catalog(catalog, tool_name)):
        print(f"[!] Can't find tool named '{tool_name}'")
        exit(1)

    print()
    print_table(content=[
        tuple(y)
        for y in tool.items()
    ], head=(f"Tool name '{tool_name}'",))


def main():
    actions = {
        "list": list_packages,
        "info": info_package,
        "install": install_package,
        "activate": activate_env
    }

    parser = argparse.ArgumentParser(description='APICheck Manager')
    subparsers = parser.add_subparsers(dest="action", help='available actions')

    # create the parser for the "a" command
    tool_install = subparsers.add_parser('install',
                                         help='install an APICheck tool')
    tool_install.add_argument('bar', type=int, help='bar help')

    # create the parser for the "a" command
    tool_list = subparsers.add_parser('list', help='search in A')

    tool_info = subparsers.add_parser('info', help='show expanded tool info')
    tool_info.add_argument("tool_name")

    tool_info = subparsers.add_parser('install',
                                      help='install an APICheck tool')
    tool_info.add_argument("tool_name")
    tool_info.add_argument("-e", "--environment-name",
                           dest="env_name",
                           default=None,
                           help="custom environment name")

    tool_activate = subparsers.add_parser('activate',
                                          help='activate an environment')

    tool_activate.add_argument(
        "-e", "--environment-name",
        dest="env_name",
        default=None,
        help="custom environment name")
    tool_activate.add_argument(
        "-H", "--docker-host",
        dest="docker_host",
        default=None,
        help="docker url. default: tcp://127.0.0.1:2375")

    cli_parsed = parser.parse_args()

    if not cli_parsed.action:
        print("\n[!] Invalid action name\n")
        parser.print_help()
        exit(1)

    # Launch action
    actions[cli_parsed.action](cli_parsed)


if __name__ == '__main__':
    main()
