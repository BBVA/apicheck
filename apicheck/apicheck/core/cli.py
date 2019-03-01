def cli_global_args(parser):
    """This functions adds the common global options for the cli interface"""
    parser.add_argument('-C', '--connection-string',
                        dest="db_connection_string",
                        required=True,
                        help="database connection string")
    parser.add_argument('--log-level',
                        dest="log_level",
                        default="INFO",
                        choices=("DEBUG", "INFO", "WARNING", "ERROR",
                                 "CRITICAL"),
                        help="define log level")
