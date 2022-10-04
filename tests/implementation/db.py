import abc
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


class IDBConfig(abc.ABC):
    @abc.abstractclassmethod
    def get_db_url(cls):
        pass

    @abc.abstractclassmethod
    def get_connect_args(cls):
        pass

    @classmethod
    def create_engine(cls):
        return create_engine(cls.get_db_url(), connect_args=cls.get_connect_args())


class PostgresDBConfig(IDBConfig):
    @classmethod
    def get_db_url(cls):
        return os.environ.get("DB_URL", "postgresql://postgres:postgres@localhost:5432/sqlalchemy-filters")

    @classmethod
    def get_connect_args(cls):
        return {"options": "-c timezone=utc"}


engine = PostgresDBConfig.create_engine()
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
