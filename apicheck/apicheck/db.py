import builtins

from sqlalchemy.schema import CreateTable
from sqlalchemy_aio import ASYNCIO_STRATEGY

from sqlalchemy import (
    Column, Integer, MetaData, Table, Text, create_engine, String)


def setup_db_engine(db_query_string: str = None):

    if not hasattr(builtins, "apicheck_db_engine"):
        builtins.apicheck_db_engine = create_engine(
            # In-memory sqlite database cannot be accessed from different
            # threads, use file.
            db_query_string, strategy=ASYNCIO_STRATEGY
        )


def get_engine():
    return builtins.apicheck_db_engine


async def create_database(engine=None):
    engine = engine or get_engine()

    await engine.execute(CreateTable(ProxyLogs))


metadata = MetaData()

ProxyLogs = Table(
    'proxy_logs', metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("proxy_session_id", String(40)),
    Column("request", Text, nullable=False),
    Column("response", Text, nullable=False),
)
