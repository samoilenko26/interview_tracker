from importlib import metadata

from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from fastapi.middleware.cors import CORSMiddleware
from interview_tracker.logger import configure_logging
from interview_tracker.web.api.router import api_router
from interview_tracker.web.lifetime import (
    register_shutdown_event,
    register_startup_event,
    register_middleware,
    register_exception_handler
)
from interview_tracker.settings import settings

def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    configure_logging()
    app = FastAPI(
        title="interview_tracker",
        version=metadata.version("interview_tracker"),
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
        reload=settings.reload,
        server_header=False,
    )

    # Adds startup and shutdown events.
    register_startup_event(app)
    register_shutdown_event(app)
    #register_middleware(app)
    register_exception_handler(app)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.client_origin_url],
        allow_methods=["GET"],
        allow_headers=["Authorization", "Content-Type"],
        max_age=86400,
    )

    # Main router for the API.
    app.include_router(router=api_router, prefix="/api")

    return app
