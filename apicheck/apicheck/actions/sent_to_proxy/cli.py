

def cli(parser):

    proxy_args = parser.add_parser(
        'send-proxy',
        help='Send API definition to proxy')
    proxy_args.add_argument('api_id',
                            help="api definition ID to send")
