from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from interview_tracker.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    sub = Column(String)

    applications = relationship("Application", backref="user")
    contacts = relationship("Contact", backref="user")
    timelines = relationship("Timeline", backref="user")
    attachments = relationship("Attachment", backref="user")
