import dataclasses
from itertools import tee, groupby, chain
from typing import Iterable, Optional, Tuple, Callable, Set, List
from functools import partial, reduce
import json
import sys

from sqlalchemy import Column, ForeignKey, Integer, String, BigInteger, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()


class Log(Base):  # type: ignore
    __tablename__ = 'proxy_logs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    proxy_session_id = Column(Text, nullable=False)
    request = Column(Text, nullable=False)
    response = Column(Text, nullable=False)


class DataClassJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)


@dataclasses.dataclass
class ReqRes:
    key: int
    session_id: str
    request: dict
    response: dict


def parse_to_dataclass(log: Log) -> Optional[ReqRes]:
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


def collect_request_info(requests: List[ReqRes]) -> None:
    def _map_to_RequestInfo(reqres: ReqRes) -> RequestInfo:
        try:
            size = int(reqres.response["headers"]["Content-Length"])
        except:
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


@dataclasses.dataclass
class Step:
    session: str
    origin: str
    destination: str


def content_type(headers: dict) -> Optional[str]:
    if "Content-Type" in headers:
        return headers["Content-Type"]
    if "content-type" in headers:
        return headers["content-type"]
    return None


def response_content_type_filter(expected: str, reqres: ReqRes) -> bool:
    content = content_type(reqres.response["headers"])
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

        return [Step(session_id, origin, dest) for origin, dest in zip(just_path, just_path[1:])]

    by_session = [_proc_by_session(x) for x in logs]
    return list(reduce(chain, by_session, iter([])))


# not in use
def _get_nodes(steps: Iterable[Step]) -> Set[str]:
    def _add_to_set(acc: Set[str], step: Step) -> Set[str]:
        acc.add(step.origin)
        acc.add(step.destination)
        return acc

    return reduce(_add_to_set, steps, set())


def main():
    def _by_session(elm: ReqRes) -> str:
        return elm.session_id

    engine = create_engine('sqlite:///apicheck.db')
    Base.metadata.create_all(engine)

    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    res = [parse_to_dataclass(x) for x in session.query(Log).all()]

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
    resources = [(host, [x.request["path"] for x in reqres]) for host, reqres in by_host]
    info["resources"] = resources
    with open("data.json", "w") as out:
        json.dump(info, out, cls=DataClassJSONEncoder)


if __name__ == "__main__":
    main()
