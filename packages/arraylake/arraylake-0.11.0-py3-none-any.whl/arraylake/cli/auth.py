import typer

from arraylake import config
from arraylake.cli.utils import coro, error_console, print_logo, rich_console
from arraylake.token import AuthException, get_auth_handler

auth = typer.Typer(help="Manage Arraylake authentication")


@auth.command()
@coro  # type: ignore
async def login(
    browser: bool = typer.Option(True, help="Whether to automatically open a browser window."),
    org: str = typer.Option(None, help="Org identifier for custom login provider (only required if your default org uses SSO)."),
):
    """**Log in** to Arraylake

    This will automatically open a browser window. If **--no-browser** is specified, a link will be printed.

    **Examples**

    - Log in without automatically opening a browser window

        ```
        $ arraylake auth login --no-browser
        ```
    """
    print_logo()
    handler = get_auth_handler(org)
    await handler.login(browser=browser)


@auth.command()
@coro  # type: ignore
async def refresh() -> None:
    """**Refresh** Arraylake's auth token"""
    print_logo()
    handler = get_auth_handler()
    if handler.tokens is not None:
        await handler.refresh_token()
        user = await handler._get_user()  # checks that the new tokens are valid
        rich_console.print(user.model_dump_json())
        rich_console.print(f"✅ Token stored at {handler.token_path}")
    else:
        error_console.print("Not logged in, log in with `arraylake auth login`")
        raise typer.Exit(code=1)


@auth.command()
@coro  # type: ignore
async def logout(browser: bool = typer.Option(True, help="Whether to also remove the browsers auth cookie.")) -> None:
    """**Logout** of Arraylake

    **Examples**

    - Logout of arraylake

        ```
        $ arraylake auth logout
        ```
    """
    print_logo()
    try:
        handler = get_auth_handler()
        await handler.logout(browser=browser)
    except AuthException as e:
        error_console.print(e)
        raise typer.Exit(code=1)


@auth.command()
@coro
async def status():
    """Verify and display information about your authentication **status**"""
    print_logo()

    rich_console.print(f"Arraylake API Endpoint: {config.get('service.uri')}")
    try:
        handler = get_auth_handler()
        user = await handler._get_user()  # checks that the new tokens are valid
        rich_console.print(f"  → logged in as {user.email}")
    except AuthException:
        error_console.print("Not logged in, log in with `arraylake auth login`")
        raise typer.Exit(code=1)


@auth.command()
def token():
    """Display your authentication **token**"""
    print_logo()
    handler = get_auth_handler()
    if handler.tokens is None:
        error_console.print("Not logged in, log in with `arraylake auth login`")
        raise typer.Exit(code=1)
    try:
        rich_console.print(handler.tokens.id_token.get_secret_value())
    except (AuthException, AttributeError):
        error_console.print("Not logged in, log in with `arraylake auth login`")
        raise typer.Exit(code=1)
