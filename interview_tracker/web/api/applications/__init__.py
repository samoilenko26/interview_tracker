"""interview_tracker applications package."""
from interview_tracker.web.api.applications.delete.views import router as delete
from interview_tracker.web.api.applications.get.views import router as get
from interview_tracker.web.api.applications.post.views import router as post

__all__ = ["post", "get", "delete"]
