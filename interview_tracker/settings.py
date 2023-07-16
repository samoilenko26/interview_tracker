import enum
from pathlib import Path
from tempfile import gettempdir

from pydantic import BaseSettings, validator
from yarl import URL

TEMP_DIR = Path(gettempdir())


class LogLevel(str, enum.Enum):  # noqa: WPS600
    """Possible log levels."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    host: str = "127.0.0.1"
    port: int = 8000
    # quantity of workers for uvicorn
    workers_count: int = 1
    # Enable uvicorn reloading
    reload: bool = False

    # Current environment
    environment: str = "dev"

    log_level: LogLevel = LogLevel.INFO

    auth0_audience: str = ""
    auth0_domain: str = ""
    client_origin_url: str = ""

    @classmethod
    @validator("client_origin_url", "auth0_audience", "auth0_domain")
    def check_not_empty(cls, variable: str) -> str:
        if variable == "":
            raise ValueError(f"{variable} is not defined")
        return variable

    # Variables for the database
    db_host: str = "localhost"
    db_port: int = 5432
    db_user: str = "interview_tracker"
    db_pass: str = "interview_tracker"
    db_base: str = "interview_tracker"
    db_echo: bool = False

    @property
    def db_url(self) -> URL:
        """
        Assemble database URL from settings.

        :return: database URL.
        """
        return URL.build(
            scheme="postgresql+asyncpg",
            host=self.db_host,
            port=self.db_port,
            user=self.db_user,
            password=self.db_pass,
            path=f"/{self.db_base}",
        )

    class Config:
        env_file = ".env"
        env_prefix = "INTERVIEW_TRACKER_"
        env_file_encoding = "utf-8"


settings = Settings()
