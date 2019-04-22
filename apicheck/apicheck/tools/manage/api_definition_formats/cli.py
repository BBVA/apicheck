from .config import RunningConfig


def cli(parser):
    proxy_args = parser.add_parser(
        'definition',
        help='Load API Definition format (OpenAPI 3.0, RAML, Swagger)')
    proxy_args.add_argument('file_path',
                            metavar="file_path",
                            help="file definition path")
    proxy_args.add_argument('-F', '--format',
                            dest="format",
                            choices=list(x.lower()
                                         for x, _ in
                                         RunningConfig.FORMAT_CHOICES),
                            help="file format definition")
    proxy_args.add_argument('-n', '--api-name',
                            dest="api_name",
                            help="manually setup of API name"
                                 "(default: imported from file definition)")
    proxy_args.add_argument('-p', '--api-version',
                            dest="api_version",
                            help="manually setup of API version"
                                 "(default: imported from file definition)")
    proxy_args.add_argument('-x',
                            dest="append_to_metadata",
                            help="append definition to existing API")
