import sys
import yaml
import json
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="YAML to JSON Converter"
    )
    parser.add_argument('YAML_FILE',
                        nargs="?",
                        help="YAML File")
    parser.add_argument('-P',
                        action="store_true",
                        default=False,
                        dest="indent",
                        help="indent json result file")

    parsed = parser.parse_args()

    if parsed.YAML_FILE:

        with open(parsed.YAML_FILE, "r") as f:
            input_content = f.read()
    else:
        input_content = sys.stdin.read()

    json.dump(yaml.load(input_content, Loader=yaml.FullLoader),
              sys.stdout,
              indent=4 if parsed.indent else None)


if __name__ == '__main__':
    main()
