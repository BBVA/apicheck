"""
This file contains python3.6+ syntax!
Feel free to import and use whatever new package you deem necessary.
"""
import sys
import json
import logging
import asyncio
import dataclasses

from collections import Counter
from functools import reduce, partial
from itertools import groupby, chain
from typing import Optional, List, Any, Iterable, Tuple, Set

from apicheck.db import ProxyLogs, get_engine, setup_db_engine
from apicheck.exceptions import APICheckException

from .config import RunningConfig

logger = logging.getLogger("apicheck")


@dataclasses.dataclass
class ReqRes:
    key: int
    session_id: str
    request: dict
    response: dict


@dataclasses.dataclass
class RequestInfo:
    key: str
    response_time: float
    size: int


@dataclasses.dataclass
class RequestStats:
    key: str = ""
    count: int = 0
    total: float = 0
    minimum: float = sys.float_info.max
    maximum: float = sys.float_info.min
    total_size: int = 0
    min_size: int = sys.maxsize
    max_size: int = -sys.maxsize - 1


@dataclasses.dataclass
class Step:
    session: str
    origin: str
    destination: str


class DataClassJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)


def try_to_extract_keys(target: dict, keys: List[str]) -> Any:
    for k in keys:
        if k in target:
            return target[k]
    return None


def collect_request_info(requests: List[ReqRes]) -> List[RequestStats]:
    def _map_to_RequestInfo(reqres: ReqRes) -> RequestInfo:
        content_length_fields = ["content-length", "Content-Length"]
        if reqres.request["method"] == "POST":
            size_field = try_to_extract_keys(
                reqres.request["headers"],
                content_length_fields
            )
        else:
            size_field = try_to_extract_keys(
                reqres.response["headers"],
                content_length_fields
            )

        if size_field:
            size = int(size_field)
        else:
            size = 0
        start = reqres.request["timestamp_start"]
        end = reqres.response["timestamp_end"]
        return RequestInfo(
            reqres.request["path"],
            (end - start) * 1000,
            size
        )

    def _by_key(reqres: RequestInfo) -> str:
        return reqres.key

    def _collect_stats(
            grouped_info: Tuple[RequestInfo, Iterable[RequestInfo]]
    ) -> RequestStats:
        _, current = grouped_info
        return reduce(_get_stats, current, RequestStats())

    def _get_stats(stats: RequestStats, info: RequestInfo) -> RequestStats:
        stats.key = info.key
        stats.count += 1
        stats.total += info.response_time
        stats.minimum = min(stats.minimum, info.response_time)
        stats.maximum = max(stats.maximum, info.response_time)
        stats.total_size += info.size
        stats.min_size = min(stats.min_size, info.size)
        stats.max_size = max(stats.max_size, info.size)
        return stats

    request_info = [_map_to_RequestInfo(x) for x in requests]
    request_info.sort(key=_by_key)
    by_endpoint = groupby(request_info, key=_by_key)
    return [_collect_stats(x) for x in by_endpoint]


def parse_to_dataclass(log: ProxyLogs) -> Optional[ReqRes]:
    try:
        return ReqRes(
            key=log.id,
            session_id=log.proxy_session_id,
            request=json.loads(log.request),
            response=json.loads(log.response)
        )
    except Exception as exc:
        if log:
            print("----------------------------------")
            print(exc)
            print(log.request)
            print(log.response)
    return None


def response_content_type_filter(expected: str, reqres: ReqRes) -> bool:
    content_type_fields = ["Content-Type", "content-type"]
    content = try_to_extract_keys(
        reqres.response["headers"],
        content_type_fields
    )
    if content:
        return expected in content
    return False


def content_type_flow(
        content_type: str,
        logs: List[Tuple[str, List[ReqRes]]]
) -> Iterable[Step]:
    target_content_filter = partial(response_content_type_filter, content_type)

    def _by_time(elm: ReqRes) -> int:
        return elm.request["timestamp_start"]

    def _proc_by_session(sess_log: Tuple[str, Iterable[ReqRes]]):
        session_id, log = sess_log
        log.sort(key=_by_time)
        just_path = [
            x.request["path"]
            for x in log
            if target_content_filter(x)
        ]

        return [Step(session_id, origin, dest) for origin, dest in
                zip(just_path, just_path[1:])]

    by_session = [_proc_by_session(x) for x in logs]
    return list(reduce(chain, by_session, iter([])))


# not in use
def _get_nodes(steps: Iterable[Step]) -> Set[str]:
    def _add_to_set(acc: Set[str], step: Step) -> Set[str]:
        acc.add(step.origin)
        acc.add(step.destination)
        return acc

    return reduce(_add_to_set, steps, set())


def headers_top(headers: List[Tuple[str, str]]) -> dict:
    def _by_key(x: Tuple[str, str]) -> str:
        return x[0]

    def _by_count(x: Tuple[str, int]) -> int:
        return x[1]

    def _max_counter(headers: List[str]) -> Tuple[str, int]:
        c = Counter(headers)
        limited = [(k, v) for k, v in c.items()]
        limited.sort(key=_by_count, reverse=True)
        return dict(limited[:6])

    headers.sort(key=_by_key)
    by_head = {
        h: _max_counter([x[1] for x in l])
        for h, l in groupby(headers, key=_by_key)
    }
    return by_head


async def get_proxy_entries() -> List or APICheckException:

    try:
        connection = await get_engine().connect()

        con_done = await connection.execute(ProxyLogs.select())
        results: list = await con_done.fetchall()

        return results
    except Exception as e:
        raise APICheckException(f"Error accessing to database: {e}")


def run(running_config: RunningConfig):
    def _by_session(elm: ReqRes) -> str:
        return elm.session_id

    # -------------------------------------------------------------------------
    # Setup database
    # -------------------------------------------------------------------------
    setup_db_engine(running_config.db_connection_string)

    # -------------------------------------------------------------------------
    # Getting Logs from database
    # -------------------------------------------------------------------------
    loop = asyncio.get_event_loop()
    logs = loop.run_until_complete(get_proxy_entries())

    res = [parse_to_dataclass(x) for x in logs]

    info = {}
    # response metrics
    metrics = list(collect_request_info(res))
    info["metrics"] = metrics

    # Flows
    res.sort(key=_by_session)
    grouped_sessions = groupby(res, key=_by_session)
    just_sessions = [(x, list(s)) for x, s in grouped_sessions]
    steps = {
        "html": content_type_flow("html", just_sessions),
        "json": content_type_flow("json", just_sessions)
    }
    info["steps"] = steps

    # Resources by host
    def _by_host(elm: ReqRes) -> str:
        return elm.request["host"]

    res.sort(key=_by_host)
    by_host = groupby(res, key=_by_host)
    resources = [(host, [x.request["path"] for x in reqres]) for host, reqres
                 in by_host]
    info["resources"] = resources

    # Headers Count
    info["headers_count"] = {
        "request": Counter([h for r in res for h in r.request["headers"]]),
        "response": Counter([h for r in res for h in r.response["headers"]])
    }

    # Headers top
    info["headers_top"] = {
        "request": headers_top(
            [h for r in res for h in r.request["headers"].items()]),
        "response": headers_top(
            [h for r in res for h in r.response["headers"].items()])
    }

    with open(running_config.fout, "w") as out:
        json.dump(info, out, cls=DataClassJSONEncoder)
