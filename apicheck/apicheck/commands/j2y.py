import sys
import yaml
import json
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Json to YAML Converter"
    )
    parser.add_argument('JSON_FILE',
                        nargs="?",
                        help="Domain to inspect using proxy")

    parsed = parser.parse_args()

    if parsed.JSON_FILE:

        with open(parsed.JSON_FILE, "r") as f:
            input_content = f.read()
    else:
        input_content = sys.stdin.read()

    return yaml.dump(json.loads(input_content), sys.stdout)


if __name__ == '__main__':
    main()
