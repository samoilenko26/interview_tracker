import json
from typing import Dict

import requests
from loguru._handler import memoize  # noqa: WPS436

from interview_tracker.settings import settings

testing_users = {
    "ga4la-salts0f@icloud.com": "6JV%Sza+&D6sV@b",
}


@memoize
def get_user_token_headers(
    user_name: str = "ga4la-salts0f@icloud.com",
) -> Dict[str, str]:
    return {"Authorization": "Bearer " + _get_user_token(user_name)}  # noqa: WPS336


def _get_user_token(user_name: str) -> str:
    url = f"https://{settings.auth0_domain}/oauth/token"
    headers = {"content-type": "application/json"}
    password = testing_users[user_name]
    parameter = {
        "client_id": settings.client_id,
        "client_secret": settings.client_secret,
        "audience": settings.auth0_audience,
        "grant_type": "password",
        "username": user_name,
        "password": password,
        "scope": "openid",
    }

    response = json.loads(
        requests.post(url, json=parameter, headers=headers).text,  # noqa: S113
    )
    return response["access_token"]


print(get_user_token_headers())  # noqa: WPS421
