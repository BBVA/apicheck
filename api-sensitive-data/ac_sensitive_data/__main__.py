import os
import re
import sys
import json
import select

from typing import List

import yaml
import requests
import argparse

from terminaltables import AsciiTable

HERE = os.path.dirname(__file__)


def _process_results(args: argparse.Namespace, found_issues: List[dict]):

    # -------------------------------------------------------------------------
    # Building results
    # -------------------------------------------------------------------------
    table_data = [
        ['Rule Id', 'Description', 'Severity'],
    ]

    if not found_issues:
        table_data.append(["No issues found"])
    else:

        for res in found_issues:
            table_data.append((
                res["id"],
                res["description"],
                res["severity"]
            ))

        # Export results
        if args.output_file:
            with open(args.output_file, "w") as f:
                json.dump(found_issues, f)

    if not args.quiet:
        if sys.stdout.isatty():
            # We're in terminal
            print(AsciiTable(table_data).table)
        else:
            try:
                sys.stdout.write(json.dumps(found_issues))
                sys.stdout.flush()
            except (BrokenPipeError, IOError) as e:
                # Piped command doesn't support data input as pipe
                sys.stderr.write(e)
            except Exception as e:
                pass


def _load_rules(args: argparse.Namespace) -> List[dict]:
    """Load rules files from local o remote"""
    default_rules_path = os.path.join(HERE, "rules.yaml")

    with open(default_rules_path, "r") as f:
        rules = yaml.safe_load(f.read())

    if args.rules_file:
        for rule_file in args.rules_file:
            if rule_file.startswith("http"):
                # Load from remote URL
                rules.extend(
                    yaml.safe_load(requests.get(rule_file).content)
                )
            else:
                # Load from local file
                real_file_path = os.path.join(os.getcwd(), rule_file)
                with open(real_file_path, "r") as f:
                    rules.extend(yaml.safe_load(f.read()))

    return rules


def _load_ignore_ids(args: argparse.Namespace) -> List[str]:
    """Load ignores files from local o remote"""

    ignores = []

    if args.ignore_rule:
        for x in args.ignore_rule:
            ignores.extend(x.split(","))

    if args.ignore_file:
        for rule_file in args.ignore_file:
            if rule_file.startswith("http"):
                # Load from remote URL
                ignores.extend(requests.get(rule_file).content.splitlines())
            else:
                # Load from local file
                real_file_path = os.path.join(os.getcwd(), rule_file)
                with open(real_file_path, "r") as f:
                    ignores.extend([x.replace("\n", "") for x in f.readlines()])

    return ignores


def analyze(args: argparse.Namespace):
    # -------------------------------------------------------------------------
    # Load Dockerfile by stdin or parameter
    # -------------------------------------------------------------------------
    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        content = sys.stdin.read()
    else:
        raise FileNotFoundError("Input data needed")

    rules = _load_rules(args)
    ignores = set(_load_ignore_ids(args))

    found_issues = []

    # Matching
    for rule in rules:

        if rule["id"] in ignores:
            continue

        #
        # TODO: here the logic
        #
        regex = re.search(rule["regex"], content)

        if regex:
            res = rule.copy()
            del res["regex"]

            found_issues.append(res)

    _process_results(args, found_issues)


def main():
    parser = argparse.ArgumentParser(
        description='Analyze a HTTP Request / Response for sensitive data'
    )
    parser.add_argument('-F', '--ignore-file',
                        action="append",
                        help="file with ignores rules")
    parser.add_argument('-i', '--ignore-rule',
                        action="append",
                        help="rule to ignore")
    parser.add_argument('-r', '--rules-file',
                        action="append",
                        help="rules file. One rule ID per line")
    parser.add_argument('-o', '--output-file',
                        help="output file path")
    parser.add_argument('-q', '--quiet',
                        action="store_true",
                        default=False,
                        help="quiet mode")
    parsed_cli = parser.parse_args()

    try:
        analyze(parsed_cli)
    except Exception as e:
        print("[!] ", e)


if __name__ == '__main__':
    main()
