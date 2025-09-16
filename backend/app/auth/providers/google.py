from typing import Dict
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")

GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_TOKEN_INFO_URL = "https://oauth2.googleapis.com/tokeninfo"

class GoogleOAuth:
    async def _decode_id_token(self, id_token):
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                GOOGLE_TOKEN_INFO_URL,
                params={"id_token": id_token}
            )
            return resp.json()

    async def get_user_info(self, provider_id: str) -> Dict[str, str]:
        """
        Make request to Google and exchange code on OpenID token
        """
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                GOOGLE_TOKEN_URL,
                data={ 
                "code": provider_id,
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "redirect_uri": GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code"
            },
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            if resp.status_code != 200:
                raise ValueError(f"Google token exchange failed: {resp.text}")

            token_data = resp.json()
            userInfo = await self._decode_id_token(token_data["id_token"])

            email = userInfo.get("email")
            name = userInfo.get("name")

            if not email:
                raise ValueError("Cannot retrieve email from Google token")
            ret = {"email": email, "name": name}
            return ret
