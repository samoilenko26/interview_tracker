from typing import List, Optional

from pydantic import BaseModel

from interview_tracker.db.models.main_model import (
    Application,
    OnSiteRemoteEnum,
    StatusCategoryEnum,
)


class TimelineBase(BaseModel):
    id: int
    name: str
    value: str


class ApplicationBase(BaseModel):
    id: int
    company_name: str
    job_title: str
    status: str
    attractiveness_scale: int
    status_category: StatusCategoryEnum
    official_website: Optional[str]
    apply_icon: Optional[bool]
    job_description_link: Optional[str]
    salary: Optional[str]
    location: Optional[str]
    on_site_remote: Optional[OnSiteRemoteEnum]
    timelines: Optional[List[TimelineBase]]
    notes: Optional[str]


class ApplicationsResponse(BaseModel):
    applications: List[ApplicationBase]


def application_to_response(application: Application) -> ApplicationBase:
    timelines = [
        TimelineBase(id=timeline.id, name=timeline.name, value=timeline.value)
        for timeline in application.timelines
    ]
    return ApplicationBase(
        id=application.id,
        company_name=application.company_name,
        job_title=application.job_title,
        status=application.status,
        attractiveness_scale=application.attractiveness_scale,
        status_category=application.status_category,
        official_website=application.official_website,
        apply_icon=application.apply_icon,
        job_description_link=application.job_description_link,
        salary=application.salary,
        location=application.location,
        on_site_remote=application.on_site_remote,
        notes=application.notes,
        timelines=timelines,
    )
