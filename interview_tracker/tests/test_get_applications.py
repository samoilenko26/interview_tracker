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
    url = fastapi_app.url_path_for("get_applications")
    headers = get_user_token_headers()
    response = await client.get(
        url=url,
        headers=headers,
    )
    response_data = json.loads(response.content)
    app = response_data["applications"][0]

    assert response.status_code == status.HTTP_200_OK
    assert app["company_name"] == application.company_name
    assert app["job_title"] == application.job_title
    assert app["attractiveness_scale"] == application.attractiveness_scale
    assert app["status"] == application.status
    assert app["status_category"] == application.status_category


@pytest.mark.anyio
async def test_get_applications_okay_two_users(  # noqa: WPS218
    client: AsyncClient,
    dbsession: AsyncSession,
    fastapi_app: FastAPI,
    mock_application: Callable[..., Awaitable[Application]],
) -> None:
    app1 = await mock_application(user_test_id="user_1", company_name="Test Company 1")
    app2 = await mock_application(user_test_id="user_2", company_name="Test Company 2")
    url = fastapi_app.url_path_for("get_applications")
    headers_user1 = get_user_token_headers(user_id="user_1")
    headers_user2 = get_user_token_headers(user_id="user_2")

    response = await client.get(
        url=url,
        headers=headers_user1,
    )
    assert response.status_code == status.HTTP_200_OK
    response_data = json.loads(response.content)
    assert len(response_data["applications"]) == 1
    app = response_data["applications"][0]
    assert app["company_name"] == app1.company_name

    response = await client.get(
        url=url,
        headers=headers_user2,
    )
    assert response.status_code == status.HTTP_200_OK
    response_data = json.loads(response.content)
    assert len(response_data["applications"]) == 1
    app = response_data["applications"][0]
    assert app["company_name"] == app2.company_name


@pytest.mark.anyio
async def test_get_applications_not_found(
    client: AsyncClient,
    dbsession: AsyncSession,
    fastapi_app: FastAPI,
    mock_application: Callable[..., Awaitable[Application]],
) -> None:
    url = fastapi_app.url_path_for("get_applications")
    headers = get_user_token_headers()
    response = await client.get(
        url=url,
        headers=headers,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
