from pydantic import BaseModel, validator

from interview_tracker.db.models.main_model import UserRoleEnum
from interview_tracker.web.api.users.schemas.validators import (
    validate_email,
    validate_username,
)


class Message(BaseModel):
    name: str
    email: str
    role: UserRoleEnum

    _validate_name = validator("name", allow_reuse=True)(validate_username)
    _validate_email = validator("email", allow_reuse=True)(validate_email)
