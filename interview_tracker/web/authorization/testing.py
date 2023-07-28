import json
from typing import Dict

import requests
from loguru._handler import memoize  # noqa: WPS436

from interview_tracker.settings import settings

testing_users = {
    "definition": ("email", "password", "sub"),
    "user_1": (
        "ga4la-salts0f@icloud.com",
        "6JV%Sza+&D6sV@b",
        "64b71e183dd4fa545798abf4",
    ),
    "user_2": ("rkfm-09-jnjn@gmail.com", "UeU4.cKF*^Dn+3u", "64c0f6419df8b5e7de879a8b"),
}


@memoize
def get_user_token_headers(user_id: str = "user_1") -> Dict[str, str]:
    user = testing_users[user_id]
    return {"Authorization": "Bearer " + _get_user_token(user)}  # noqa: WPS336


def _get_user_token(user: tuple[str, str, str]) -> str:
    url = f"https://{settings.auth0_domain}/oauth/token"
    headers = {"content-type": "application/json"}
    parameter = {
        "client_id": settings.client_id,
        "client_secret": settings.client_secret,
        "audience": settings.auth0_audience,
        "grant_type": "password",
        "username": user[0],
        "password": user[1],
        "scope": "openid",
    }

    response = json.loads(
        requests.post(url, json=parameter, headers=headers).text,  # noqa: S113
    )
    return response["access_token"]


print(get_user_token_headers())  # noqa: WPS421
