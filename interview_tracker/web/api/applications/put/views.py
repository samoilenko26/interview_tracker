from fastapi import APIRouter, Depends, Response, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from interview_tracker.db.data_access_layer.application import (
    delete_timelines,
    get_application_by_application_id,
    save_application,
    save_timeline,
)
from interview_tracker.db.data_access_layer.user import get_user_by_sub
from interview_tracker.db.dependencies import get_db_session
from interview_tracker.db.models.main_model import Timeline
from interview_tracker.web.api.applications.put.schemas.application import (
    ApplicationPutMessage,
)
from interview_tracker.web.authorization.dependencies import authorization
from interview_tracker.web.authorization.json_web_token import JsonWebToken

auth_scheme = HTTPBearer()
router = APIRouter()


@router.put("/{application_id}/")
async def update_application(  # noqa: WPS210
    application_id: int,
    incoming_message: ApplicationPutMessage,
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
    jwt_token: JsonWebToken = Depends(authorization),
    session: AsyncSession = Depends(get_db_session),
) -> Response:
    user = await get_user_by_sub(session, jwt_token.subject)
    application = await get_application_by_application_id(
        session=session,
        application_id=application_id,
    )

    if not application:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    if application.user_id != user.id:
        return Response(status_code=status.HTTP_403_FORBIDDEN)

    application_data = incoming_message.dict(exclude_unset=True, exclude={"timelines"})
    for key, value in application_data.items():
        setattr(application, key, value)
    await save_application(session=session, application=application)

    timelines_data = incoming_message.dict().get("timelines")
    existing_timelines = {
        timeline.name: timeline.value for timeline in application.timelines
    }
    if timelines_data is not None and timelines_data != existing_timelines:
        await delete_timelines(application=application, session=session)

        for timeline_data in timelines_data:
            timeline = Timeline(
                user_id=user.id,
                application_id=application.id,
                **timeline_data,
            )
            await save_timeline(session=session, timeline=timeline)

    return Response(status_code=status.HTTP_200_OK)
