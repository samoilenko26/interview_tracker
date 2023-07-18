from sqlalchemy.ext.asyncio import AsyncSession

from interview_tracker.db.models.application import Application, Timeline


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
