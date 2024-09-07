import os
import httpx
from fastapi import HTTPException
from chainlit.user import User
from chainlit.oauth_providers import OAuthProvider
import json
from dotenv import load_dotenv

load_dotenv()


class LineOAuthProvider(OAuthProvider):
    id = "line"
    env = [
        "OAUTH_LINE_CLIENT_ID",
        "OAUTH_LINE_CLIENT_SECRET",
        "OAUTH_LINE_REDIRECT_URI",
    ]

    authorize_url = "https://access.line.me/oauth2/v2.1/authorize"
    token_url = "https://api.line.me/oauth2/v2.1/token"
    userinfo_url = "https://api.line.me/v2/profile"

    def __init__(self):
        print("[LineOAuthProvider]init line oauth provider")
        self.client_id = os.getenv("OAUTH_LINE_CLIENT_ID", "")
        self.client_secret = os.getenv("OAUTH_LINE_CLIENT_SECRET", "")
        self.redirect_uri = os.getenv("OAUTH_LINE_REDIRECT_URI", "")
        print(f"[LineOAuthProvider][__init__]client_id: {self.client_id}")
        print(f"[LineOAuthProvider][__init__]client_secret: {self.client_secret}")
        print(f"[LineOAuthProvider][__init__]redirect_uri: {self.redirect_uri}")
        print(f"[LineOAuthProvider][__init__]scope: profile openid")
        self.authorize_params = {
            "response_type": "code",
            "scope": "profile openid",
        }

    async def get_token(self, code: str, url: str) -> str:
        print("[LineOAuthProvider][get_token]get_token<====")
        print(f"[LineOAuthProvider][get_token]code: {code}")
        print(f"[LineOAuthProvider][get_token]url: {url}")
        payload = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": url,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(self.token_url, data=payload)
            print(f"[LineOAuthProvider][get_token]response: {response.json()}")
        response.raise_for_status()
        print(f"[LineOAuthProvider][get_token]response: {response.json()}")
        return response.json()["access_token"]

    async def get_user_info(self, token: str):
        print("[LineOAuthProvider][get_user_info]get_user_info<====")
        print(f"[LineOAuthProvider][get_user_info]token: {token}")
        headers = {"Authorization": f"Bearer {token}"}
        async with httpx.AsyncClient() as client:
            response = await client.get(self.userinfo_url, headers=headers)
        response.raise_for_status()
        user_info = response.json()
        print(f"[LineOAuthProvider][get_user_info]user_info: {user_info}")
        user = User(
            identifier=user_info["userId"],
            metadata={"provider": "line", "name": user_info.get("displayName")},
        )
        print(f"[LineOAuthProvider][get_user_info]user: {user}")
        return user_info, user
