import pytest

import asyncio
import os
from pathlib import Path

from alembic import command
from alembic.config import Config
from starlette.config import environ
from starlette.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database, drop_database

from teleologic import app, db

environ["TESTING"] = "True"


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
def database():
    url = str(db.DATABASE_URL)
    engine = create_engine(url)
    assert not database_exists(url), "Test database already exists. Aborting tests."
    create_database(url)  # Create the test database.

    db.metadata.create_all(engine)  # Create the tables.

    # FIXME (aliddell): this should be a fixture, but it doesn't seem to work
    query = db.users.insert().values(name="zoltan-kakler", authenticated=False)
    engine.execute(query)

    # FIXME (aliddell): we should run db migrations for all tests, but it
    # doesn't seem to work with asyncio tests

    # cwd = os.getcwd()
    # config_file = Path(__file__).parent.parent / "alembic.ini"
    # assert config_file.is_file()
    # os.chdir(config_file.parent)
    #
    # config = Config(config_file)  # Run the migrations.
    # command.upgrade(config, "head")
    #
    # os.chdir(cwd)
    # yield engine  # Run the tests.
    yield db.database  # Run the tests.
    drop_database(url)  # Drop the test database.
