from typing import List, Optional

from pydantic import BaseModel, validator
from pydantic.class_validators import partial

from interview_tracker.db.models.application import OnSiteRemoteEnum, StatusCategoryEnum
from interview_tracker.web.api.applications.schemas.validators import (
    validate_attractiveness_scale,
    validate_length,
)


class TimelineBase(BaseModel):
    name: str
    value: str

    _validate_length = validator("name", "value", allow_reuse=True)(
        partial(validate_length, min_len=1, max_len=400),  # noqa: WPS432
    )


class ApplicationCreateMessage(BaseModel):
    company_name: str
    job_title: str
    status: str
    attractiveness_scale: int
    status_category: StatusCategoryEnum
    official_website: Optional[str]
    apply_icon: Optional[bool] = False
    job_description_link: Optional[str]
    salary: Optional[str]
    location: Optional[str]
    on_site_remote: Optional[OnSiteRemoteEnum]
    timelines: Optional[List[TimelineBase]]
    notes: Optional[str]

    _validate_length = validator(
        "company_name",
        "job_title",
        "status",
        "official_website",
        "job_description_link",
        "salary",
        "location",
        allow_reuse=True,
    )(
        partial(validate_length, min_len=1, max_len=400),  # noqa: WPS432
    )

    _validate_attractiveness_scale = validator(
        "attractiveness_scale",
        allow_reuse=True,
    )(
        validate_attractiveness_scale,
    )
