from fastapi import Depends

from interview_tracker.web.authorization.authorization_header_elements import (
    get_bearer_token,
)
from interview_tracker.web.authorization.json_web_token import JsonWebToken


def authorization(token: str = Depends(get_bearer_token)) -> JsonWebToken:
    return JsonWebToken(token)
