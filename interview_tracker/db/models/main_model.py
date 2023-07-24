from enum import Enum as PythonEnum
from typing import List

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
    official_website: Mapped[str] = mapped_column(String)
    apply_icon: Mapped[str] = mapped_column(Boolean)
    icon: Mapped[str] = mapped_column(String)
    job_title: Mapped[str] = mapped_column(String)
    job_description_link: Mapped[str] = mapped_column(String)
    attractiveness_scale: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String)
    status_category: Mapped[StatusCategoryEnum] = mapped_column(
        Enum(StatusCategoryEnum),
    )
    salary: Mapped[str] = mapped_column(String)
    location: Mapped[str] = mapped_column(String)
    on_site_remote: Mapped[OnSiteRemoteEnum] = mapped_column(Enum(OnSiteRemoteEnum))
    notes: Mapped[str] = mapped_column(Text)
    archived: Mapped[bool] = mapped_column(Boolean)

    user: Mapped["User"] = relationship("User", back_populates="applications")
    timelines: Mapped[List["Timeline"]] = relationship(
        "Timeline",
        back_populates="application",
        lazy="joined",
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
