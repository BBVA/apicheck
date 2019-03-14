

def cli(parser):

    proxy_args = parser.add_parser(
        'dataset',
        help='Generate a dataset from proxy trafic')
    proxy_args.add_argument('fout',
                            help="output file to store results")
