from sqlalchemy.orm import DeclarativeBase

from interview_tracker.db.meta import meta


class Base(DeclarativeBase):
    """Base for all models."""

    metadata = meta
