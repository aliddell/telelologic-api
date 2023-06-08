import pytest
from httpx import AsyncClient

from teleologic import app
from teleologic.db import users


@pytest.fixture(scope="module")
def mock_user(database):
    query = users.insert().values(name="zoltan-kakler", authenticated=False)
    database.execute(query)
    yield


async def test_homepage():
    async with AsyncClient(app=app, base_url="http://localhost") as client:
        response = await client.get("/")
        assert 200 == response.status_code

        assert response.content.decode() == "This is TeleoLogic."


@pytest.mark.parametrize(
    ("username", "code"),
    [
        ("foo", 404),
        ("bar", 404),
        ("zoltan-kakler", 200),
    ])
async def test_user_page(database, username, code):
    async with AsyncClient(app=app, base_url="http://localhost") as client:
        response = await client.get(f"/users/{username}")
        assert code == response.status_code

        if 200 == code:
            assert response.content.decode() == f"Hello, {username}!"
        elif 404 == code:
            assert response.content.decode() == "Not Found"


async def test_all_users_endpoint(database):
    async with AsyncClient(app=app, base_url="http://localhost") as client:
        response = await client.get(f"/users")
        assert 200 == response.status_code

        assert {"name": "zoltan-kakler", "authenticated": False} in response.json()
