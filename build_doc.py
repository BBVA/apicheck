"""
This file build the documentation for APICheck
"""
import os
import csv
import json
import hashlib
import configparser

HERE = os.path.abspath(os.path.dirname(__file__))
URL_PREFIX = "/apicheck"

DOC_PATH = os.path.join(HERE, "docs")
TOOLS_PATH = os.path.join(HERE, "tools")
STATIC_PATH = os.path.join(HERE, "docs", "assets")

META_KEYS = ("name", "short-command", "version", "description",
             "home", "author")


def main():

    catalog = []
    short_commands = set()
    tool_names = set()

    tools_brief = {}

    #
    # Getting README from plugin
    #
    for d in os.listdir(TOOLS_PATH):

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
        home = meta["home"]
        author = meta["author"]
        tool_name = meta["name"]
        description = meta["description"]
        short_command = meta["short-command"]

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
        tools_brief[tool_name] = (description, author, home)

        #
        # Build tools documentation
        #
        doc_tool_path = os.path.join(DOC_PATH,
                                     "docs",
                                     "tools",
                                     d.replace("_", "-"))
        readme_title = readme_text[0].replace("#", "").strip()

        with open(os.path.join(f"{doc_tool_path}.md"), "w") as f:
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
    tools_index_path = os.path.join(DOC_PATH,
                                    "docs",
                                    "index")
    # Build text for index
    built_index_content = []

    for t_name, (t_brief, t_author, t_home_page) in tools_brief.items():
        built_index_content.append(f"""
    <div class="summary mb-2">
        <h2 class="title-summary"><a href="{{{{ "/tools/{t_name}/" | relative_url }}}}">{t_name.capitalize()}</a></h2>
        <p>{t_brief}</p>
        <ul>
            <ol>- Author: <b>{t_author}</b></ol>
            <ol>- Developer Site: <a target="_blank" href="{t_home_page}">{t_home_page}</a></ol>
        </ul>
        <br />
        <a class="button button-primary mb-2" href="{{{{ "/tools/{t_name}/" | relative_url }}}}">Go to doc &rarr;</a>
    </div>
""")

    with open(os.path.join(f"{tools_index_path}.html.template"), "r") as f:
        index_template_content = f.read()

    with open(os.path.join(f"{tools_index_path}.html"), "w") as f:
        f.write(index_template_content.format(
            content="\n".join(built_index_content))
        )

    #
    # Build Menu
    #
    tools_menu_path = os.path.join(DOC_PATH, "_layouts", "doc")
    # Build text for index
    tools_menu = []

    for t_name in tools_brief.keys():
        tools_menu.append(f"""
                        <li class="active">
                            <a href="{{{{ "/tools/{t_name}/" | relative_url }}}}">{t_name.capitalize()}</a>
                        </li>
""")

    with open(os.path.join(f"{tools_menu_path}.html.template"), "r") as f:
        menu_content = f.read()

    with open(os.path.join(f"{tools_menu_path}.html"), "w") as f:
        f.write(menu_content.format(
            dynamic_content="\n".join(tools_menu))
        )

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