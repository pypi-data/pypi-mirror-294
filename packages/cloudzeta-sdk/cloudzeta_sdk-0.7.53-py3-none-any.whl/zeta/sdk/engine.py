from __future__ import annotations
from cryptography.fernet import Fernet
from google.cloud import firestore
from google.oauth2 import credentials
import os
import requests
import time

from zeta.db.base import ZetaBase
from zeta.sdk.asset import ZetaAsset
from zeta.utils.logging import zetaLogger
from zeta.utils.downloader import AssetDownloader


CLOUD_ZETA_PROJECT_ID = "gozeta-prod"
CLOUD_ZETA_API_KEY = "AIzaSyBBDfxgpOAnH7GJ6RNu0Q_v79OGbVr1V2Q"
CLOUD_ZETA_URL_PREFIX = "https://cloudzeta.com"
GOOGLE_AUTH_URL = "https://securetoken.googleapis.com/v1/token"


class ZetaEngine(object):
    def __init__(self, api_key=CLOUD_ZETA_API_KEY, zeta_url_prefix=CLOUD_ZETA_URL_PREFIX):
        self._api_key = api_key
        self._zeta_url_prefix = zeta_url_prefix

        self._auth_token = None
        self._auth_token_expiry = 0
        self._refresh_token = None
        self._user_uid = None

        self._db: firestore.Client = None

    def make_url(self, *elements) -> str:
        # Note that here os.path.join may not work as certain elements may start with a /
        return self._zeta_url_prefix + "/" + os.path.normpath("/".join(elements))

    def login(self, token_uid: str, encryption_key: str) -> bool:
        """
        Login with the given token_uid and encryption_key.

        @param token_uid: The token_uid to login with.
        @param encryption_key: The encryption_key to decrypt the token with.
        """
        if not token_uid or not encryption_key:
            zetaLogger.error("Token ID and/or encryption key is empty.")
            return False

        zeta_auth_token_url = f"{self._zeta_url_prefix}/api/auth/token/get"
        response = requests.get(zeta_auth_token_url, params={"authToken": token_uid})
        if not response.ok:
            zetaLogger.error(f"Failed to get auth token")
            return False

        res = response.json()
        encrypted_token = res.get("encryptedToken")

        try:
            fernet = Fernet(encryption_key.encode())
            self._refresh_token = fernet.decrypt(encrypted_token.encode()).decode()
        except Exception as e:
            zetaLogger.error("Failed to decrypt token.")
            return False

        return self.refresh_auth_token()

    def refresh_auth_token(self) -> bool:
        """
        Refresh the authentication token from the refresh token.

        Must be called after login().
        """
        if not self._refresh_token:
            zetaLogger.error("Refresh token is empty.")
            return False

        google_login_url = f"{GOOGLE_AUTH_URL}?key={self._api_key}"
        response = requests.post(
            google_login_url,
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
            }, data={
                "grant_type": "refresh_token",
                "refresh_token": self._refresh_token,
            }
        )

        if not response.ok:
            zetaLogger.error(f"Failed to login with auth token")
            return False

        res = response.json()
        self._auth_token = res["id_token"]
        self._user_uid = res["user_id"]
        assert self._refresh_token == res["refresh_token"]
        assert self._auth_token is not None
        assert self._user_uid is not None

        try:
            # self._auth_token_expiry = int(time.time() + int(res["expires_in"]))
            self._auth_token_expiry = int(time.time() - int(res["expires_in"]))
        except ValueError:
            # Default to 30 minutes expiry
            self._auth_token_expiry = int(time.time() + 1800)

        cred = credentials.Credentials(
            self._auth_token, self._refresh_token, client_id="", client_secret="",
            token_uri=f"{GOOGLE_AUTH_URL}?key={self._api_key}")

        self._db = firestore.Client(CLOUD_ZETA_PROJECT_ID, cred)
        assert self._db is not None

        # Initialize the ZetaBase and AssetDownloader to use the credentials from this login.
        ZetaBase.set_client(self._db)
        AssetDownloader.set_engine(self)

        return True

    def ensure_auth_token(method):
        def wrapper(self, *args, **kwargs):
            if not self._auth_token or self._auth_token_expiry < time.time():
                if not self.refresh_auth_token():
                    raise PermissionError("Failed to refresh auth token")

            return method(self, *args, **kwargs)
        return wrapper

    @ensure_auth_token
    def api_get(self, url: str, params: dict) -> requests.Response:
        if not self._auth_token:
            raise ValueError("Must login() before get()")
        if not url.startswith("/"):
            raise ValueError("URL must start with /")

        full_url: str = f"{self._zeta_url_prefix}{url}"
        return requests.get(
            full_url,
            headers={
                "Authorization": f"Bearer {self._auth_token}",
            },
            params=params
        )

    @ensure_auth_token
    def api_post(self, url: str, json: dict) -> requests.Response:
        if not self._auth_token:
            raise ValueError("Must login() before get()")
        if not url.startswith("/"):
            raise ValueError("URL must start with /")

        full_url: str = f"{self._zeta_url_prefix}{url}"
        return requests.post(
            full_url,
            headers={
                "Authorization": f"Bearer {self._auth_token}",
                "Content-Type": "application/json",
            },
            json=json
        )

    @ensure_auth_token
    def asset(self, owner_name: str, project_name: str, asset_path: str) -> ZetaAsset:
        return ZetaAsset(self, owner_name, project_name, asset_path)