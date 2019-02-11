import argparse


def common_cli_args(description: str):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-d', '--storage',
                        dest="storage",
                        help="backend storage choice")

    parser.add_argument_group('MongoDB')
    parser.add_argument('-H', '--mongo-host',
                        dest='mongo_host',
                        help='database host IP')
    parser.add_argument('--mongo-port',
                        dest='mongo_port',
                        help='database port')
    parser.add_argument('-U', '--mongo-user',
                        dest='mongo_user',
                        help='database username')
    parser.add_argument('-P', '--mongo-password',
                        dest='mongo_password',
                        help='database password')

    return parser
