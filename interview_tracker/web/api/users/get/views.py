from fastapi import APIRouter, Depends, Response, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from interview_tracker.db.data_access_layer.user import get_user_by_sub
from interview_tracker.db.dependencies import get_db_session
from interview_tracker.web.authorization.dependencies import authorization
from interview_tracker.web.authorization.json_web_token import JsonWebToken

auth_scheme = HTTPBearer()
router = APIRouter()


@router.get("/")
async def create_user(  # noqa: WPS210
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
    jwt_token: JsonWebToken = Depends(authorization),
    session: AsyncSession = Depends(get_db_session),
) -> Response:
    await get_user_by_sub(session, jwt_token.subject)
    return Response(status_code=status.HTTP_201_CREATED)
