from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from interview_tracker.db.data_access_layer.application import (
    get_all_applications_by_user_id,
    get_application_by_application_id,
)
from interview_tracker.db.data_access_layer.user import get_user_by_sub
from interview_tracker.db.dependencies import get_db_session
from interview_tracker.web.api.applications.get.schemas.application import (
    ApplicationResponse,
    ApplicationsResponse,
    make_base_info_application,
    make_full_info_application,
)
from interview_tracker.web.authorization.dependencies import authorization
from interview_tracker.web.authorization.json_web_token import JsonWebToken

auth_scheme = HTTPBearer()
router = APIRouter()


@router.get("/", response_model=ApplicationsResponse)
async def get_applications(
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
    jwt_token: JsonWebToken = Depends(authorization),
    session: AsyncSession = Depends(get_db_session),
) -> JSONResponse:

    user = await get_user_by_sub(session, jwt_token.subject)
    row_applications = await get_all_applications_by_user_id(
        user_id=user.id,
        session=session,
    )
    if not row_applications:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Applications not found",
        )

    applications = [make_base_info_application(app) for app in row_applications]
    response_data = ApplicationsResponse(
        applications=applications,
    ).dict(exclude_none=True)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=response_data,
    )


@router.get("/{application_id}", response_model=ApplicationResponse)
async def get_application_by_id(
    application_id: int,
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
    jwt_token: JsonWebToken = Depends(authorization),
    session: AsyncSession = Depends(get_db_session),
) -> JSONResponse:

    user = await get_user_by_sub(session, jwt_token.subject)
    row_application = await get_application_by_application_id(
        application_id=application_id,
        session=session,
    )
    if not row_application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )
    if row_application.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No access to the application",
        )

    application = make_full_info_application(row_application)
    response_data = ApplicationResponse(
        application=application,
    ).dict(exclude_none=True)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=response_data,
    )
