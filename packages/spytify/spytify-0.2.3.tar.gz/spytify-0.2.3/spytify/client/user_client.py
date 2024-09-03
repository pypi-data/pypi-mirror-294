"""Client to interact with the Spotify Web API using the authorization code flow."""

import logging
import urllib
import urllib.parse
from base64 import b64encode
from secrets import token_urlsafe

from spytify.client.base import BaseClient


class UserClient(BaseClient):
    """Server client to interact with the Spotify Web API.

    This client is meant to be used with the authorization code flow. Using this flow,
    the client can access all user-related endpoints of the Spotify Web API.

    The client needs to be authorized by the user before it can access the user's data.
    Given the client ID, client secret, and redirect URI, the client can generate an
    authorization URL to authorize the application. After the user authorizes the
    application, the client can set the authorization code and log in to the Spotify Web API.
    """

    def __init__(self, client_id: str, client_secret, scope: str, redirect_uri: str):
        super().__init__(client_id)
        self.__scope = scope
        self.__redirect_uri = redirect_uri
        self.__client_secret = client_secret

        self.__logger = logging.getLogger(__name__)
        self.__authorization_code = None
        self.__state = None
        self.__user_id = None
        self.__validate_credentials()

    def __validate_credentials(self):
        if not self.__scope:
            raise ValueError("Scope not defined!")
        if not self.__client_secret:
            raise ValueError("Client secret not defined!")
        if not self.__redirect_uri:
            raise ValueError("Redirect URI not defined!")

    def generate_random_string(self, length: int) -> str:
        """Generate a random string of a given length."""
        return token_urlsafe(length)

    def build_authorization_url(self) -> str:
        """Build the authorization URL to authorize the application."""
        self.__state = self.generate_random_string(16)

        payload = {
            "response_type": "code",
            "client_id": self._client_id,
            "scope": self.__scope,
            "redirect_uri": self.__redirect_uri,
            "state": self.__state,
        }

        authorization_url = (
            f"{self._LOGIN_BASE_ENDPOINT}/authorize?{urllib.parse.urlencode(payload)}"
        )

        return authorization_url

    def set_authorization_code(self, authorization_code: str):
        """Set the authorization code to be used for authorization."""
        self.__authorization_code = authorization_code

    def login(self):
        """Login to the Spotify Web API using the authorization code."""

        if self.__authorization_code is None:
            raise ValueError(
                "Authorization code not defined! Set it before logging in."
            )

        payload = {
            "grant_type": "authorization_code",
            "code": self.__authorization_code,
            "redirect_uri": self.__redirect_uri,
        }

        basic_data = b64encode(
            f"{self._client_id}:{self.__client_secret}".encode()
        ).decode()

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {basic_data}",
        }

        response_data = self._post_request(
            route="/api/token",
            data=payload,
            authorize=False,
            additional_headers=headers,
            base_endpoint=self._LOGIN_BASE_ENDPOINT,
        )

        self._token = response_data["access_token"]

        user = self.get_user()
        self.__user_id = user["id"]

    def is_state_valid(self, state: str) -> bool:
        """Verify the state sent by the Spotify Web API."""

        return state == self.__state

    def get_user(self):
        """Get the user's information.

        Requires the `user-read-private, user-read-email` scopes.
        """
        return self._get_request(route="/me")

    def create_playlist(
        self,
        name: str,
        public: bool = False,
        collaborative: bool = False,
        description: str = None,
    ):
        """Create a new playlist in the user's Spotify account."""

        return self._post_request(
            route=f"/users/{self.__user_id}/playlists",
            data={
                "name": name,
                "public": public,
                "collaborative": collaborative,
                "description": description,
            },
            authorize=True,
        )

    def add_items_to_playlist(self, playlist_id: str, uris: list[str]):
        """Add items to a playlist."""

        if len(uris) > 100:
            raise ValueError("Cannot add more than 100 items at once.")

        return self._post_request(
            route=f"/playlists/{playlist_id}/tracks",
            data={"uris": uris},
            authorize=True,
        )
