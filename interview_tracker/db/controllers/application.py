from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from interview_tracker.db.models.main_model import Application, Timeline


async def save_application(
    session: AsyncSession,
    application: Application,
) -> Application:
    session.add(application)
    await session.flush()
    await session.refresh(application)

    return application


async def save_timeline(
    session: AsyncSession,
    timeline: Timeline,
) -> Timeline:
    session.add(timeline)
    await session.flush()
    await session.refresh(timeline)

    return timeline


async def get_application_by_user_id(
    user_id: int,
    session: AsyncSession,
) -> Sequence[Application]:
    query = select(Application).filter_by(user_id=user_id)
    result = await session.execute(query)

    return result.unique().scalars().all()
