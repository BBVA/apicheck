from typing import Iterator

from sqlalchemy import and_
from apicheck.db import ProxyLogs, get_engine


async def get_proxy_logs(log_id: int) -> Iterator[dict]:
    """
    This method returns an iterator with the proxy logs structures.

    Each value returned has the format:

    {
        "request": {},
        "response": {}
    }

    """
    connection = await get_engine().connect()

    _logs = await connection.execute(ProxyLogs.select().where(and_(
        ProxyLogs.c.id
    )))

    async for log in await _logs.fetchall():
        yield {
            "request": log["request"],
            "response": log["response"]
        }

