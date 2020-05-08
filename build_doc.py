"""
This file build the documentation for APICheck
"""
import os
import re
import json
import hashlib
import configparser

HERE = os.path.abspath(os.path.dirname(__file__))
URL_PREFIX = "/apicheck"

DOC_PATH = os.path.join(HERE, "docs")
TOOLS_PATH = os.path.join(HERE, "tools")
STATIC_PATH = os.path.join(HERE, "docs", "assets")

META_KEYS = ("name", "version", "description",
             "home", "author")

OPTIONAL_KEYS = ("short-command", )
NAME_FORMAT_REGEX = r"([A-Za_-z0-9]+)"


def main():

    catalog = []
    short_commands = set()
    tool_names = set()

    tools_brief = {}

    #
    # Getting README from plugin
    #
    for d in os.listdir(TOOLS_PATH):

        if d.startswith("."):
            continue

        # Get README.md file
        tools_path = os.path.join(TOOLS_PATH, d)

        meta_path = os.path.join(tools_path, "META")
        readme_path = os.path.join(tools_path, "README.md")

        try:
            with open(readme_path, "r") as readme_handler:
                readme_text = readme_handler.readlines()
        except OSError:
            print(f"[!] Tool \"{d}\" doesnt has README.md file")
            continue

        try:
            with open(meta_path, "r") as meta_handler:
                cf = configparser.ConfigParser()
                cf.read_string(f"[DEFAULT]\n {meta_handler.read()}")

                meta = dict(cf["DEFAULT"])

        except OSError:
            print(f"[!] Tool \"{d}\" doesnt has README.md file")
            continue

        # Check that META contains all needed keys
        if not all(x in meta.keys() for x in META_KEYS):
            print(f"[!] Missing keys in META \"{d}\". "
                  f"Needed keys: \"{', '.join(META_KEYS)}\"")
            exit(1)

        #
        # Check that 'name' and 'short-command' are unique
        #
        tool_name = meta["name"]

        if not re.match(NAME_FORMAT_REGEX, tool_name):
            print(f"Invalid name format for: '{tool_name}'. "
                  f"Only allowed : A-Za_-z0-9")
            exit(1)

        home = meta["home"]
        author = meta["author"]
        description = meta["description"]
        display_name = meta.get("display-name", "") or tool_name
        short_command = meta.get("short-command", None)

        if short_command:
            if short_command in short_commands:
                print(f"[!] Short-command \"{short_command}\" at tool "
                      f"'{tool_name}' already exits in another tool")
                exit(1)
            else:
                short_commands.add(short_command)

        if tool_name in tool_names:
            print(f"[!] Tool name '{tool_name}' already exits used "
                  f"for other tool")
            exit(1)
        else:
            tool_names.add(tool_name)

        catalog.append(meta)
        tools_brief[tool_name] = (description, author, home, display_name)

        #
        # Build tools documentation
        #
        doc_tool_path = os.path.join(DOC_PATH,
                                     "docs",
                                     "tools")
        readme_title = readme_text[0].replace("#", "").strip()

        if not os.path.exists(doc_tool_path):
            os.makedirs(doc_tool_path, exist_ok=True)

        with open(os.path.join(doc_tool_path,
                               f"{d.replace('_', '-')}.md"), "w") as f:
            f.write("\n".join([
                "---",
                "layout: doc",
                f"title: {readme_title}",
                f"permalink: /tools/{tool_name}",
                "---",
                "\n",
            ]))
            f.writelines(readme_text)
            f.flush()

    #
    # Build tools index
    #
    tool_menu_item = []
    for t_name, (t_brief, t_author, t_home_page, display_name) in tools_brief.items():
        tool_menu_item.append(f"  - title: {display_name}")
        tool_menu_item.append(f"    author: {t_author}")
        tool_menu_item.append(f"    home: {t_home_page}")
        tool_menu_item.append(f"    brief: {t_brief}")
        tool_menu_item.append(f"    url: /tools/{t_name}")
        tool_menu_item.append("")

    #
    # Build Menu
    #
    tools_menu_path_data = os.path.join(DOC_PATH, "_data", "tools.yaml")
    tools_yaml_data = """
menu_title: Tool list

menu:

"""

    with open(os.path.join(tools_menu_path_data), "w") as f:
        f.write(tools_yaml_data)
        f.write("\n".join(tool_menu_item))

    #
    # Build catalog
    #
    catalog_path = os.path.join(STATIC_PATH, "catalog.json")
    catalog_path_checksum = os.path.join(STATIC_PATH, "catalog.json.checksum")
    with open(catalog_path, "w") as f, open(catalog_path_checksum, "w") as c:
        cat_content = json.dumps(catalog)

        h = hashlib.sha512()
        h.update(cat_content.encode("UTF-8"))

        f.write(cat_content)
        c.write(h.hexdigest())


if __name__ == '__main__':
    main()