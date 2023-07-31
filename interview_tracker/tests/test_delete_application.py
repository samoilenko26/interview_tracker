from typing import Any, Awaitable, Callable, Dict

import pytest
from fastapi import FastAPI, status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from interview_tracker.db.data_access_layer.application import (
    get_application_by_application_id,
    get_timeline_by_id,
)
from interview_tracker.db.models.main_model import Application
from interview_tracker.web.api.applications.get.schemas.application import TimelineBase
from interview_tracker.web.authorization.testing import get_user_token_headers


@pytest.mark.anyio
async def test_delete_applications_okay(
    client: AsyncClient,
    dbsession: AsyncSession,
    fastapi_app: FastAPI,
    mock_application: Callable[..., Awaitable[Application]],
    application_request_body: Dict[str, Any],
) -> None:
    # create application
    application = await mock_application(user_test_id="user_1")

    # get the created application from DB
    row_application = await get_application_by_application_id(
        application_id=application.id,
        session=dbsession,
    )
    # get the created timelines from DB
    timelines = [
        TimelineBase(id=timeline.id, name=timeline.name, value=timeline.value)
        for timeline in row_application.timelines  # type: ignore
    ]

    # delete application
    url = fastapi_app.url_path_for(
        "delete_application",
        application_id=application.id,
    )
    headers = get_user_token_headers()
    response = await client.delete(
        url=url,
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK

    # check if the app is deleted
    deleted_application = await get_application_by_application_id(
        application_id=application.id,
        session=dbsession,
    )
    assert deleted_application is None

    # check if all timelines are deleted
    for timeline in timelines:
        deleted_timeline = await get_timeline_by_id(
            timeline_id=timeline.id,
            session=dbsession,
        )
        assert deleted_timeline is None


@pytest.mark.anyio
async def test_delete_applications_not_found(
    client: AsyncClient,
    dbsession: AsyncSession,
    fastapi_app: FastAPI,
    mock_application: Callable[..., Awaitable[Application]],
    application_request_body: Dict[str, Any],
) -> None:
    # create application
    application = await mock_application(user_test_id="user_1")

    # delete application
    url = fastapi_app.url_path_for(
        "delete_application",
        application_id=application.id + 1,
    )
    headers = get_user_token_headers()
    response = await client.delete(
        url=url,
        headers=headers,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.anyio
async def test_delete_applications_no_access(
    client: AsyncClient,
    dbsession: AsyncSession,
    fastapi_app: FastAPI,
    mock_application: Callable[..., Awaitable[Application]],
    application_request_body: Dict[str, Any],
) -> None:
    # create application
    application = await mock_application(user_test_id="user_1")

    # delete application
    url = fastapi_app.url_path_for(
        "delete_application",
        application_id=application.id,
    )
    headers = get_user_token_headers(user_id="user_2")
    response = await client.delete(
        url=url,
        headers=headers,
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
