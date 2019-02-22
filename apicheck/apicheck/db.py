import asyncio
import builtins

from sqlalchemy.schema import CreateTable
from sqlalchemy_aio import ASYNCIO_STRATEGY

from sqlalchemy import (
    Column, Integer, MetaData, Table, Text, create_engine, ForeignKey, String)


def setup_db_engine(db_query_string: str = None):

    if not hasattr(builtins, "apicheck_db_engine"):
        builtins.apicheck_db_engine = create_engine(
            # In-memory sqlite database cannot be accessed from different
            # threads, use file.
            db_query_string, strategy=ASYNCIO_STRATEGY
        )

    #
    # Creating database
    #
    loop = asyncio.get_event_loop()

    print("[*] Creating database...", end='')
    engine = builtins.apicheck_db_engine

    tables_to_create = [
        ProxyLogs, APIDefinitionMetadata, APIRequests,APIResponses
    ]

    for table in tables_to_create:
        try:
            loop.run_until_complete(engine.execute(CreateTable(table)))
        except Exception as e:

            #
            # Ignore errors when a table already exits in the database
            #
            if "already exists" in str(e):
                continue
            else:
                print(e)

    print("done")


def get_engine():
    return builtins.apicheck_db_engine


metadata = MetaData()

# -------------------------------------------------------------------------
# Database definition
# -------------------------------------------------------------------------
ProxyLogs = Table(
    'proxy_logs', metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("proxy_session_id", String(40)),
    Column("request", Text, nullable=False),
    Column("response", Text, nullable=False),
    Column("request_id", Integer, ForeignKey("requests.id"), nullable=True),
)

APIDefinitionMetadata = Table(
    'metadata', metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("api_name", String(200), unique=True),
    Column("api_version", String(200)),

)

APIRequests = Table(
    'requests', metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("uri", Text, index=True),
    Column("http_version", Text),
    Column("headers", Text),
    Column("body", Text),
    Column("metadata_id", Integer, ForeignKey("metadata.id"), nullable=False),
)
APIResponses = Table(
    'responses', metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("http_code", Text),
    Column("http_message", Text),
    Column("headers", Text),
    Column("body", Text),
    Column("requests_id", Integer, ForeignKey("requests.id"), nullable=False),
)
