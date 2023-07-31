from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from interview_tracker.db.data_access_layer.application import (
    delete_application as dal_delete_application,
)
from interview_tracker.db.data_access_layer.application import (
    get_application_by_application_id,
)
from interview_tracker.db.data_access_layer.user import get_user_by_sub
from interview_tracker.db.dependencies import get_db_session
from interview_tracker.web.authorization.dependencies import authorization
from interview_tracker.web.authorization.json_web_token import JsonWebToken

auth_scheme = HTTPBearer()
router = APIRouter()


@router.delete("/{application_id}")
async def delete_application(
    application_id: int,
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
    jwt_token: JsonWebToken = Depends(authorization),
    session: AsyncSession = Depends(get_db_session),
) -> Response:

    user = await get_user_by_sub(session, jwt_token.subject)
    application = await get_application_by_application_id(
        application_id=application_id,
        session=session,
    )
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )

    if application.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No access to the application",
        )

    await dal_delete_application(application=application, session=session)

    return Response(status_code=status.HTTP_200_OK)
