"""
This file build the documentation for APICheck
"""
import os
import json
import configparser

HERE = os.path.abspath(os.path.dirname(__file__))

DOC_PATH = os.path.join(HERE, "docs")
TOOLS_PATH = os.path.join(HERE, "tools")
STATIC_PATH = os.path.join(HERE, "docs", "static")


def main():

    catalog = []

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

                catalog.append(dict(cf["DEFAULT"]))

        except OSError:
            print(f"[!] Tool \"{d}\" doesnt has README.md file")
            continue

        #
        # Build tools documentation
        #
        doc_tool_path = os.path.join(DOC_PATH, "content", d.replace("_", "-"))
        readme_title = readme_text[0].replace("#", "").strip()

        if not os.path.exists(doc_tool_path):
            os.mkdir(doc_tool_path)

        with open(os.path.join(doc_tool_path, "index.md"), "w") as f:
            f.write(f"---\ntitle: {readme_title}\n---\n")
            f.write("\n".join(readme_text))
            f.flush()

    #
    # Build catalog
    #
    with open(os.path.join(STATIC_PATH, "catalog.json"), "w") as f:
        json.dump(catalog, f)


if __name__ == '__main__':
    main()