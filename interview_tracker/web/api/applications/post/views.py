from fastapi import APIRouter, Depends, Response, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from interview_tracker.db.controllers.application import save_application, save_timeline
from interview_tracker.db.controllers.user import get_user_by_sub
from interview_tracker.db.dependencies import get_db_session
from interview_tracker.db.models.main_model import Application, Timeline
from interview_tracker.web.api.applications.post.schemas.application import (
    ApplicationPostMessage,
)
from interview_tracker.web.authorization.dependencies import authorization
from interview_tracker.web.authorization.json_web_token import JsonWebToken

auth_scheme = HTTPBearer()
router = APIRouter()


@router.post("/")
async def create_application(  # noqa: WPS210
    incoming_message: ApplicationPostMessage,
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
    jwt_token: JsonWebToken = Depends(authorization),
    session: AsyncSession = Depends(get_db_session),
) -> Response:
    user = await get_user_by_sub(session, jwt_token.subject)

    application_data = incoming_message.dict(exclude={"timelines"})
    application = Application(user_id=user.id, archived=False, **application_data)
    application = await save_application(
        session=session,
        application=application,
    )

    timelines_data = incoming_message.dict().pop("timelines", [])
    if timelines_data:
        for timeline_data in timelines_data:
            timeline = Timeline(
                user_id=user.id,
                application_id=application.id,
                **timeline_data,
            )
            await save_timeline(session=session, timeline=timeline)

    return Response(status_code=status.HTTP_201_CREATED)
