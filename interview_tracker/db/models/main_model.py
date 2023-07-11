from enum import Enum as PythonEnum

from sqlalchemy import Boolean, Column, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from interview_tracker.db.base import Base


class UserRoleEnum(str, PythonEnum):  # noqa: WPS600
    user = "user"
    admin = "admin"


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

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    role = Column(Enum(UserRoleEnum))  # type: ignore


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", backref="applications")
    company_name = Column(String)
    official_website = Column(String)
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
    contacts = relationship("Contact", backref="application")
    archived = Column(Boolean)


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", backref="contacts")
    application_id = Column(Integer, ForeignKey("applications.id"))
    application = relationship("Application", backref="contacts")
    name = Column(String)
    contact = Column(String)


class Timeline(Base):
    __tablename__ = "timelines"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", backref="timelines")
    application_id = Column(Integer, ForeignKey("applications.id"))
    application = relationship("Application", backref="timelines")
    name = Column(String)
    value = Column(String)


class Attachment(Base):
    __tablename__ = "attachments"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", backref="attachments")
    application_id = Column(Integer, ForeignKey("applications.id"))
    application = relationship("Application", backref="attachments")
    name = Column(String)
    link = Column(String)
