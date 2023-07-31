from enum import Enum as PythonEnum
from typing import List, Optional

from sqlalchemy import Boolean, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from interview_tracker.db.base import Base


class OnSiteRemoteEnum(str, PythonEnum):  # noqa: WPS600
    remote = "remote"
    onsite = "onsite"
    hybrid = "hybrid"


class StatusCategoryEnum(str, PythonEnum):  # noqa: WPS600
    red = "red"
    blue = "blue"
    green = "green"
    yellow = "yellow"
    orange = "orange"
    purple = "purple"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sub: Mapped[str] = mapped_column(String)

    applications: Mapped[List["Application"]] = relationship(
        "Application",
        back_populates="user",
    )


class Application(Base):
    __tablename__ = "applications"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    company_name: Mapped[str] = mapped_column(String)
    job_title: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String)
    attractiveness_scale: Mapped[int] = mapped_column(Integer)
    status_category: Mapped[StatusCategoryEnum] = mapped_column(
        Enum(StatusCategoryEnum),
    )
    official_website: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    apply_icon: Mapped[str] = mapped_column(Boolean, nullable=True)
    icon: Mapped[str] = mapped_column(String, nullable=True)
    job_description_link: Mapped[str] = mapped_column(String, nullable=True)
    salary: Mapped[str] = mapped_column(String, nullable=True)
    location: Mapped[str] = mapped_column(String, nullable=True)
    on_site_remote: Mapped[OnSiteRemoteEnum] = mapped_column(
        Enum(OnSiteRemoteEnum),
        nullable=True,
    )
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    archived: Mapped[bool] = mapped_column(Boolean)

    user: Mapped["User"] = relationship("User", back_populates="applications")
    timelines: Mapped[List["Timeline"]] = relationship(
        "Timeline",
        back_populates="application",
        cascade="all, delete-orphan",
    )


class Timeline(Base):
    __tablename__ = "timelines"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    application_id: Mapped[int] = mapped_column(Integer, ForeignKey("applications.id"))
    name: Mapped[str] = mapped_column(String)
    value: Mapped[str] = mapped_column(String)

    application: Mapped["Application"] = relationship(
        "Application",
        back_populates="timelines",
    )
