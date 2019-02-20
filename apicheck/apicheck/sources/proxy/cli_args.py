def cli_args_proxy(parser):

    proxy_args = parser.add_parser('proxy', help='start a HTTP(s) proxy')
    proxy_args.add_argument('domain',
                            metavar="domain",
                            help="Domain to inspect using proxy")
    proxy_args.add_argument('-l', '--listen',
                            dest="listen_addr",
                            default="127.0.0.1",
                            help="proxy listen address (default: 127.0.0.1)")
    proxy_args.add_argument('-p', '--port',
                            dest="listen_port",
                            help="proxy listen port (default: 8080)")
    proxy_args.add_argument('-C', '--connection-string',
                            dest="db_connection_string",
                            required=True,
                            help="database connection string")
    proxy_args.add_argument('--store-assets',
                            action="store_true",
                            default=False,
                            dest="store_assets_content",
                            help="store assets content in database")
