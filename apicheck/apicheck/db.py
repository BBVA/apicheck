import asyncio
import builtins

from sqlalchemy.engine import Engine
from sqlalchemy.schema import CreateTable
from sqlalchemy_aio import ASYNCIO_STRATEGY

from sqlalchemy import (
    Column, Integer, MetaData, Table, Text, create_engine, ForeignKey, String)


def setup_db_engine(db_query_string: str = None):

    if not hasattr(builtins, "apicheck_db_engine"):
        builtins.apicheck_db_engine: Engine = create_engine(
            db_query_string, strategy=ASYNCIO_STRATEGY
        )
        builtins.apicheck_db_engine_sync: Engine = create_engine(
            db_query_string
        )

    #
    # Creating database
    #
    loop = asyncio.get_event_loop()

    print("[*] Creating database...", end='')
    engine = builtins.apicheck_db_engine_sync

    tables_to_create = [
        # ProxyLogs, APIMetadata, APIRequests, APIResponses, APIDefinitions
        ProxyLogs, APIMetadata, APIDefinitions
    ]

    for table in tables_to_create:
        try:
            engine.execute(CreateTable(table))
        except Exception as e:

            #
            # Ignore errors when a table already exits in the database
            #
            if "already exists" in str(e):
                continue
            else:
                print(e)

    print("done")


def get_engine() -> Engine:
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
    Column("response", Text, nullable=False)
)

APIMetadata = Table(
    'metadata', metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("api_name", String(200), unique=True),
    Column("api_version", String(200), unique=True),

)

APIDefinitions = Table(
    'definitions', metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("format", String(50), index=True),
    Column("version", String(50), index=True),
    Column("data", Text),
    Column("metadata_id",
           Integer,
           ForeignKey("metadata.id"),
           nullable=False)
)
