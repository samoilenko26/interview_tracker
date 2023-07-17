from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from interview_tracker.db.models.user import User


async def _create_new_user(session: AsyncSession, sub: str) -> User:
    user = User(sub=sub)
    session.add(user)
    await session.flush()
    await session.refresh(user)
    return user


async def get_user_by_sub(session: AsyncSession, sub: str) -> User:
    user_result = await session.execute(
        select(User).where(User.sub == sub),
    )
    user = user_result.scalar()
    if user:
        return user
    else:
        return await _create_new_user(session, sub)  # noqa: WPS503
