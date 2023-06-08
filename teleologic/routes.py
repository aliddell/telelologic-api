from starlette.applications import Starlette
from starlette.requests import HTTPConnection
from starlette.responses import Response, PlainTextResponse, JSONResponse
from starlette.routing import Route, Mount, WebSocketRoute
from starlette.staticfiles import StaticFiles

from .db import database, users


def homepage(_) -> Response:
    return PlainTextResponse("This is TeleoLogic.")


async def all_users(request: HTTPConnection) -> Response:
    query = users.select()
    results = await database.fetch_all(query)
    content = [
        {
            "name": result.name,
            "authenticated": result.authenticated
        }
        for result in results
    ]
    return JSONResponse(content)


async def single_user(request: HTTPConnection) -> Response:
    username = request.path_params["username"]
    query = users.select().where(users.c.name == username)
    result = await database.fetch_one(query)
    if result is None:
        return PlainTextResponse("Not Found", status_code=404)
    return PlainTextResponse("Hello, %s!" % result.name)


routes = [
    Route("/", endpoint=homepage, methods=["GET"]),
    Route("/users", endpoint=all_users, methods=["GET"]),
    Route("/users/{username}", endpoint=single_user, methods=["GET"]),
]
