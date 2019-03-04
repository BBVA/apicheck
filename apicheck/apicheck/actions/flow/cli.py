

def cli(parser):

    proxy_args = parser.add_parser(
        'flow',
        help='Send API definition to proxy')
    proxy_args.add_argument('fout',
                            help="output file to store results")
