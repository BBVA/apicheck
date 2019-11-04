def cli_log_level(parser):
    """This functions adds log level option to the CLI"""
    parser.add_argument('--log-level',
                        dest="log_level",
                        default="INFO",
                        choices=("DEBUG", "INFO", "WARNING", "ERROR",
                                 "CRITICAL"),
                        help="define log level")


def cli_db(parser):
    """This functions adds the db configuration to the CLI"""
    parser.add_argument('-C', '--connection-string',
                        dest="db_connection_string",
                        required=True,
                        help="database connection string")
