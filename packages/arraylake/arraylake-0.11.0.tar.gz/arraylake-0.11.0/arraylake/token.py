import pathlib
from json import JSONDecodeError
from typing import Optional, Union
from webbrowser import open_new

import httpx
from pydantic import ValidationError
from rich.console import Console
from rich.prompt import Prompt

from arraylake.config import config
from arraylake.types import OauthTokens, OauthTokensResponse, UserInfo


class AuthException(ValueError):
    pass


class TokenHandler:
    """
    Class used to handle OAuth2
    """

    token_path: pathlib.Path
    tokens: Optional[OauthTokens]

    def __init__(
        self,
        api_endpoint: str = "https://api.earthmover.io",
        hint: Optional[str] = None,
        scopes: list[str] = ["email", "openid", "profile"],
        raise_if_not_logged_in: bool = False,
    ):
        self.api_endpoint = api_endpoint
        self.scopes = scopes
        self.hint = hint

        self.token_path = pathlib.Path(config.get("service.token_path", None) or "~/.arraylake/token.json").expanduser()
        self.default_headers = {"accept": "application/vnd.earthmover+json"}

        # get cached tokens
        self.tokens = None
        try:
            with self.token_path.open() as f:
                self.tokens = OauthTokens.model_validate_json(f.read())
        except (ValidationError, JSONDecodeError):
            if raise_if_not_logged_in:
                raise AuthException("Found malformed auth tokens, logout and log back in")
        except FileNotFoundError:
            if raise_if_not_logged_in:
                raise AuthException("Not logged in, please log in with `arraylake auth login`")

    async def get_authorize_url(self) -> str:
        body = {"scopes": self.scopes}
        async with httpx.AsyncClient() as client:
            params = {"hint": self.hint} if self.hint else {}
            response = await client.post(f"{self.api_endpoint}/login", json=body, headers=self.default_headers, params=params)
        if response.status_code != httpx.codes.OK:
            raise AuthException("failed to get authorization url")

        return response.json()["url"]

    async def get_token(self, code: str):
        params = {"code": code}
        if self.hint:
            params["hint"] = self.hint
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.api_endpoint}/token", params=params, headers=self.default_headers)
        if response.status_code != httpx.codes.OK:
            raise AuthException("unable to get token")
        new_token_data = OauthTokensResponse.model_validate_json(response.content)
        self.update(new_token_data)

    async def refresh_token(self):
        if self.tokens is None:
            raise ValueError("Must be logged in to refresh tokens")
        params = {"token": self.tokens.refresh_token.get_secret_value()}
        if self.hint:
            params["hint"] = self.hint
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.api_endpoint}/refresh_token", params=params, headers=self.default_headers)
        if response.status_code == httpx.codes.OK:
            # a refresh token is persisted over time
            # performing a fresh yields a new id + access token
            # perform an update with the new values, but maintain
            # the refresh token
            new_token_data = OauthTokensResponse.model_validate_json(response.content)
            self.update(new_token_data)
        else:
            raise AuthException("unable to refresh token")

    def update(self, new_token_data: Union[OauthTokensResponse, dict]):
        if isinstance(new_token_data, OauthTokensResponse):
            # converting to a dict allows us to update only non-default fields
            new_token_data = new_token_data.model_dump(exclude_none=True)

        if self.tokens is None:
            self.tokens = OauthTokens.model_validate(new_token_data)
        else:
            # a little work to make sure we write back
            # an OauthTokens object with the correct value types
            staged_token_data = self.tokens.model_dump()
            staged_token_data.update(new_token_data)
            self.tokens = OauthTokens.model_validate(staged_token_data)
        self.cache()

    def cache(self):
        if not self.tokens:
            raise ValueError("Error saving tokens, no tokens to cache")
        self.token_path.parent.mkdir(exist_ok=True)
        with self.token_path.open(mode="w") as fp:
            fp.write(self.tokens.model_dump_json(exclude_unset=True))
        self.token_path.chmod(0o100600)  # -rw-------

    def get_logout_url(self) -> str:
        endpoint = f"{self.api_endpoint}/logout"
        if self.hint:
            return f"{self.api_endpoint}/logout?hint={self.hint}"
        else:
            return endpoint

    def purge_cache(self):
        self.token_path.unlink()
        self.tokens = None

    async def _get_user(self) -> UserInfo:
        if self.tokens is None:
            raise AuthException("Not logged in")
        headers = {"Authorization": f"Bearer {self.tokens.id_token.get_secret_value()}", **self.default_headers}
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.api_endpoint}/user", headers=headers)
        if response.status_code != httpx.codes.OK:
            raise AuthException("unable to get user")
        return UserInfo.model_validate_json(response.content)

    async def login(self, *, browser: bool = False):
        rich_console = Console()

        has_tokens = False
        if self.tokens is not None:
            # try to refresh tokens if they are present but fail gracefully, the user is already expecting to log in
            try:
                await self.refresh_token()
                has_tokens = True
            except Exception:
                pass

        if not has_tokens:
            url = await self.get_authorize_url()
            if browser:
                open_new(url)
            else:
                docs_link = "https://docs.earthmover.io/arraylake/org-access#authenticating-as-a-user"

                rich_console.print("\n")
                rich_console.rule(":key: [bold]Authorize[/bold]", style="dim", align="left")
                rich_console.print(f"\n[dim]Copy and paste the following [link={url}]:link: link[/link] into your browser:[/dim]\n")
                rich_console.print(f"[blue]{url}[/blue]\n", soft_wrap=True)
                rich_console.print(
                    f"[dim]:down_arrow: Then enter the code below. Visit [link={docs_link}]docs.earthmover.io[/link] for help.[/dim]"
                )
            code = Prompt.ask("\n:sunglasses: [bold]Enter your code[/bold]")

            await self.get_token(code)

        # check that the token is valid
        user = await self._get_user()
        rich_console.print(user.model_dump_json())
        rich_console.print(f"✅ Token stored at {self.token_path}")

    async def logout(self, browser: bool = False) -> None:
        rich_console = Console()
        error_console = Console(stderr=True)

        try:
            url = self.get_logout_url()
            if browser:
                open_new(url)
            else:
                rich_console.print(f"To completely log out, open this URL in your browser: {url}")
            self.purge_cache()
            rich_console.print(f"✅ Token removed from {self.token_path}")
        except FileNotFoundError as e:
            error_console.print("Not logged in")
            raise AuthException(e)


def get_auth_handler(org: Optional[str] = None) -> TokenHandler:
    return TokenHandler(api_endpoint=config.get("service.uri"), hint=org or config.get("user.org", None))
