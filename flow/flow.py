from dataclasses import dataclass
from itertools import tee, groupby, chain
from typing import Iterable, Optional, Tuple
from functools import partial, reduce
import json

from sqlalchemy import Column, ForeignKey, Integer, String, BigInteger, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()


class Log(Base):# type: ignore
    __tablename__ = 'proxy_logs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    proxy_session_id = Column(Text, nullable=False)
    request = Column(Text, nullable=False)
    response = Column(Text, nullable=False)


@dataclass
class ReqRes:
    key :int
    session_id :str
    request :dict
    response :dict


def parse_to_dataclass(log :Log) -> Optional[ReqRes]:
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


def content_type(headers :dict) -> Optional[str]:
    if "Content-Type" in headers:
        return headers["Content-Type"]
    if "content-type" in headers:
        return headers["content-type"]
    return None

def response_content_type_filter(expected :str, reqres :ReqRes) -> bool:
    content = content_type(reqres.response["headers"])
    if content:
        return expected in content
    return False


@dataclass
class Step:
    origin :str
    destination :str


def content_type_flow(
        content_type :str, 
        logs :Iterable[Tuple[str, Iterable[ReqRes]]]
    ) -> Iterable[Step]:
    target_content_filter = partial(response_content_type_filter, content_type)
    def _by_time(elm :ReqRes) -> int:
        return elm.request["timestamp_start"]

    def _proc_by_session(sess_log :Tuple[str, Iterable[ReqRes]]):
        session, log = sess_log
        target_content = list(filter(target_content_filter, log))
        target_content.sort(key=_by_time)
        just_path = map(lambda x: x.request["path"], target_content)
        origin, destination = tee(just_path)
        next(destination)

        origin_destination = zip(origin, destination)
        return map(lambda x: Step(x[0], x[1]), origin_destination)

    by_session = map(_proc_by_session, logs)
    return reduce(chain, by_session, iter([]))
    


def main():
    def _by_session(elm :ReqRes) -> str:
        return elm.session_id

    engine = create_engine('sqlite:///apicheck.db')
    Base.metadata.create_all(engine)

    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    res = list(map(parse_to_dataclass, session.query(Log).all()))
    res.sort(key=_by_session)
    grouped_sessions :Tuple[str, Iterable[ReqRes]] = groupby(res, key=_by_session)

    processes = [
        partial(content_type_flow, "html"),
        partial(content_type_flow, "json")
    ]

    analysis = map(lambda x: x[0](x[1]), zip(processes, tee(grouped_sessions)))
    for x in analysis:
        print(list(x))


if __name__ == "__main__":
    main()
