import datetime
import uuid

from sqlalchemy import (
    create_engine, Table, Boolean, Column, DateTime, ForeignKey, Integer,
    String, JSON, and_, or_, not_
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session, contains_eager, lazyload, joinedload,selectinload
from sqlalchemy_utils import UUIDType, EmailType
from sqlalchemy.sql.expression import bindparam

from zix.server.logging import get_logger

logger = get_logger(logger_name=__name__)


engine = None
SessionLocal = None

def get_engine(database_url, connect_args, engine_kwargs):
    global SessionLocal
    global DBEngine
    DBEngine = create_engine(
        database_url,
        connect_args=connect_args,
        **engine_kwargs,
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=DBEngine)
    return DBEngine


def get_db():
    global SessionLocal
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Base(object):
    def __tablename__(self):
        return self.__name__.lower()

    # Use id (primary key) for internal reference instead of uid
    # for better performance and sorting
    id = Column(Integer, primary_key=True)

    # Use uid as a public identifier
    # Note: do binary=True, native=True on Postgres for better performance
    uid = Column(UUIDType(binary=False, native=False), default=uuid.uuid4)

    created_at = Column(
            DateTime,
            default=datetime.datetime.utcnow
            )

    update_at = Column(
            DateTime,
            default=datetime.datetime.utcnow,
            onupdate=datetime.datetime.utcnow,
            )

Base = declarative_base(cls=Base)
