from dataclasses import dataclass
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
    key: int
    request: dict
    response: dict


def parse_to_dataclass(log: Log) -> ReqRes:
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


def sort_by_time(elm):
    return elm.request["timestamp_start"]


def main():
    engine = create_engine('sqlite:///apicheck.db')
    Base.metadata.create_all(engine)

    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    res = list(map(parse_to_dataclass, session.query(Log).all()))
    res.sort(key=sort_by_time)
    print(list(map(lambda x: x.key, res)))


if __name__ == "__main__":
    main()
