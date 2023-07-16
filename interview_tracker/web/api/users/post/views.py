from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from interview_tracker.db.dependencies import get_db_session
from interview_tracker.db.models.main_model import User
from interview_tracker.web.api.users.schemas.base import Message
from interview_tracker.web.auth.dependencies import validate_token

auth_scheme = HTTPBearer()
router = APIRouter()


@router.post("/")
async def create_user(  # noqa: WPS210
    incoming_message: Message,
    auth_header: HTTPAuthorizationCredentials = Depends(
        auth_scheme,
    ),  # for FastApi docs
    token: Dict[str, Any] = Depends(validate_token),  # THE validation of token
    db: AsyncSession = Depends(get_db_session),
) -> Response:

    im_name = incoming_message.name.strip().lower().title()
    im_email = incoming_message.email.strip().lower()
    im_role = incoming_message.role

    user_query = select(User).where(User.email == im_email)
    user = await db.execute(user_query)
    if user.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with the same email already exists.",
        )
    new_user = User(
        name=im_name,
        email=im_email,
        role=im_role,
    )
    db.add(new_user)

    return Response(status_code=status.HTTP_201_CREATED)
