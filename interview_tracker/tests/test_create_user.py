import pytest
from fastapi import FastAPI, status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from interview_tracker.web.authorization.testing import get_user_token_headers


@pytest.mark.anyio
async def test_create_okay(
    client: AsyncClient,
    dbsession: AsyncSession,
    fastapi_app: FastAPI,
) -> None:

    url = fastapi_app.url_path_for("create_user")
    headers = get_user_token_headers()
    response = await client.get(url=url, headers=headers)

    # Assert response status code
    assert response.status_code == status.HTTP_201_CREATED
