from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sqlalchemy.orm as sa_orm

from typing import Optional
from contextvars import ContextVar, Token

# TODO: set DATABASE_URL
from config.env_config import settings
DATABASE_URL = settings.DATABASE_URL

REQUEST_ID_CTX_KEY = "session_id"

_request_id_ctx_var: ContextVar[Optional[str]] = ContextVar(REQUEST_ID_CTX_KEY, default=None)

def get_session_id() -> Optional[str]:
    return _request_id_ctx_var.get()

def set_session_id(value: str) -> Token:
    return _request_id_ctx_var.set(value)

def reset_session_id(token: Token):
    _request_id_ctx_var.reset(token)


class DatabaseConnector:
    def __init__(self):
        self.engine = create_engine(
            DATABASE_URL,
            pool_size=100,
            max_overflow=50,
            pool_timeout=10,
            pool_recycle=3600,
            pool_pre_ping=True,
        )
        self._Session = sessionmaker(bind=self.engine)
        self.session = self._make_scoped_session()

    def _make_scoped_session(self):
        """
        Create a :class:`sqlalchemy.orm.scoping.scoped_session` around the factory
        """
        factory = self._make_session_factory()
        return sa_orm.scoped_session(factory, get_session_id)

    def _make_session_factory(self):
        """
        Create the SQLAlchemy :class:`sqlalchemy.orm.sessionmaker` used by
        """
        return sa_orm.sessionmaker(bind=self.engine)


db = DatabaseConnector()