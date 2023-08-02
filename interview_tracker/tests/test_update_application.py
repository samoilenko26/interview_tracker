from typing import Any, Awaitable, Callable, Dict

import pytest
from fastapi import FastAPI, status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from interview_tracker.db.data_access_layer.application import (
    get_application_by_application_id,
)
from interview_tracker.db.models.main_model import Application
from interview_tracker.web.authorization.testing import get_user_token_headers


@pytest.mark.anyio
async def test_update_application_okay(  # noqa: WPS218
    client: AsyncClient,
    dbsession: AsyncSession,
    fastapi_app: FastAPI,
    mock_application: Callable[..., Awaitable[Application]],
) -> None:
    # Create an initial application in the database
    application = await mock_application()

    # Prepare the update data
    update_data = {
        "company_name": "Updated Company",
        "status": "Interview Scheduled",
        "timelines": [
            {"name": "Phone Screen", "value": "2023-07-01"},
            {"name": "Onsite Interview", "value": "2023-07-02"},
        ],
    }

    # update application
    url = fastapi_app.url_path_for(
        "update_application",
        application_id=application.id,
    )
    headers = get_user_token_headers()
    response = await client.put(
        url=url,
        json=update_data,
        headers=headers,
    )
    # Need to commit changes. In runtime, it will be committed right after the method
    # is Done. But here another logic for committing changes. So, need to do it manually
    await dbsession.commit()
    await dbsession.close()

    assert response.status_code == status.HTTP_200_OK

    # Check if the application data is updated in the database
    updated_application = await get_application_by_application_id(
        application_id=application.id,
        session=dbsession,
    )
    assert updated_application is not None
    assert updated_application.company_name == update_data["company_name"]
    assert updated_application.status == update_data["status"]

    updated_timelines = updated_application.timelines
    assert len(updated_timelines) == len(update_data["timelines"])

    # Assert that the timelines are updated with the correct values
    for timeline, updated_data in zip(updated_timelines, update_data["timelines"]):
        assert timeline.name == updated_data["name"]  # type: ignore
        assert timeline.value == updated_data["value"]  # type: ignore

    # Assert that the others fields have correct, unchanged values
    assert updated_application.job_title == application.job_title
    assert updated_application.attractiveness_scale == application.attractiveness_scale
    assert updated_application.status_category == application.status_category
    assert updated_application.official_website == application.official_website
    assert updated_application.apply_icon == application.apply_icon
    assert updated_application.icon == application.icon
    assert updated_application.job_description_link == application.job_description_link
    assert updated_application.salary == application.salary
    assert updated_application.location == application.location
    assert updated_application.on_site_remote == application.on_site_remote
    assert updated_application.notes == application.notes


@pytest.mark.anyio
async def test_update_application_not_found(
    client: AsyncClient,
    dbsession: AsyncSession,
    fastapi_app: FastAPI,
    mock_application: Callable[..., Awaitable[Application]],
) -> None:
    application = await mock_application()

    update_data = {
        "company_name": "Updated Company",
    }

    # update application
    url = fastapi_app.url_path_for(
        "update_application",
        application_id=application.id + 1,
    )
    headers = get_user_token_headers()
    response = await client.put(
        url=url,
        json=update_data,
        headers=headers,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.anyio
async def test_update_application_no_access(
    client: AsyncClient,
    dbsession: AsyncSession,
    fastapi_app: FastAPI,
    mock_application: Callable[..., Awaitable[Application]],
) -> None:
    application = await mock_application(user_test_id="user_1")

    update_data = {
        "company_name": "Updated Company",
    }

    # update application
    url = fastapi_app.url_path_for(
        "update_application",
        application_id=application.id,
    )
    headers = get_user_token_headers(user_id="user_2")
    response = await client.put(
        url=url,
        json=update_data,
        headers=headers,
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.anyio
async def test_update_application_deletion_timelines(
    client: AsyncClient,
    dbsession: AsyncSession,
    fastapi_app: FastAPI,
    mock_application: Callable[..., Awaitable[Application]],
) -> None:
    application = await mock_application()

    # Prepare the update data
    update_data: Dict[str, Any] = {
        "timelines": [],
    }

    # update application
    url = fastapi_app.url_path_for(
        "update_application",
        application_id=application.id,
    )
    headers = get_user_token_headers()
    response = await client.put(
        url=url,
        json=update_data,
        headers=headers,
    )
    await dbsession.commit()
    await dbsession.close()

    assert response.status_code == status.HTTP_200_OK

    updated_application = await get_application_by_application_id(
        application_id=application.id,
        session=dbsession,
    )
    assert updated_application is not None
    updated_timelines = updated_application.timelines
    assert not updated_timelines  # len(updated_timelines) == 0


@pytest.mark.anyio
async def test_update_application_untouched_timelines(
    client: AsyncClient,
    dbsession: AsyncSession,
    fastapi_app: FastAPI,
    mock_application: Callable[..., Awaitable[Application]],
    application_request_body: Dict[str, Any],
) -> None:
    application = await mock_application()

    update_data = {
        "company_name": "Updated Company",
    }

    url = fastapi_app.url_path_for(
        "update_application",
        application_id=application.id,
    )
    headers = get_user_token_headers()
    response = await client.put(
        url=url,
        json=update_data,
        headers=headers,
    )
    await dbsession.commit()
    await dbsession.close()

    assert response.status_code == status.HTTP_200_OK

    updated_application = await get_application_by_application_id(
        application_id=application.id,
        session=dbsession,
    )
    assert updated_application is not None
    assert updated_application.company_name == update_data["company_name"]

    updated_timelines = updated_application.timelines
    assert len(updated_timelines) == len(application_request_body["timelines"])
    for timeline, original in zip(
        updated_timelines,
        application_request_body["timelines"],
    ):
        assert timeline.name == original["name"]
        assert timeline.value == original["value"]


@pytest.mark.anyio
async def test_update_application_validation_error1(
    client: AsyncClient,
    dbsession: AsyncSession,
    fastapi_app: FastAPI,
    mock_application: Callable[..., Awaitable[Application]],
) -> None:
    application = await mock_application()

    update_data = {
        "company_name": "",
    }

    url = fastapi_app.url_path_for(
        "update_application",
        application_id=application.id,
    )
    headers = get_user_token_headers()
    response = await client.put(
        url=url,
        json=update_data,
        headers=headers,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.anyio
async def test_update_application_validation_error2(
    client: AsyncClient,
    dbsession: AsyncSession,
    fastapi_app: FastAPI,
    mock_application: Callable[..., Awaitable[Application]],
) -> None:
    application = await mock_application()

    update_data = {
        "attractiveness_scale": 100,
    }

    url = fastapi_app.url_path_for(
        "update_application",
        application_id=application.id,
    )
    headers = get_user_token_headers()
    response = await client.put(
        url=url,
        json=update_data,
        headers=headers,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
