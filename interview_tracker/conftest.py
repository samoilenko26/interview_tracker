from typing import Any, AsyncGenerator, Dict

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from interview_tracker.db.dependencies import get_db_session
from interview_tracker.db.utils import create_database, drop_database
from interview_tracker.settings import settings
from interview_tracker.web.application import get_app


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    """
    Backend for anyio pytest plugin.

    :return: backend name.
    """
    return "asyncio"


@pytest.fixture(scope="session")
async def _engine() -> AsyncGenerator[AsyncEngine, None]:
    """
    Create engine and databases.

    :yield: new engine.
    """
    from interview_tracker.db.meta import meta  # noqa: WPS433
    from interview_tracker.db.models import load_all_models  # noqa: WPS433

    load_all_models()

    await create_database()

    engine = create_async_engine(str(settings.db_url))
    async with engine.begin() as conn:
        await conn.run_sync(meta.create_all)

    try:
        yield engine
    finally:
        await engine.dispose()
        await drop_database()


@pytest.fixture
async def dbsession(
    _engine: AsyncEngine,
) -> AsyncGenerator[AsyncSession, None]:
    """
    Get session to database.

    Fixture that returns a SQLAlchemy session with a SAVEPOINT, and the rollback to it
    after the test completes.

    :param _engine: current engine.
    :yields: async session.
    """
    connection = await _engine.connect()
    trans = await connection.begin()

    session_maker = async_sessionmaker(
        connection,
        expire_on_commit=False,
    )
    session = session_maker()

    try:
        yield session
    finally:
        await session.close()
        await trans.rollback()
        await connection.close()


@pytest.fixture
def fastapi_app(
    dbsession: AsyncSession,
) -> FastAPI:
    """
    Fixture for creating FastAPI app.

    :return: fastapi app with mocked dependencies.
    """
    application = get_app()
    application.dependency_overrides[get_db_session] = lambda: dbsession
    return application  # noqa: WPS331


@pytest.fixture
async def client(
    fastapi_app: FastAPI,
    anyio_backend: Any,
) -> AsyncGenerator[AsyncClient, None]:
    """
    Fixture that creates client for requesting server.

    :param fastapi_app: the application.
    :yield: client for the app.
    """
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def application_request_body() -> Dict[str, Any]:
    return {
        "company_name": "Test Company",
        "job_title": "Test Job",
        "status": "Pending",
        "attractiveness_scale": 5,
        "status_category": "red",
        "official_website": "https://example.com",
        "apply_icon": True,
        "icon": "https://example.com/icon.ico",
        "job_description_link": "https://example.com/job_description",
        "salary": "100,000",
        "location": "Test City",
        "on_site_remote": "remote",
        "timelines": [
            {
                "name": "Interview 1",
                "value": "2023-07-21",
            },
            {
                "name": "Interview 2",
                "value": "2023-07-25",
            },
        ],
        "notes": "Test notes",
    }
