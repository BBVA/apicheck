import os
import json
import hashlib
import argparse
import subprocess
import urllib.request
from collections import defaultdict

from pathlib import Path

# -------------------------------------------------------------------------
# Alias management
# -------------------------------------------------------------------------
from typing import List, Tuple, Set

RC_FILES = {
    "bash": ".bashrc",
    "zsh": ".zshrc"
}

VERSION = "1.0.0"


class CatalogCheckSumError(Exception):
    pass


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
CATALOG_REMOTE_FILE = "https://bbva.github.io/apicheck/assets/catalog.json"
CATALOG_CHECK_SUM = \
    "https://bbva.github.io/apicheck/assets/catalog.json.checksum"


def get_catalog() -> List[dict] or CatalogCheckSumError:
    # Fetch remote catalog
    with urllib.request.urlopen(CATALOG_REMOTE_FILE) as catalog, \
            urllib.request.urlopen(CATALOG_CHECK_SUM) as check_sum:
        raw_content = catalog.read()
        remote_catalog_check_sum = check_sum.read()

        h = hashlib.sha512()
        h.update(raw_content.encode("UTF-8"))
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
                f"{' ' * (width - (max_key_len + len(head[1]) + 5 ))}",
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

    command = f"docker pull {docker_image_name}"

    proc = subprocess.Popen(command,
                            stdout=subprocess.PIPE,
                            shell=True)

    # while line := proc.stdout.poll():
    print("")
    while line := proc.stdout.readline():
        print("   ", line.decode("UTF-8"), end="")
    print("")

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

    #
    # Add to installed packages
    #
    if not path.joinpath("meta.json").exists():
        meta = defaultdict(dict)
        meta["environments"][env_name] = {}
    else:
        with open(str(path.joinpath("meta.json")), "r") as f:
            meta = json.load(f)

    env_config = meta["environments"][env_name]

    if "installed" not in env_config:
        env_config["installed"] = []

    # Search for already installed
    for s in env_config["installed"]:
        if s["name"] == tool_name and s["version"] == tool["version"]:
            break
    else:
        env_config["installed"].append({
            "name": tool_name,
            "version": tool["version"]
        })

    #
    # Dump the config
    #
    with open(str(path.joinpath("meta.json")), "w") as f:
        json.dump(meta, f)


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

    with open(str(env_path_route), "r") as f:
        print(f.read())


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


def describe_env(args: argparse.Namespace):
    env_name = args.env_name or "default"

    meta = Path().home().joinpath(".apicheck_manager").joinpath("meta.json")

    if not meta.exists():
        print("[i] There's not APICheck tools installed yet")
        exit(0)

    with open(str(meta), "r") as f:
        meta_json = json.load(f)

    if env_name not in meta_json["environments"]:
        print(f"[!] Environment '{env_name}' doesnt exits")
        exit(1)

    env_info = meta_json["environments"][env_name]

    print_table(content=[("Environment", env_name)])
    content = [
        (y["name"], y["version"])
        for y in env_info["installed"]
    ]
    print(f"|{'|' * 60}|")
    print_table(content=content, head=(f"Tool name", "Version"))


def list_environments(args: argparse.Namespace):

    base = Path().home().joinpath(".apicheck_manager")
    meta = base.joinpath("meta.json")

    if not meta.exists():
        print("[i] There's not APICheck tools installed yet")
        exit(0)

    with open(str(meta), "r") as f:
        meta_json = json.load(f)

    # Get environments
    environments = [
        x for x in os.listdir(str(base))
        if not x.endswith("json") and not x.endswith("deactivate")
    ]

    results = []
    for env in environments:
        _env = meta_json["environments"][env]
        results.append((
            env,
            str(len(_env.get("installed", 0))))
        )

    print_table(content=results,
                head=(f"Environment Name", "Number of installed tools"))


def main():
    actions = {
        "list": list_packages,
        "info": info_package,
        "install": install_package,
        "activate": activate_env,
        "describe": describe_env,
        "envs": list_environments,
        "version": lambda x: print(f"\nCurrent version: {VERSION}\n"),
    }

    parser = argparse.ArgumentParser(description='APICheck Manager')
    parser.add_argument("-H", "--docker-host",
                        dest="docker_host",
                        default=None,
                        help="docker url. default: tcp://127.0.0.1:2375")

    subparsers = parser.add_subparsers(dest="action", help='available actions')

    # create the parser for the "a" command
    tool_list = subparsers.add_parser('list', help='search in A')

    tool_info = subparsers.add_parser('info', help='show expanded tool info')
    tool_info.add_argument("tool_name")

    tool_install = subparsers.add_parser('install',
                                         help='install an APICheck tool')
    tool_install.add_argument("tool_name")
    tool_install.add_argument("-e", "--environment-name",
                              dest="env_name",
                              default=None,
                              help="custom environment name")

    tool_activate = subparsers.add_parser('activate',
                                          help='activate an environment')
    tool_activate.add_argument("-e", "--environment-name",
                               dest="env_name",
                               default=None,
                               help="custom environment name")

    tool_activate = subparsers.add_parser('describe',
                                          help='show info of environment')
    tool_activate.add_argument("-e", "--environment_name",
                               dest="env_name",
                               nargs="*",
                               default=None,
                               help="show information about environments")

    environments = subparsers.add_parser('envs',
                                         help='show available environments')

    version = subparsers.add_parser('version',
                                    help='displays version')

    cli_parsed = parser.parse_args()

    if not cli_parsed.action:
        print("\n[!] Invalid action name\n")
        parser.print_help()
        exit(1)

    # Launch action
    try:
        actions[cli_parsed.action](cli_parsed)
    except CatalogCheckSumError as e:
        print(f"[!] {e}")


if __name__ == '__main__':
    main()
