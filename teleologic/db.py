import contextlib

import databases
import sqlalchemy
from starlette.config import Config

config = Config(".env")
DATABASE_URL = config("DATABASE_URL")

# Database table definitions.
metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("authenticated", sqlalchemy.Boolean)
)

database = databases.Database(DATABASE_URL)


@contextlib.asynccontextmanager
async def lifespan(app):
    await database.connect()
    yield
    await database.disconnect()
