from typing import Awaitable, Callable

import pytest
from fastapi import FastAPI, status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from interview_tracker.web.authorization.testing import get_user_token_headers


@pytest.mark.anyio
async def test_get_applications_okay(
    client: AsyncClient,
    dbsession: AsyncSession,
    fastapi_app: FastAPI,
    mock_application: Callable[..., Awaitable[None]],
) -> None:
    exclude = ["notes"]
    await mock_application(exclude)
    url = fastapi_app.url_path_for("get_applications")
    headers = get_user_token_headers()
    response = await client.get(
        url=url,
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK
