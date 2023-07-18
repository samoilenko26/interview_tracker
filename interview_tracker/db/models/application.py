from enum import Enum as PythonEnum

from sqlalchemy import Boolean, Column, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

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


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    company_name = Column(String)
    official_website = Column(String)
    apply_icon = Column(Boolean)
    icon = Column(String)
    job_title = Column(String)
    job_description_link = Column(String)
    attractiveness_scale = Column(Integer)
    status = Column(String)
    status_category = Column(Enum(StatusCategoryEnum))  # type: ignore
    salary = Column(String)
    location = Column(String)
    on_site_remote = Column(Enum(OnSiteRemoteEnum))  # type: ignore
    notes = Column(Text)
    archived = Column(Boolean)

    contacts = relationship("Contact", backref="application")
    timelines = relationship("Timeline", backref="application")
    attachments = relationship("Attachment", backref="application")


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    application_id = Column(Integer, ForeignKey("applications.id"))
    name = Column(String)
    contact = Column(String)


class Timeline(Base):
    __tablename__ = "timelines"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    application_id = Column(Integer, ForeignKey("applications.id"))
    name = Column(String)
    value = Column(String)


class Attachment(Base):
    __tablename__ = "attachments"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    application_id = Column(Integer, ForeignKey("applications.id"))
    name = Column(String)
    link = Column(String)
