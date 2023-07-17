from typing import Any, Dict

import jwt

from interview_tracker.settings import settings
from interview_tracker.web.authorization.custom_exceptions import (
    BadCredentialsException,
    UnableCredentialsException,
)


class JsonWebToken:  # noqa: WPS230
    def __init__(self, jwt_access_token: str):
        self.jwt_access_token: str = jwt_access_token
        self.auth0_issuer_url: str = f"https://{settings.auth0_domain}/"
        self.auth0_audience: str = settings.auth0_audience
        self.algorithm: str = "RS256"
        self.jwks_uri: str = f"{self.auth0_issuer_url}.well-known/jwks.json"
        self.payload: Dict[str, Any] = {}
        self.is_valid: bool = self.validate()

    def validate(self) -> bool:
        try:
            jwks_client = jwt.PyJWKClient(self.jwks_uri)
            jwt_signing_key = jwks_client.get_signing_key_from_jwt(
                self.jwt_access_token,
            ).key
            self.payload = jwt.decode(
                self.jwt_access_token,
                jwt_signing_key,
                algorithms=self.algorithm,  # type: ignore
                audience=self.auth0_audience,
                issuer=self.auth0_issuer_url,
            )
        except jwt.exceptions.PyJWKClientError:  # noqa: WPS329
            raise UnableCredentialsException
        except jwt.exceptions.InvalidTokenError:  # noqa: WPS329
            raise BadCredentialsException
        return True

    @property
    def subject(self) -> str:
        try:
            return self.payload.get("sub").split("|")[1]  # type: ignore
        except (AttributeError, IndexError):  # noqa: WPS329
            raise BadCredentialsException
