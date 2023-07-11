from typing import AsyncGenerator

import pytest
from fastapi import FastAPI, status
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from interview_tracker.db.models.main_model import User


@pytest.mark.anyio
async def test_create_okay(
    client: AsyncClient,
    dbsession: AsyncGenerator[AsyncSession, None],
    fastapi_app: FastAPI,
) -> None:

    user_name = "Anton Maximov"
    user_email = "anton@maximov.com"
    user_role = "user"

    # Execute request
    data = {
        "name": user_name,
        "email": user_email,
        "role": user_role,
    }
    url = fastapi_app.url_path_for("create_user")
    response = await client.post(url=url, json=data)

    # Assert response status code
    assert response.status_code == status.HTTP_201_CREATED
    query = select(User).where(User.email == user_email)
    result = await dbsession.execute(query)  # type: ignore
    assert result.scalar_one_or_none() is not None


@pytest.mark.anyio
async def test_create_user_with_the_same_email(
    client: AsyncClient,
    dbsession: AsyncGenerator[AsyncSession, None],
    fastapi_app: FastAPI,
) -> None:

    # Init database
    user_id = 1
    user_name = "Anton Maximov"
    user_email = "anton@maximov.com"
    user_role = "user"
    mock_user = User(
        id=user_id,
        name=user_name,
        email=user_email,
        role=user_role,
    )
    dbsession.add(mock_user)  # type: ignore
    await dbsession.commit()  # type: ignore

    # Execute request
    data = {
        "name": user_name,
        "email": user_email,
        "role": user_role,
    }
    url = fastapi_app.url_path_for("create_user")
    response = await client.post(url=url, json=data)

    # Assert response status code
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Assert response body
    assert response.json() == {
        "detail": "User with the same email already exists.",
    }


@pytest.mark.anyio
async def test_create_incorrect_name_first_letter(
    client: AsyncClient,
    dbsession: AsyncGenerator[AsyncSession, None],
    fastapi_app: FastAPI,
) -> None:

    user_name = "999Anton Maximov"
    user_email = "anton@maximov.com"
    user_role = "user"

    # Execute request
    data = {
        "name": user_name,
        "email": user_email,
        "role": user_role,
    }
    url = fastapi_app.url_path_for("create_user")
    response = await client.post(url=url, json=data)

    # Assert response status code
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.anyio
async def test_create_incorrect_name_len(
    client: AsyncClient,
    dbsession: AsyncGenerator[AsyncSession, None],
    fastapi_app: FastAPI,
) -> None:

    user_name = "Anton Maximokfmrlvkwerlvkwmerlkmvwelkrmvklsev"
    user_email = "anton@maximov.com"
    user_role = "user"

    # Execute request
    data = {
        "name": user_name,
        "email": user_email,
        "role": user_role,
    }
    url = fastapi_app.url_path_for("create_user")
    response = await client.post(url=url, json=data)

    # Assert response status code
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.anyio
async def test_create_incorrect_role(
    client: AsyncClient,
    dbsession: AsyncGenerator[AsyncSession, None],
    fastapi_app: FastAPI,
) -> None:
    user_name = "Anton Maximov"
    user_email = "anton@maximov.com"
    user_role = "user123"

    # Execute request
    data = {
        "name": user_name,
        "email": user_email,
        "role": user_role,
    }
    url = fastapi_app.url_path_for("create_user")
    response = await client.post(url=url, json=data)

    # Assert response status code
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.anyio
async def test_create_incorrect_email(
    client: AsyncClient,
    dbsession: AsyncGenerator[AsyncSession, None],
    fastapi_app: FastAPI,
) -> None:

    user_name = "Anton Maximov"
    user_email = "antonmaximovcom"
    user_role = "user"

    # Execute request
    data = {
        "name": user_name,
        "email": user_email,
        "role": user_role,
    }
    url = fastapi_app.url_path_for("create_user")
    response = await client.post(url=url, json=data)

    # Assert response status code
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.anyio
async def test_create_corrector_name(
    client: AsyncClient,
    dbsession: AsyncGenerator[AsyncSession, None],
    fastapi_app: FastAPI,
) -> None:

    user_name = "  anton maximov  "
    user_email = "anton@maximov.com"
    user_role = "user"

    # Execute request
    data = {
        "name": user_name,
        "email": user_email,
        "role": user_role,
    }
    url = fastapi_app.url_path_for("create_user")
    await client.post(url=url, json=data)
    query = select(User).where(User.email == user_email)
    result = await dbsession.execute(query)  # type: ignore
    user_object = result.scalar_one_or_none()

    assert user_object.name == "Anton Maximov"


@pytest.mark.anyio
async def test_create_corrector_email(
    client: AsyncClient,
    dbsession: AsyncGenerator[AsyncSession, None],
    fastapi_app: FastAPI,
) -> None:

    user_name = "Anton Maximov"
    user_email = "    ANTON@maximov.com   "
    user_role = "user"

    # Execute request
    data = {
        "name": user_name,
        "email": user_email,
        "role": user_role,
    }
    url = fastapi_app.url_path_for("create_user")
    await client.post(url=url, json=data)
    query = select(User).where(User.name == user_name)
    result = await dbsession.execute(query)  # type: ignore
    user_object = result.scalar_one_or_none()
    assert user_object.email == "anton@maximov.com"
