import secure
from typing import Awaitable, Callable
from fastapi.responses import JSONResponse
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from starlette.exceptions import HTTPException as StarletteHTTPException
from interview_tracker.db.meta import meta
from interview_tracker.db.models import load_all_models
from interview_tracker.settings import settings


def _setup_db(app: FastAPI) -> None:  # pragma: no cover
    """
    Creates connection to the database.

    This function creates SQLAlchemy engine instance,
    session_factory for creating sessions
    and stores them in the application's state property.

    :param app: fastAPI application.
    """
    engine = create_async_engine(str(settings.db_url), echo=settings.db_echo)
    session_factory = async_sessionmaker(
        engine,
        expire_on_commit=False,
    )
    app.state.db_engine = engine
    app.state.db_session_factory = session_factory


async def _create_tables() -> None:  # pragma: no cover
    """Populates tables in the database."""
    load_all_models()
    engine = create_async_engine(str(settings.db_url))
    async with engine.begin() as connection:
        await connection.run_sync(meta.create_all)
    await engine.dispose()


def register_startup_event(
    app: FastAPI,
) -> Callable[[], Awaitable[None]]:  # pragma: no cover
    """
    Actions to run on application startup.

    This function uses fastAPI app to store data
    in the state, such as db_engine.

    :param app: the fastAPI application.
    :return: function that actually performs actions.
    """

    @app.on_event("startup")
    async def _startup() -> None:  # noqa: WPS430
        _setup_db(app)
        await _create_tables()
        pass  # noqa: WPS420

    return _startup


def register_shutdown_event(
    app: FastAPI,
) -> Callable[[], Awaitable[None]]:  # pragma: no cover
    """
    Actions to run on application's shutdown.

    :param app: fastAPI application.
    :return: function that actually performs actions.
    """

    @app.on_event("shutdown")
    async def _shutdown() -> None:  # noqa: WPS430
        await app.state.db_engine.dispose()

        pass  # noqa: WPS420

    return _shutdown


def register_middleware(
    app: FastAPI,
) -> Callable[[], Awaitable[None]]:  # pragma: no cover
    """
    :param app: fastAPI application.
    :return: function that actually performs actions.
    """

    csp = secure.ContentSecurityPolicy().default_src("'self'").frame_ancestors("'none'")
    hsts = secure.StrictTransportSecurity().max_age(31536000).include_subdomains()
    referrer = secure.ReferrerPolicy().no_referrer()
    cache_value = secure.CacheControl().no_cache().no_store()\
        .max_age(0).must_revalidate()
    x_frame_options = secure.XFrameOptions().deny()

    secure_headers = secure.Secure(

        hsts=hsts,
        referrer=referrer,
        cache=cache_value,
        xfo=x_frame_options,
    )

    @app.middleware("http")
    async def _set_secure_headers(request, call_next):
        response = await call_next(request)
        secure_headers.framework.fastapi(response)
        return response

    return _set_secure_headers


def register_exception_handler(
    app: FastAPI,
) -> Callable[[], Awaitable[None]]:  # pragma: no cover
    """
    :param app: fastAPI application.
    :return: function that actually performs actions.
    """

    @app.exception_handler(StarletteHTTPException)
    async def _http_exception_handler(request, exc):
        message = str(exc.detail)

        return JSONResponse({"message": message}, status_code=exc.status_code)

    return _http_exception_handler
