from .config import RunningConfig


def cli(parser):

    proxy_args = parser.add_parser(
        'send-proxy',
        help='Send API definition to proxy')
    proxy_args.add_argument('api_id',
                            help="api definition ID to send")
    proxy_args.add_argument('--source',
                            dest="source",
                            default="definition",
                            choices=RunningConfig.OPERATION_MODES,
                            help="origin of data. Default: definition")
    proxy_args.add_argument('--proxy',
                            dest="proxy_destination",
                            required=True,
                            help="proxy destination. IP:PORT")
