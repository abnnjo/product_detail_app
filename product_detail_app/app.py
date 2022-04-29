from starlette.applications import Starlette
from starlette.responses import JSONResponse
from .config import DEBUG, DATABASE_URL, MIN_DB_CONN, MAX_DB_CONN
from .urls import url_patterns
from typing import AsyncGenerator
from gino import create_engine


class DatabaseMiddleware:
    def __init__(self, app, engine):
        self.app = app
        self.engine = engine

    async def __call__(self, scope, receive, send) -> None:
        scope["database"] = self.engine
        await self.app(scope, receive, send)


async def on_startup():
    engine = await create_engine(
        DATABASE_URL, min_size=MIN_DB_CONN, max_size=MAX_DB_CONN
    )
    return engine


async def LifeSpanMiddleware(app) -> AsyncGenerator:
    engine = await on_startup()
    app.add_middleware(DatabaseMiddleware, engine=engine)
    yield
    # await dbShutdown()


app = Starlette(debug=DEBUG, lifespan=LifeSpanMiddleware)


for url in url_patterns:
    app.add_route(url[0], url[1])


@app.exception_handler(404)
async def not_found(request, exc):
    """
    Exception Handler for 404 Page not Found
    :param request:
    :param exc:
    :return: Json Response
    """
    return JSONResponse(
        {"status": "error", "message": "Page not found"}, status_code=exc.status_code
    )


@app.exception_handler(405)
async def method_not_allowed(request, exc):
    """
    Exception Handler for 405 MEthod Not Allowed
    :param request:
    :param exc:
    :return: Json Response
    """
    return JSONResponse(
        {"status": "error", "message": "Method Not Allowed"}, status_code=405
    )


@app.exception_handler(500)
async def server_error(request, exc):
    """
    Exception Handler for 500 Internal Server Error
    :param request:
    :param exc:
    :return: Json Response
    """
    return JSONResponse(
        {"status": "error", "message": "Server error."},
        status_code=500,
    )
