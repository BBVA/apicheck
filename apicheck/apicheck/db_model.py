from sqlalchemy import Column, ForeignKey, Integer, String, BigInteger, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()


class Log(Base):
    __tablename__ = 'log'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True, autoincrement=True)
    request = Column(Text, nullable=False)
    response = Column(Text, nullable=False)


# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
# engine = create_engine('sqlite:///apicheck.db')
#
# # Create all tables in the engine. This is equivalent to "Create Table"
# # statements in raw SQL.
# Base.metadata.create_all(engine)
#
# DBSession = sessionmaker()
# DBSession.bind = engine
# session = DBSession()
