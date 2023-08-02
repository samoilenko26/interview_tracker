from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from interview_tracker.db.models.main_model import Application, Timeline


async def save_application(
    session: AsyncSession,
    application: Application,
) -> Application:
    session.add(application)
    await session.flush()
    # We do not need attribute_names=["timelines"] until we
    # create application without timelines
    await session.refresh(application)  # attribute_names=["timelines"]
    return application


async def save_timeline(
    session: AsyncSession,
    timeline: Timeline,
) -> Timeline:
    session.add(timeline)
    await session.flush()
    await session.refresh(timeline)
    return timeline


async def get_all_applications_by_user_id(
    user_id: int,
    session: AsyncSession,
) -> Sequence[Application]:
    query = select(Application).filter(Application.user_id == user_id)
    result = await session.execute(query)
    return result.scalars().all()


async def get_application_by_application_id(
    application_id: int,
    session: AsyncSession,
) -> Optional[Application]:
    query = (
        select(Application)
        .options(selectinload(Application.timelines))
        .filter(Application.id == application_id)
    )
    result = await session.execute(query)
    return result.unique().scalars().first()


async def get_timeline_by_id(
    timeline_id: int,
    session: AsyncSession,
) -> Optional[Timeline]:
    query = select(Timeline).filter(Timeline.id == timeline_id)
    result = await session.execute(query)
    return result.unique().scalars().first()


async def delete_timelines(
    application: Application,
    session: AsyncSession,
) -> None:
    for timeline in application.timelines:
        await session.delete(timeline)
    await session.flush()
    await session.refresh(application, attribute_names=["timelines"])


async def delete_application(
    application: Application,
    session: AsyncSession,
) -> None:
    await delete_timelines(application=application, session=session)
    await session.delete(application)
    await session.flush()
