from dataclasses import dataclass
from itertools import tee
from typing import Iterable
from functools import partial
import json

from sqlalchemy import Column, ForeignKey, Integer, String, BigInteger, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()


class Log(Base):
    __tablename__ = 'proxy_logs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    request = Column(Text, nullable=False)
    response = Column(Text, nullable=False)


@dataclass
class ReqRes:
    key :int
    request :dict
    response :dict


def parse_to_dataclass(log :Log) -> ReqRes:
    try:
        return ReqRes(
            key=log.id,
            request=json.loads(log.request),
            response=json.loads(log.response)
        )
    except Exception as exc:
        if log:
            print("----------------------------------")
            print(exc)
            print(log.request)
            print(log.response)


def content_type(headers :dict) -> str:
    if "Content-Type" in headers:
        return headers["Content-Type"]
    if "content-type" in headers:
        return headers["content-type"]

def response_content_type_filter(expected :str, reqres :ReqRes) -> bool:
    content = content_type(reqres.response["headers"])
    return expected in content


@dataclass
class Step:
    origin :str
    destination :str


def content_type_flow(content_type :str, logs :Iterable[ReqRes])->Iterable[Step]:
    only_html = partial(response_content_type_filter, content_type)
    just_path = map(lambda x: x.request["path"], filter(only_html, logs))
    
    origin, destination = tee(just_path)
    next(destination)

    origin_destination = zip(origin, destination)
    return map(lambda x: Step(x[0], x[1]), origin_destination)


def main():
    def _sort_by_time(elm :ReqRes) -> int:
        return elm.request["timestamp_start"]

    engine = create_engine('sqlite:///apicheck.db')
    Base.metadata.create_all(engine)

    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    res = list(map(parse_to_dataclass, session.query(Log).all()))
    res.sort(key=_sort_by_time)

    processes = [
        partial(content_type_flow, "html")
    ]
    analysis = map(lambda x: x(res), processes)
    print(list(analysis))


if __name__ == "__main__":
    main()
