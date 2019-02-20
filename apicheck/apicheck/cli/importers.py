import argparse

from apicheck.sources.proxy import cli_args_proxy


def cli():
    parser = argparse.ArgumentParser(
        description="API-Check importer commands"
    )

    subparsers = parser.add_subparsers(dest="importer_type",
                                       description="Valid actions",
                                       help='Actions')

    #
    # Add subparsers
    #
    cli_args_proxy(subparsers)

    #
    # Parse cli
    #
    args = parser.parse_args()

    #
    # Choice correct config object
    #
    importer_config = importer_function = None
    importer_type = args.importer_type

    if importer_type == "proxy":
        from apicheck.sources.proxy import ProxyConfig, launch_apicheck_proxy

        importer_config = ProxyConfig
        importer_function = launch_apicheck_proxy

    if not importer_config or not importer_function:
        print()
        if importer_type is None:
            print(f"[!] Importer type is needed")
        else:
            print(f"[!] Invalid importer: '{importer_type}'")
        print()

        exit(1)

    running_config = args.__dict__
    running_config.pop("importer_type")

    #
    # Launch API Check
    #
    importer_function(importer_config(**running_config))


if __name__ == '__main__':
    cli()
