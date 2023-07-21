import json

import pytest
from fastapi import FastAPI, status
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from interview_tracker.db.models.application import Application, Timeline
from interview_tracker.web.api.applications.schemas.application import (
    ApplicationCreateMessage,
)
from interview_tracker.web.authorization.testing import get_user_token_headers


@pytest.mark.anyio
async def test_create_application_okay(  # noqa: WPS218
    client: AsyncClient,
    dbsession: AsyncSession,
    fastapi_app: FastAPI,
    application_request_body: ApplicationCreateMessage,
) -> None:
    request_body = application_request_body.dict()
    url = fastapi_app.url_path_for("create_application")
    headers = get_user_token_headers()
    response = await client.post(url=url, headers=headers, json=request_body)

    assert response.status_code == status.HTTP_201_CREATED

    # Retrieve the created application from the database
    application = await dbsession.execute(
        select(Application).filter_by(
            company_name=application_request_body.company_name,
            job_title=application_request_body.job_title,
        ),
    )
    created_application = application.scalar()

    assert created_application is not None
    assert created_application.company_name == application_request_body.company_name
    assert created_application.job_title == application_request_body.job_title
    assert created_application.status == application_request_body.status
    assert (
        created_application.attractiveness_scale
        == application_request_body.attractiveness_scale
    )
    assert (
        created_application.status_category == application_request_body.status_category
    )
    assert (
        created_application.official_website
        == application_request_body.official_website
    )
    assert created_application.apply_icon == application_request_body.apply_icon
    assert (
        created_application.job_description_link
        == application_request_body.job_description_link
    )
    assert created_application.salary == application_request_body.salary
    assert created_application.location == application_request_body.location
    assert created_application.on_site_remote == application_request_body.on_site_remote
    assert created_application.notes == application_request_body.notes

    # Retrieve the timelines associated with the created application
    timelines = await dbsession.execute(
        select(Timeline).filter_by(application_id=created_application.id),
    )
    created_timelines = timelines.scalars().all()
    requested_timelines = application_request_body.timelines or []

    assert len(created_timelines) == len(requested_timelines)
    for created_timeline, requested_timeline in zip(  # noqa: WPS352
        created_timelines,
        requested_timelines,
    ):
        assert created_timeline.name == requested_timeline.name
        assert created_timeline.value == requested_timeline.value


@pytest.mark.anyio
async def test_create_application_company_name_not_valid(  # noqa:WPS118
    client: AsyncClient,
    dbsession: AsyncSession,
    fastapi_app: FastAPI,
    application_request_body: ApplicationCreateMessage,
) -> None:

    application_request_body.company_name = ""
    request_body = application_request_body.dict()
    url = fastapi_app.url_path_for("create_application")
    headers = get_user_token_headers()
    response = await client.post(url=url, headers=headers, json=request_body)
    response_data = json.loads(response.content)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response_data["detail"] == [
        {
            "loc": ["body", "company_name"],
            "msg": "company_name cannot be less 1 characters",
            "type": "value_error",
        },
    ]


@pytest.mark.anyio
async def test_create_application_job_title_not_valid(
    client: AsyncClient,
    dbsession: AsyncSession,
    fastapi_app: FastAPI,
    application_request_body: ApplicationCreateMessage,
) -> None:

    application_request_body.job_title = ""
    request_body = application_request_body.dict()
    url = fastapi_app.url_path_for("create_application")
    headers = get_user_token_headers()
    response = await client.post(url=url, headers=headers, json=request_body)
    response_data = json.loads(response.content)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response_data["detail"] == [
        {
            "loc": ["body", "job_title"],
            "msg": "job_title cannot be less 1 characters",
            "type": "value_error",
        },
    ]


@pytest.mark.anyio
async def test_create_application_status_not_valid(
    client: AsyncClient,
    dbsession: AsyncSession,
    fastapi_app: FastAPI,
    application_request_body: ApplicationCreateMessage,
) -> None:

    application_request_body.status = ""
    request_body = application_request_body.dict()
    url = fastapi_app.url_path_for("create_application")
    headers = get_user_token_headers()
    response = await client.post(url=url, headers=headers, json=request_body)
    response_data = json.loads(response.content)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response_data["detail"] == [
        {
            "loc": ["body", "status"],
            "msg": "status cannot be less 1 characters",
            "type": "value_error",
        },
    ]


@pytest.mark.anyio
async def test_create_application_attractiveness_scale_not_valid(  # noqa:WPS118
    client: AsyncClient,
    dbsession: AsyncSession,
    fastapi_app: FastAPI,
    application_request_body: ApplicationCreateMessage,
) -> None:

    application_request_body.attractiveness_scale = 100
    request_body = application_request_body.dict()
    url = fastapi_app.url_path_for("create_application")
    headers = get_user_token_headers()
    response = await client.post(url=url, headers=headers, json=request_body)
    response_data = json.loads(response.content)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response_data["detail"] == [
        {
            "loc": ["body", "attractiveness_scale"],
            "msg": "attractiveness_scale must be in range 1..5",
            "type": "value_error",
        },
    ]


@pytest.mark.anyio
async def test_create_application_status_category_not_valid(  # noqa:WPS118
    client: AsyncClient,
    dbsession: AsyncSession,
    fastapi_app: FastAPI,
    application_request_body: ApplicationCreateMessage,
) -> None:

    application_request_body.status_category = "hello"  # type: ignore
    request_body = application_request_body.dict()
    url = fastapi_app.url_path_for("create_application")
    headers = get_user_token_headers()
    response = await client.post(url=url, headers=headers, json=request_body)
    response_data = json.loads(response.content)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response_data["detail"][0]["type"] == "type_error.enum"
