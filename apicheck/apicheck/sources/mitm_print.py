from sqlalchemy import Column, ForeignKey, Integer, String, BigInteger, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from sqlalchemy import create_engine

from apicheck.db_model import Log, Base


class AddHeader:

    def __init__(self):
        engine = create_engine('sqlite:///apicheck.db')

        # Create all tables in the engine. This is equivalent to "Create Table"
        # statements in raw SQL.
        Base.metadata.create_all(engine)

        self.session = scoped_session(sessionmaker(autocommit=False,
                                                   autoflush=False,
                                                   bind=engine))

    def response(self, flow):
        print(self.save(flow.request.data))
        print(self.save(flow.response.data))

    def plain(self, data: dict) -> dict:

        ret = {}
        for x, y in data.items():
            if x == "headers" or x.startswith("_"):
                continue

            try:
                ret[x] = y.decode("UTF-8")
            except (AttributeError, UnicodeDecodeError):
                ret[x] = y

        ret["headers"] = {
            x.decode("UTF-8"): y.decode("UTF-8")
            for x, y in data["headers"].fields
        }

        return ret

    def save(self, data: dict):
        d = self.plain(data.__dict__)
        l = Log(id=None, request=str(d), response=str(d))

        self.session.add(l)
        self.session.commit()

    def done(self):
        self.session.commit()


addons = [
    AddHeader()
]
