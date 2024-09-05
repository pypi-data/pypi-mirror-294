import sqlite3

from . import query as q  # noqa: F401
from . import sqla as sqla
from . import types as types
from .base_model import BaseModel as BaseModel


def get_metadata():
    return BaseModel.metadata


@sqla.event.listens_for(sqla.Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """Enable sqlite `foreign_keys` feature upon connecting."""
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


@sqla.compiles(sqla.Identity, "sqlite")
def visit_identity(element, compiler, **kwargs):
    """There is a bug(?) with `Identity`, alembic and sqlite,
    requiring us to omit `Identity` objects from the migrations."""
    return sqla.text("")
