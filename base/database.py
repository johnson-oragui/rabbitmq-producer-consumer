from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager

from config.settings import settings

DB_URL = settings.DB_URL

class Base(DeclarativeBase):
    pass

engine = create_engine(
    url=DB_URL,
    future=True,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=18000
)

def create_tables():
    Base.metadata.create_all(
        bind=engine,
    )

SessionMaker = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False
)

@contextmanager
def get_db():
    with SessionMaker().begin() as session:
        try:
            yield session
            session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()
