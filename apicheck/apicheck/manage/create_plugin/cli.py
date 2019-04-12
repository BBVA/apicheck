

def cli(subparser):

    plugin_args = subparser.add_parser(
        'create-plugin',
        help='Manage stored APIs')

    plugin_args.add_argument('name',
                             help="plugin name")
    plugin_args.add_argument('--dest', "-d",
                             required=True,
                             help="plugin dir destination")
