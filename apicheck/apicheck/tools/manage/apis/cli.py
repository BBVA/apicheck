

def cli(parser):

    plugin_args = parser.add_parser(
        'api',
        help='Manage stored APIs')
    plugin_args.add_argument('api_action',
                             default="list",
                             help="list stores APIs")
