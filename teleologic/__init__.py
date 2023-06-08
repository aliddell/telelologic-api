from starlette.applications import Starlette

from .routes import routes
from .db import lifespan

app = Starlette(routes=routes, lifespan=lifespan)

VERSION = "0.0.1"
