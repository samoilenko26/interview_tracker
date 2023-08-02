import json
from typing import Awaitable, Callable

import pytest
from fastapi import FastAPI, status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from interview_tracker.db.models.main_model import Application
from interview_tracker.web.authorization.testing import get_user_token_headers


@pytest.mark.anyio
async def test_get_applications_okay(  # noqa: WPS218
    client: AsyncClient,
    dbsession: AsyncSession,
    fastapi_app: FastAPI,
    mock_application: Callable[..., Awaitable[Application]],
) -> None:
    application = await mock_application(user_test_id="user_1")
    url = fastapi_app.url_path_for(
        "get_application_by_id",
        application_id=application.id,
    )
    headers = get_user_token_headers()
    response = await client.get(
        url=url,
        headers=headers,
    )
    response_data = json.loads(response.content)
    app_in_response = response_data["application"]

    assert app_in_response["company_name"] == application.company_name
    assert app_in_response["job_title"] == application.job_title
    assert app_in_response["status"] == application.status
    assert app_in_response["attractiveness_scale"] == application.attractiveness_scale
    assert app_in_response["status_category"] == application.status_category
    assert app_in_response["official_website"] == application.official_website
    assert app_in_response["apply_icon"] == application.apply_icon
    assert app_in_response["icon"] == application.icon
    assert app_in_response["job_description_link"] == application.job_description_link
    assert app_in_response["salary"] == application.salary
    assert app_in_response["location"] == application.location
    assert app_in_response["on_site_remote"] == application.on_site_remote
    assert app_in_response["notes"] == application.notes
    assert app_in_response["timelines"] == [
        {"id": tl.id, "name": tl.name, "value": tl.value}
        for tl in application.timelines
    ]


@pytest.mark.anyio
async def test_get_applications_no_access(
    client: AsyncClient,
    dbsession: AsyncSession,
    fastapi_app: FastAPI,
    mock_application: Callable[..., Awaitable[Application]],
) -> None:
    application = await mock_application(user_test_id="user_1")
    url = fastapi_app.url_path_for(
        "get_application_by_id",
        application_id=application.id,
    )
    headers = get_user_token_headers(user_id="user_2")
    response = await client.get(
        url=url,
        headers=headers,
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.anyio
async def test_get_applications_not_found(
    client: AsyncClient,
    dbsession: AsyncSession,
    fastapi_app: FastAPI,
    mock_application: Callable[..., Awaitable[Application]],
) -> None:
    application = await mock_application(user_test_id="user_1")
    url = fastapi_app.url_path_for(
        "get_application_by_id",
        application_id=application.id + 1,
    )
    headers = get_user_token_headers(user_id="user_1")
    response = await client.get(
        url=url,
        headers=headers,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
