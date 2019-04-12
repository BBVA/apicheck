from .config import RunningConfig


def cli(parser):

    custom_parser = parser.add_parser(
        'send-proxy',
        help='Send API definition to proxy')
    custom_parser.add_argument('api_id',
                               help="api definition ID to send")
    custom_parser.add_argument('--source',
                               dest="source",
                               default="definition",
                               choices=RunningConfig.OPERATION_MODES,
                               help="origin of data. Default: definition")
    custom_parser.add_argument('--proxy',
                               dest="proxy_destination",
                               required=True,

                               help="proxy destination. IP:PORT")

    c = custom_parser.add_argument_group("API Definitions")
    c.add_argument("--api-url",
                   dest="api_url",
                   help="api base url used for requests")
