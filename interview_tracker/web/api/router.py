from fastapi.routing import APIRouter

from interview_tracker.web.api import applications, echo, monitoring, users

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(echo.router, prefix="/echo", tags=["echo"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(
    applications.post,
    prefix="/applications",
    tags=["applications"],
)
api_router.include_router(
    applications.get,
    prefix="/applications",
    tags=["applications"],
)
api_router.include_router(
    applications.delete,
    prefix="/applications",
    tags=["applications"],
)
api_router.include_router(
    applications.put,
    prefix="/applications",
    tags=["applications"],
)
