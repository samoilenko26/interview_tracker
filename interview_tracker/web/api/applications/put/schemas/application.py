from typing import List, Optional

from pydantic import BaseModel, validator
from pydantic.class_validators import partial

from interview_tracker.db.models.main_model import OnSiteRemoteEnum, StatusCategoryEnum
from interview_tracker.web.api.applications.post.schemas.application import Timeline
from interview_tracker.web.api.applications.post.schemas.validators import (
    validate_attractiveness_scale,
    validate_length,
)


class ApplicationPutMessage(BaseModel):
    company_name: Optional[str] = None
    job_title: Optional[str] = None
    status: Optional[str] = None
    attractiveness_scale: Optional[int] = None
    status_category: Optional[StatusCategoryEnum] = None
    official_website: Optional[str] = None
    apply_icon: Optional[bool] = None
    icon: Optional[str] = None
    job_description_link: Optional[str] = None
    salary: Optional[str] = None
    location: Optional[str] = None
    on_site_remote: Optional[OnSiteRemoteEnum] = None
    notes: Optional[str] = None
    timelines: Optional[List[Timeline]] = None

    _validate_length = validator(
        "company_name",
        "job_title",
        "status",
        "icon",
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
