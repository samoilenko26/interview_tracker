"""interview_tracker applications package."""
from interview_tracker.web.api.applications.delete.views import router as delete
from interview_tracker.web.api.applications.get.views import router as get
from interview_tracker.web.api.applications.post.views import router as post
from interview_tracker.web.api.applications.put.views import router as put

__all__ = ["post", "get", "delete", "put"]
